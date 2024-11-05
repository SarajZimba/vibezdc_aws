# myapp/management/commands/my_command.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from organization.models import Branch, Organization, EndDayDailyReport, EndDayRecord
from bill.models import Bill, BillPayment
from decimal import Decimal
from product.models import Product, ItemReconcilationApiItem

# from myapp.models import MyModel  # Import your models here if needed

class Command(BaseCommand):
    help = 'This is a sample management command'

    def handle(self, *args, **kwargs):
        # Your code to be executed goes here
        # Example: Fetch data from a model and print it
        # queryset = MyModel.objects.all()  # Replace MyModel with your actual model
        # for obj in queryset:
        #     self.stdout.write(self.style.SUCCESS(f'Object: {obj}'))
        current_datetime_ny = timezone.now()

        formatted_date = current_datetime_ny.strftime('%Y-%m-%d')
        formatted_datetime = current_datetime_ny.strftime('%Y-%m-%d %I:%M %p')
        print(f"The formatted time is {formatted_datetime}")
        branches = Branch.objects.all()

        bill_terminals = Bill.objects.filter(is_end_day=False)

        terminal_ids =[]

        for terminals in bill_terminals:
            if terminals.terminal not in terminal_ids:
                terminal_ids.append(terminals.terminal)

        print(f"terminals {terminal_ids}")

        # terminal_ids = ["5", "9"]

        for branch in branches:
            for terminal_id in terminal_ids:

                try:
                    queryset = Bill.objects.filter(is_end_day=False, branch=branch, terminal=terminal_id)
                except Exception as e:
                    print(f"The error occured in queryset {e}")

                try:
                    queryset1 = Bill.objects.filter(is_end_day=False, status=True, branch=branch, terminal=terminal_id)
                except:
                    print(f"The error occured in the queryset1 {e}")
            # def list(self, request, *args, **kwargs):
            #     queryset, queryset1 = self.get_queryset()

                # Get the IDs of bills with is_end_day=False
                    
                if queryset is not None and queryset1 is not None and queryset.exists() and queryset1.exists():
                    bill_ids = queryset1.values_list('id', flat=True)

                    possible_payment_modes = ["CASH", "CREDIT", "COMPLIMENTARY", "CREDIT CARD", "MOBILE PAYMENT"]

                    # Initialize a dictionary to store the payment mode totals
                    payment_mode_totals = {mode: Decimal(0.0) for mode in possible_payment_modes}

                    # Get the total amount for each payment mode
                    try:
                        bill_payments = BillPayment.objects.filter(bill_id__in=bill_ids)
                        print(bill_payments)
                    except Exception as e:
                        print(f"The error occured in the bill_payments {e}")
                        print(f"These are the bill ids", bill_ids)

                    if bill_payments is not None:
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
                    # payment_mode_serializer = PaymentModeSerializer(payment_mode_data, many=True)
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
        
                    # serializer = self.get_serializer(queryset, many=True)

                    # Create a response dictionary with "bill_data" key
                    response_data = {
                        "bill_data": queryset,
                        "payment_modes": payment_mode_data,
                        "Starting_from":starting_from_invoice,
                        "Ending_from":ending_from_invoice,
                        "bill_items_total": bill_items_total,
                    }

                    print("I have got the response_data", response_data)

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
                    
                    organization = Organization.objects.first()

                    organization = {

                    "org_name" : organization.org_name,
                    "tax_number" : organization.tax_number,
                    # contact details
                    "company_contact_number" : organization.company_contact_number,
                    # company_contact_email = models.EmailField(null=True, blank=True)
                    "company_address" : organization.company_address


                    }
                    
                    response_data["organization"] = organization


                    print("Cronjob activated successfully")

                    cash_total = 0.0
                    credit_total = 0.0
                    credit_card_total = 0.0
                    mobile_payment_total = 0.0
                    complimentary_total = 0.0

                    for mode in payment_mode_data:
                        if mode['payment_mode'] == 'CASH':
                            cash_total = mode['total_amount']
                        if mode['payment_mode'] == 'CREDIT':
                            credit_total = mode['total_amount']
                        if mode['payment_mode'] == 'CREDIT CARD':
                            credit_card_total = mode['total_amount']
                        if mode['payment_mode'] == 'MOBILE PAYMENT':
                            mobile_payment_total = mode['total_amount']
                        if mode['payment_mode'] == 'COMPLIMENTARY':
                            complimentary_total = mode['total_amount']

            
                    
                    try:
                        EndDayRecord.objects.create(branch_id =branch.id,
                                                terminal=terminal_id,
                                                date = formatted_date
                                                )

                    except Exception as e:
                        print("Error creating the Endday Record Object", e)


                    try:

                        EndDayDailyReport.objects.create(employee_name="system", net_sales=taxable_amount_sum, vat=tax_amount_sum, total_discounts=discount_amount_sum, cash=cash_total , credit=credit_total , credit_card=credit_card_total , mobile_payment=mobile_payment_total , complimentary=complimentary_total , start_bill=starting_from_invoice, end_bill=ending_from_invoice, date_time=formatted_datetime, terminal=terminal_id, total_sale = grand_total_sum , branch_id=branch.id)
                        print("The End Day object has been created")
                    except Exception as e :
                        print("Error creating the Endday Object", e)

                    # try:
                    #     products = Product.objects.filter(reconcile=True, is_deleted=False, status=True)

                    #     for product in products:
                    #         ItemReconcilationApiItem.objects.create(product=product, wastage=0, returned=0, physical=0, date = formatted_date, branch=branch)


                    # except Exception as e:
                    #     print("Error reconciling the items", e)
                    
                    try:
                        Bill.objects.filter(branch_id=branch, terminal=terminal_id, is_end_day=False).update(is_end_day=True)

                    except Exception as e:
                        print("Error in updating the bills")

                    # serializer = BulkItemReconcilationApiItemSerializer(data=request.data)
                    # serializer.is_valid(raise_exception=True)
                    # serializer.save()
                        


                    
                    # You can also perform any other tasks here
                    
                    # Finally, print a success message
                    self.stdout.write(self.style.SUCCESS('Command executed successfully at %s' % timezone.now()))
                else:
                    self.stdout.write(self.style.SUCCESS('Bills are not created %s' % timezone.now()))


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
