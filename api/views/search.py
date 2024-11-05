# # views.py
# from rest_framework import generics
# from rest_framework import filters
# from django.db.models import Q
# from product.models import Product
# from api.serializers.search import ProductSerializer

# class ProductSearchAPIView(generics.ListAPIView):
#     serializer_class = ProductSerializer
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['title', 'category__title', 'budclass__title']

#     def get_queryset(self):
#         keyword = self.request.query_params.get('keyword')
#         if keyword:
#             queryset = Product.objects.filter(
#                 Q(title__icontains=keyword) |
#                 Q(category__title__icontains=keyword) |
#                 Q(budclass__title__icontains=keyword)
#             )
#         else:
#             queryset = Product.objects.all()
#         return queryset

# views.py
# from rest_framework import generics
# from rest_framework import filters
# from django.db.models import Q
# from product.models import Product
# # from api.serializers.search import ProductSerializer
# from api.serializers.search import AllProductSerializer
# import jwt

# class ProductSearchAPIView(generics.ListAPIView):
#     serializer_class = AllProductSerializer
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['title', 'category__title', 'budclass__title']

#     def get_queryset(self):
#         keyword = self.request.query_params.get('keyword')
#         if keyword:
#             queryset = Product.objects.filter(
#                 Q(title__icontains=keyword) |
#                 Q(category__title__icontains=keyword) |
#                 Q(budclass__title__icontains=keyword)
#             )
#         else:
#             queryset = Product.objects.all()

#         # for product in queryset:
#         #     if product.category:
#         #         product.category = product.category.title
#         #     else:
#         #         product.category = None
#         return queryset
#     def get_serializer_context(self):
#         jwt_token = self.request.META.get("HTTP_AUTHORIZATION")
#         jwt_token = jwt_token.split()[1]
#         try:
#             token_data = jwt.decode(jwt_token, options={"verify_signature": False})  # Disable signature verification for claims extraction
#             user_id = token_data.get("user_id")
#             username = token_data.get("username")
#             role = token_data.get("role")
#             # You can access other claims as needed

#             # Assuming "branch" is one of the claims, access it
#             branch = token_data.get("branch")

#             # Print the branch
#             print("Branch:", branch)
#         except jwt.ExpiredSignatureError:
#             print("Token has expired.")
#         except jwt.DecodeError:
#             print("Token is invalid.")
#         # Get the base context
#         context = super(ProductSearchAPIView, self).get_serializer_context()

#         # Add your custom context data here
#         context['branch'] = branch  # Replace with your actual branch data

#         return context

from rest_framework import generics
from rest_framework import filters
from django.db.models import Q
from product.models import Product
# from api.serializers.search import ProductSerializer
from api.serializers.search import AllProductSerializer
import jwt
from product.models import BranchStock
from django.db.models import OuterRef, Subquery, Sum

class ProductSearchAPIView(generics.ListAPIView):
    serializer_class = AllProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'category__title', 'budclass__title']

    def get_serializer_context(self):
        jwt_token = self.request.META.get("HTTP_AUTHORIZATION")
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
        # Get the base context
        context = super(ProductSearchAPIView, self).get_serializer_context()

        # Add your custom context data here
        context['branch'] = branch  # Replace with your actual branch data

        return context

    def get_queryset(self):
        jwt_token = self.request.META.get("HTTP_AUTHORIZATION")
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
        keyword = self.request.query_params.get('keyword')
        if keyword:
            # queryset = Product.objects.filter(
            #     Q(title__icontains=keyword) |
            #     Q(category__title__icontains=keyword) |
            #     Q(budclass__title__icontains=keyword)
            # )
            branchstock_quantity_subquery_all = BranchStock.objects.filter(
                product=OuterRef('pk'),
                branch=branch
            ).values('product').annotate(total_quantity=Sum('quantity')).values('total_quantity')[:1]

            queryset = Product.objects.annotate(branchstock_total_quantity=Subquery(branchstock_quantity_subquery_all)).filter(
                Q(title__icontains=keyword) |
                Q(category__title__icontains=keyword) |
                Q(budclass__title__icontains=keyword),
                is_deleted = False,
                branchstock_total_quantity__gt=0,
                is_billing_item=True

            )
        else:
            queryset = Product.objects.all()

        # for product in queryset:
        #     if product.category:
        #         product.category = product.category.title
        #     else:
        #         product.category = None
        return queryset
    

