from rest_framework import viewsets
from rest_framework.response import Response
from product.models import ProductCategory, Product, BudClass
from api.serializers.get_product_menu import CategoryProductSerializer, AllProductSerializer, BudClassSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from product.models import BranchStock
import jwt
from django.db.models import OuterRef, Subquery, Sum



class CategoryProductViewSetMenu(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]

    def list(self, request):
        # print(request)
        jwt_token = request.META.get("HTTP_AUTHORIZATION")
        jwt_token = jwt_token.split()[1]
        try:
            token_data = jwt.decode(jwt_token, options={"verify_signature": False})  # Disable signature verification for claims extraction
            user_id = token_data.get("user_id")
            username = token_data.get("username")
            role = token_data.get("role")
            # You can access other claims as needed 

            # Assuming "branch" is one of the claims, access it
            branch = token_data.get("branch")

            # Print the branch
            print("Branch:", branch)
        except jwt.ExpiredSignatureError:
            print("Token has expired.")
        except jwt.DecodeError:
            print("Token is invalid.")
        budclasses = BudClass.objects.all()
        data = []

        # all_products = Product.objects.filter(is_deleted=False)

        branchstock_quantity_subquery_all = BranchStock.objects.filter(
            product=OuterRef('pk'),
            branch=branch
        ).values('product').annotate(total_quantity=Sum('quantity')).values('total_quantity')[:1]

        all_products = Product.objects.annotate(branchstock_total_quantity=Subquery(branchstock_quantity_subquery_all)).filter(
            is_deleted = False,
            branchstock_total_quantity__gt=0,
            is_menu_item = True
        )

        
        all_products_serializer = AllProductSerializer(all_products, many=True, context={"branch": branch})

        all_data = {"All": all_products_serializer.data}
        data.append(all_data)

        for budclass in budclasses:
            branchstock_quantity_subquery = BranchStock.objects.filter(
                product=OuterRef('pk'),
                branch=branch
            ).values('product').annotate(total_quantity=Sum('quantity')).values('total_quantity')[:1]

            # Filter products with total quantity greater than 0
            products = Product.objects.annotate(branchstock_total_quantity=Subquery(branchstock_quantity_subquery)).filter(
                is_deleted=False,
                budclass=budclass,
                branchstock_total_quantity__gt=0,
                is_menu_item = True
            )
            
            serializer = CategoryProductSerializer(
                {
                    "budclass_name": budclass.title,
                    "budclassid": budclass.id,
                    "products": products,
                },
                many=False,
                context={"branch": branch}
            )
            data.append(serializer.data)

                # Sort the BudClassProducts by the title of the products within each BudClass
            data[1:] = sorted(data[1:], key=lambda x: x["budclass_name"])

        # Combine data from both serializers
        combined_data = {
            "All": all_products_serializer.data,
            "BudClassProducts": data[1:],  # Exclude the "All" data
        }

        return Response(combined_data)

