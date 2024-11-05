# # views.py
# from rest_framework import generics, serializers
# from bill.models import Bill
# from api.serializers.customer import BillSerializer
# from rest_framework import status
# from rest_framework.response import Response
# from user.models import Customer
# import jwt
# from rest_framework.views import APIView
# from product.models import ProductPoints, CustomerProductPointsTrack, BranchStock

# class BillDetailView(generics.ListAPIView):
#     # queryset = Bill.objects.all()
#     serializer_class = BillSerializer
#     lookup_field = 'customer'  # Assuming the URL parameter is 'id'

#     def get_queryset(self):
#         customer = self.kwargs['customer']  # Get the invoice_number from URL
#         customer = Customer.objects.get(pk=customer)
#         queryset = Bill.objects.filter(customer=customer)
#         return queryset
    
#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

# class RedeemProduct(APIView):
#     def get(self, request, *args, **kwargs):
#         jwt_token = request.META.get("HTTP_AUTHORIZATION")
#         jwt_token = jwt_token.split()[1]
#         try:
#             token_data = jwt.decode(jwt_token, options={"verify_signature": False})
#             user_id = token_data.get("user_id")
#             branch = token_data.get("branch")
#         except jwt.ExpiredSignatureError:
#             print("Token has expired.")
#             return Response({"detail": "Token has expired."}, status=status.HTTP_401_UNAUTHORIZED)
#         except jwt.DecodeError:
#             print("Token is invalid.")
#             return Response({"detail": "Token is invalid."}, status=status.HTTP_401_UNAUTHORIZED)

#         # Convert the date parameter to a datetime object

#         # print(branch)

#         customer_id = kwargs.get('customer')
#         # product_id = kwargs.get('product')
#         loyalty_id = kwargs.get('loyalty_id')

#         # customer_id = validated_data.get('customer')
#         if customer_id is not None:
#             try:
#                 customer = Customer.objects.get(pk=customer_id)

#             except:
#                 raise serializers.ValidationError(f"Customer with id {customer_id} not found")
   
#             if loyalty_id is not None:
#                 try:
#                     product_for_points = ProductPoints.objects.get(pk=loyalty_id)
#                 except:
#                     raise serializers.ValidationError(f"Product Points with id {loyalty_id} not found")
#                 loyaltypoints_tobe_sub = product_for_points.points
#                 starting_points_redeem = customer.loyalty_points
#                 if loyaltypoints_tobe_sub is None:
#                     raise serializers.ValidationError("loyalty points cannot be null")
#                 if starting_points_redeem is None:
#                     raise serializers.ValidationError("customer loyalty points cannot be null")  
#                 if starting_points_redeem < loyaltypoints_tobe_sub:
#                     raise serializers.ValidationError("You do not have sufficient points to claim the reward")
#                 customer.loyalty_points -= loyaltypoints_tobe_sub
#                 customer.save()
#                 product_redeemed = product_for_points.product
#                 branchstock_entries = BranchStock.objects.filter(branch=branch, product=product_redeemed, is_deleted=False).order_by('quantity')

#                 quantity_decreased = False
#                 for branchstock in branchstock_entries:
#                         available_quantity = branchstock.quantity
#                         if available_quantity > 0 and not quantity_decreased:
#                             branchstock.quantity -= 1
#                             branchstock.save()
#                             quantity_decreased=True

#                 if quantity_decreased == False:
#                     raise serializers.ValidationError("The product redeemed has no stock quantities")
#                 CustomerProductPointsTrack.objects.create(customer=customer, starting_points=starting_points_redeem, points=loyaltypoints_tobe_sub, action="Redeem", remaining_points=customer.loyalty_points)

#         return Response({"reponse": "Product Redeemed Successfully" })

# views.py
from rest_framework import generics, serializers
from bill.models import Bill
from api.serializers.customer import BillSerializer
from rest_framework import status
from rest_framework.response import Response
from user.models import Customer
import jwt
from rest_framework.views import APIView
from product.models import ProductPoints, CustomerProductPointsTrack, BranchStock
from decimal import Decimal
from product.models import CustomerProductPointsTrack
from .user import CustomerSerializer

from rest_framework.response import Response
from rest_framework import status

