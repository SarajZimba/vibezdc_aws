


from rest_framework import generics
from bill.models import Bill, BillPayment
from django.db.models import Sum
from api.serializers.give_all_bills import BillSerializer,PaymentModeSerializer
from rest_framework import status
from rest_framework.response import Response


from django.db.models import Sum, DecimalField
from decimal import Decimal
from django.db.models.functions import Cast
from product.models import Product
from django.db.models import Q, Sum, Case, When, Value, F, CharField
from django.db.models.functions import Coalesce
from rest_framework_simplejwt.authentication import JWTAuthentication
import jwt
from organization.models import Branch

class BillDetailView(generics.ListAPIView):
    serializer_class = BillSerializer  # Assuming the URL parameter is 'id'

    # def get_queryset(self):
    #     queryset = Bill.objects.filter(is_end_day=False)
    #     queryset1 = Bill.objects.filter(is_end_day=False, status=True)

    #     return queryset, queryset1
        
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
            # print("Branch:", branch)
        except jwt.ExpiredSignatureError:
            print("Token has expired.")
        except jwt.DecodeError:
            print("Token is invalid.")
        print(branch)
        branch = Branch.objects.get(id=branch)
        terminal_id = self.kwargs.get("terminal_id", "1") 
        queryset = Bill.objects.filter(is_end_day=False, branch=branch, terminal=terminal_id)
        queryset1 = Bill.objects.filter(is_end_day=False, status=True, branch=branch, terminal=terminal_id)

        return queryset, queryset1

    def list(self, request, *args, **kwargs):
        queryset, queryset1 = self.get_queryset()

        # Get the IDs of bills with is_end_day=False
        bill_ids = queryset1.values_list('id', flat=True)

        possible_payment_modes = ["CASH", "CREDIT", "COMPLIMENTARY", "CREDIT CARD", "MOBILE PAYMENT"]

        # Initialize a dictionary to store the payment mode totals
        payment_mode_totals = {mode: Decimal(0.0) for mode in possible_payment_modes}

        # Get the total amount for each payment mode
        bill_payments = BillPayment.objects.filter(bill_id__in=bill_ids)

        for payment in bill_payments:
            # Update the total for each payment mode
            payment_mode_totals[payment.payment_mode] += payment.amount

        # Create a list of payment mode data
        payment_mode_data = [
            {"payment_mode": mode, "total_amount": payment_mode_totals[mode]}
            for mode in possible_payment_modes
        ]


        # Calculate the invoice_number and grand_total for void bills
        void_bills_data = queryset.filter(status=False).values('invoice_number', 'grand_total')

        # Serialize the payment_mode_data
        payment_mode_serializer = PaymentModeSerializer(payment_mode_data, many=True)
        first_bill = None
        last_bill = None

        for bill in queryset:
            if not first_bill and bill.invoice_number:
                first_bill = bill
            if bill.invoice_number:
                last_bill = bill

        # If no bill with a non-null invoice number is found for the last bill, use the last bill
        if last_bill is None:
            last_bill = queryset.last()

        starting_from_invoice = first_bill.invoice_number if first_bill else None
        ending_from_invoice = last_bill.invoice_number if last_bill else None

        
        # Serialize the queryset for bill data
        # serializer = self.get_serializer(queryset, many=True)

        # Calculate sums
        sub_total_sum = Decimal(0)
        discount_amount_sum = Decimal(0)
        taxable_amount_sum = Decimal(0)
        tax_amount_sum = Decimal(0)
        grand_total_sum = Decimal(0)
        service_charge_sum = Decimal(0)

        for bill in queryset1:
            # sub_total_sum += bill.sub_total
            # discount_amount_sum += bill.discount_amount
            # taxable_amount_sum += bill.taxable_amount
            # tax_amount_sum += bill.tax_amount
            # grand_total_sum += bill.grand_total
            # service_charge_sum += bill.service_charge
            if bill.payment_mode != 'COMPLIMENTARY':
                sub_total_sum += bill.sub_total
                discount_amount_sum += bill.discount_amount
                taxable_amount_sum += bill.taxable_amount
                tax_amount_sum += bill.tax_amount
                grand_total_sum += bill.grand_total
                service_charge_sum += bill.service_charge
        # # Serialize the queryset
        # serializer = self.get_serializer(queryset, many=True)
        bill_items_total = self.calculate_bill_items_total(queryset)

        serializer = self.get_serializer(queryset, many=True)

        # Create a response dictionary with "bill_data" key
        response_data = {
            "bill_data": serializer.data,
            "payment_modes": payment_mode_serializer.data,
            "Starting_from":starting_from_invoice,
            "Ending_from":ending_from_invoice,
            "bill_items_total": bill_items_total,
        }


        # Calculate and add the sales data to the response
        sales_data = {
            'discount_amount': discount_amount_sum,
            'taxable_amount': taxable_amount_sum,
            'tax_amount': tax_amount_sum,
            'grand_total': grand_total_sum,
            'service_charge': service_charge_sum,
        }
        response_data['Sales'] = sales_data

        # Add void bills data to the response
        response_data['void_bills'] = void_bills_data

        return Response(response_data, status=status.HTTP_200_OK)
    
    def calculate_bill_items_total(self, queryset):
            bill_items_total = []

            # Create a dictionary to store product quantities
            product_quantities = {}

            for bill in queryset:
                for bill_item in bill.bill_items.all():
                    product_id = bill_item.product.id
                    quantity = bill_item.product_quantity
                    rate = bill_item.rate
                  
                    product_title = bill_item.product_title

                    key = (product_id, rate)
                    if key in product_quantities:
                        product_quantities[key]['quantity'] += quantity
                    else:
                        product_quantities[key] = {
                        'quantity': quantity,
                        'rate': rate,
                        'product_title': product_title,
                    }

            # Convert the product quantities back to a list of dictionaries
            for product_id, item_data in product_quantities.items():
                # Find the associated product
                # product = Product.objects.get(id=product_id)
                # Create a dictionary for the bill item total
                bill_items_total.append({
                    'product_title': item_data['product_title'],
                    'product_quantity': item_data['quantity'],
                    'rate': item_data['rate'],
                    'amount': item_data['quantity'] * item_data['rate'],
                })

            return bill_items_total