class BillDetailView(generics.ListAPIView):
    # Your existing code...

    def get_queryset(self):
        customer = self.kwargs['customer']  # Get the customer ID from URL
        customer = Customer.objects.get(pk=customer)
        return Bill.objects.filter(customer=customer, status=True, is_deleted=False).order_by('-id')

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        customer = Customer.objects.get(pk=self.kwargs['customer'])
        print(customer)
        pointstrack = CustomerProductPointsTrack.objects.filter(is_deleted=False, status=True, customer=customer)

        sub_total_sum = Decimal(0)
        discount_amount_sum = Decimal(0)
        taxable_amount_sum = Decimal(0)
        tax_amount_sum = Decimal(0)
        grand_total_sum = Decimal(0)
        service_charge_sum = Decimal(0)
        no_of_bills = queryset.count()

        for bill in queryset:
            if bill.payment_mode != 'COMPLIMENTARY':
                sub_total_sum += bill.sub_total
                discount_amount_sum += bill.discount_amount
                taxable_amount_sum += bill.taxable_amount
                tax_amount_sum += bill.tax_amount
                grand_total_sum += bill.grand_total
                service_charge_sum += bill.service_charge

        total_redeemed_points = Decimal(0)
        total_rewarded_points = Decimal(0)
        for pointsobj in pointstrack:
            if pointsobj.action == 'Reward':
                total_rewarded_points += pointsobj.points
            if pointsobj.action == 'Redeem':
                total_redeemed_points += pointsobj.points
        
        sales_data = {
            'total_discount_sum': discount_amount_sum,
            'total_grand_total': grand_total_sum,
            'service_charge': service_charge_sum,
            'total_rewarded': total_rewarded_points,
            'total_redeemed': total_redeemed_points,
            'total_sales' : no_of_bills
        }
        
        response_data = {
            'customer': CustomerSerializer(customer).data,
            'bills': BillSerializer(queryset, many=True).data,
            'summary': sales_data
        }
        
        return Response(response_data, status=status.HTTP_200_OK)


class RedeemProduct(APIView):
    def post(self, request, *args, **kwargs):
        jwt_token = request.META.get("HTTP_AUTHORIZATION")
        jwt_token = jwt_token.split()[1]
        try:
            token_data = jwt.decode(jwt_token, options={"verify_signature": False})
            user_id = token_data.get("user_id")
            branch = token_data.get("branch")
        except jwt.ExpiredSignatureError:
            print("Token has expired.")
            return Response({"detail": "Token has expired."}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.DecodeError:
            print("Token is invalid.")
            return Response({"detail": "Token is invalid."}, status=status.HTTP_401_UNAUTHORIZED)

        # Convert the date parameter to a datetime object

        # print(branch)

        customer_id = kwargs.get('customer')
        # product_id = kwargs.get('product')
        loyalty_ids = request.data.get('loyalty_ids', [])

        if not loyalty_ids:
            serializers.ValidationError(f"No loyalty_ids have been provided")
        # customer_id = validated_data.get('customer')
            
        if customer_id is not None:
            try:
                customer = Customer.objects.get(pk=customer_id)
            except:
                raise serializers.ValidationError({"detail": f"Customer with id {customer_id} not found"})
        
        for loyalty_id in loyalty_ids:     
            if loyalty_id is not None:
                try:
                    product_for_points = ProductPoints.objects.get(pk=loyalty_id)
                except:
                    raise serializers.ValidationError({"detail":f"Product Points with id {loyalty_id} not found"})

                branchstock_entries = BranchStock.objects.filter(branch=branch, product=product_for_points.product, is_deleted=False).order_by('quantity')

                quantity_decreased = False
                for branchstock in branchstock_entries:
                        available_quantity = branchstock.quantity
                        if available_quantity > 0 and not quantity_decreased:
                            branchstock.quantity -= 1
                            branchstock.save()
                            quantity_decreased=True

                if quantity_decreased == False:
                    raise serializers.ValidationError({"detail":"The product redeemed has no stock quantities"})

                loyaltypoints_tobe_sub = product_for_points.points
                starting_points_redeem = customer.loyalty_points
                if loyaltypoints_tobe_sub is None:
                    raise serializers.ValidationError({"detail":"loyalty points cannot be null"})
                if starting_points_redeem is None:
                    raise serializers.ValidationError({"detail":"customer loyalty points cannot be null"})         
                if starting_points_redeem < loyaltypoints_tobe_sub:
                    raise serializers.ValidationError({"detail":"You do not have sufficient points to claim the reward"})
                customer.loyalty_points -= loyaltypoints_tobe_sub
                customer.save()
                CustomerProductPointsTrack.objects.create(customer=customer, starting_points=starting_points_redeem, points=loyaltypoints_tobe_sub, action="Redeem", remaining_points=customer.loyalty_points)




        return Response({"detail": "Product Redeemed Successfully" })