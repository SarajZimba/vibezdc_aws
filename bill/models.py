from datetime import datetime
from decimal import Decimal
from django.contrib.auth import get_user_model


from django.db import models
from django.dispatch import receiver
from organization.models import Organization, Branch
from product.models import Product, ProductStock
from root.utils import BaseModel
from django.db.models.signals import post_save
from .utils import product_sold, create_journal_for_complimentary, create_journal_for_bill


User = get_user_model()


class TblTaxEntry(models.Model):
    idtbltaxEntry = models.AutoField(primary_key=True)
    fiscal_year = models.CharField(max_length=20)
    bill_no = models.CharField(null=True, max_length=20)
    customer_name = models.CharField(max_length=200, null=True)
    customer_pan = models.CharField(max_length=200, null=True)
    bill_date = models.DateField(null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    taxable_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_printed = models.CharField(max_length=20, default="Yes")
    is_active = models.CharField(max_length=20, default="Yes")
    printed_time = models.CharField(null=True, max_length=20)
    entered_by = models.CharField(null=True, max_length=20)
    printed_by = models.CharField(null=True, max_length=20)
    is_realtime = models.CharField(max_length=20, default="Yes")
    sync_with_ird = models.CharField(max_length=20, default="Yes")
    payment_method = models.CharField(null=True, max_length=20, default="Cash")
    vat_refund_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    transaction_id = models.CharField(null=True, max_length=20)
    unit = models.CharField(default="-", max_length=20)

    class Meta:
        db_table = "tbltaxentry"

    def __str__(self):
        return f"{self.idtbltaxEntry}- {self.fiscal_year} - {self.bill_no}"


class TblSalesEntry(models.Model):
    tblSalesEntry = models.AutoField(primary_key=True)
    bill_date = models.CharField(null=True, max_length=20)
    bill_no = models.CharField(null=True, max_length=20)
    customer_name = models.CharField(max_length=200, null=True)
    customer_pan = models.CharField(max_length=200, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    NoTaxSales = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ZeroTaxSales = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    taxable_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    miti = models.CharField(null=True, max_length=20)
    ServicedItem = models.CharField(max_length=20, default="Goods")
    quantity = models.PositiveIntegerField(default=1)
    exemptedSales = models.CharField(default="0", max_length=20)
    export = models.CharField(default="0", max_length=20)
    exportCountry = models.CharField(default="0", max_length=20)
    exportNumber = models.CharField(default="0", max_length=20)
    exportDate = models.CharField(default="0", max_length=20)
    unit = models.CharField(default="-", max_length=20)

    class Meta:
        db_table = "tblSalesEntry"

    def __str__(self):
        return f"{self.tblSalesEntry}- {self.bill_date} - {self.bill_no}"


class TablReturnEntry(models.Model):
    idtblreturnEntry = models.AutoField(primary_key=True)
    bill_date = models.CharField(null=True, max_length=20)
    bill_no = models.CharField(null=True, max_length=20)
    customer_name = models.CharField(max_length=200, null=True)
    customer_pan = models.CharField(max_length=200, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    NoTaxSales = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    ZeroTaxSales = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    taxable_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    miti = models.CharField(null=True, max_length=20)
    ServicedItem = models.CharField(max_length=20, default="Goods")
    quantity = models.PositiveIntegerField(default=1)
    reason = models.TextField(null=True, blank=True)
    exemptedSales = models.CharField(default="0", max_length=20)
    export = models.CharField(default="0", max_length=20)
    exportCountry = models.CharField(default="0", max_length=20)
    exportNumber = models.CharField(default="0", max_length=20)
    exportDate = models.CharField(default="0", max_length=20)
    unit = models.CharField(default="-", max_length=20)

    class Meta:
        db_table = "tblreturnentry"

    def __str__(self):
        return f"{self.idtblreturnEntry}- {self.bill_date} - {self.bill_no}"


class PaymentType(BaseModel):
    title = models.CharField(max_length=255, verbose_name="Payment Type Title")
    description = models.TextField(null=True, verbose_name="Payment Type Description")
    icon = models.ImageField(upload_to="payment-type/icons/", null=True, blank=True)
    slug = models.SlugField(unique=True, verbose_name="Payment Type Slug")

    def __str__(self):
        return self.title 


class BillItem(BaseModel):
    agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product_title = models.CharField(
        max_length=255, verbose_name="Product Title", null=True
    )
    product_quantity = models.PositiveBigIntegerField(default=1)
    rate = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    unit_title = models.CharField(max_length=50, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_taxable = models.BooleanField(default=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.product_title}"

''' Signal for Decresing Product Stock after Sold '''

# def update_stock(sender, instance, **kwargs):
#     stock = ProductStock.objects.get(product=instance.product)
#     try:
#         stock.stock_quantity = stock.stock_quantity - int(instance.product_quantity)
#         stock.save()
#     except Exception as e:
#         print(e)
#     product_sold(instance=instance)
    

# post_save.connect(update_stock, sender=BillItem)

""" **************************************** """

class Bill(BaseModel):
    fiscal_year = models.CharField(max_length=20)
    agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    agent_name = models.CharField(max_length=255, null=True)
    terminal = models.CharField(max_length=10, default="1")
    customer_name = models.CharField(max_length=255, null=True, blank=True)
    customer_address = models.CharField(max_length=255, null=True, blank=True)
    customer_tax_number = models.CharField(max_length=255, null=True, blank=True)
    customer = models.ForeignKey("user.Customer", on_delete=models.SET_NULL, null=True)
    transaction_date_time = models.DateTimeField(auto_now_add=True)
    transaction_date = models.DateField(auto_now_add=True)

    transaction_miti = models.CharField(max_length=255, null=True, blank=True)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    taxable_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    service_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    invoice_number = models.CharField(max_length=255, null=True, blank=True)
    amount_in_words = models.TextField(null=True, blank=True)
    payment_mode = models.CharField(
        max_length=255, default="Cash", blank=True, null=True
    )

    bill_items = models.ManyToManyField(BillItem, blank=False)
    organization = models.ForeignKey(
        "organization.Organization", on_delete=models.SET_NULL, null=True
    )
    branch = models.ForeignKey(
        "organization.Branch", on_delete=models.SET_NULL, null=True
    )
    print_count = models.PositiveIntegerField(default=1)
    # is_taxable = models.BooleanField(default=True)
    bill_count_number = models.PositiveIntegerField(blank=True, null=True, db_index=True)   
    is_end_day = models.BooleanField(default=False)
    discount_reason = models.CharField(max_length=255, null=True, blank=True)



    class Meta:
        unique_together = 'invoice_number', 'fiscal_year', 'branch'

    def __str__(self):
        return f"{self.customer_name}-{self.transaction_date}- {self.grand_total}"

@receiver(post_save, sender=Bill)
def create_invoice_number(sender, instance, created, **kwargs):
    current_fiscal_year = Organization.objects.last().current_fiscal_year

    if created and not instance.payment_mode.lower() == "complimentary":
        branch = instance.branch.branch_code
        terminal = instance.terminal

        bill_number = 0 
        invoice_number = ""
    
        instance.fiscal_year = current_fiscal_year
        if terminal == 1:
            last_bill = Bill.objects.filter(terminal=terminal, fiscal_year = current_fiscal_year, branch=instance.branch).order_by('-bill_count_number').first()
            if not last_bill:
                bill_number = 1
            else:
                bill_number = last_bill.bill_count_number + 1

            if branch is not None:
                invoice_number = f"{branch}-{terminal}-{bill_number}"
            else:
                invoice_number = f"{terminal}-{bill_number}"
            
            instance.invoice_number = invoice_number
      
            instance.bill_count_number=bill_number
        else:
            invoice_number = instance.invoice_number
        

        a = TblTaxEntry(
            fiscal_year=current_fiscal_year,
            bill_no=invoice_number,
            customer_name=instance.customer_name,
            customer_pan=instance.customer_tax_number,
            bill_date=instance.transaction_date,
            amount=instance.grand_total,
            taxable_amount=instance.taxable_amount,
            tax_amount=instance.tax_amount,
            is_printed="Yes",
            printed_time=str(datetime.now().time().strftime(("%I:%M %p"))),
            entered_by=instance.agent_name,
            printed_by=instance.agent_name,
            is_realtime="Yes",
            sync_with_ird="Yes",
            payment_method=instance.payment_mode,
            vat_refund_amount=0.0,
            transaction_id="-",
        )

        b = TblSalesEntry(
            bill_date=instance.transaction_date,
            customer_name=instance.customer_name,
            customer_pan=instance.customer_tax_number,
            amount=instance.grand_total,
            NoTaxSales=0.0,
            ZeroTaxSales=0.0,
            taxable_amount=instance.taxable_amount,
            tax_amount=instance.tax_amount,
            miti=instance.transaction_miti,
            ServicedItem="Goods",
            quantity=1.0,
            bill_no=invoice_number,
        )

        """
        Accounting Section to create Journals after Bill Create
        """
        try:
            create_journal_for_bill(instance)
        except Exception as e:
            pass
        # ___________________________________

        if instance.tax_amount == 0:
            a.exemptedSales = instance.sub_total
            b.exemptedSales = instance.sub_total

        b.save()

        a.save()
        instance.save()

    if created and instance.payment_mode.lower().strip() == "complimentary":
        instance.tax_amount = 0
        instance.taxable_amount = 0
        instance.discount_amount = 0
       
        instance.save()
        try:
            create_journal_for_complimentary(instance)
        except Exception as e:
            pass




class BillPayment(BaseModel):
    bill = models.ForeignKey(Bill, on_delete=models.PROTECT)
    payment_mode = models.CharField(max_length=100)
    rrn = models.CharField(max_length=100, null=True, blank=True)
    amount = models.DecimalField(max_digits=9, decimal_places=2, default=0)

    def __str__(self):
        return self.payment_mode
    
class ConflictBillNumber(BaseModel):
    invoice_number = models.CharField(max_length=50)

    def __str__(self):
        return self.invoice_number

class tbldeliveryhistory(BaseModel):
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    customer = models.ForeignKey("user.Customer", on_delete=models.SET_NULL, null=True, blank=True)
    deliveryDate = models.DateTimeField(null=True, blank=True)
    deliver_to = models.CharField(max_length=200, null=True, blank=True)
    special_request = models.CharField(max_length=200, null=True, blank=True)
    Current_state = models.CharField(max_length=200,default="Ordered")
    delivery_option = models.CharField(max_length=200, null=True, blank=True)
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, null=True, blank=True)
    bill_no = models.CharField(max_length=255, null=True, blank=True)

import environ
env = environ.Env(DEBUG=(bool, False))
from .utils import send_mail_to_recipents
from threading import Thread
from root.firebase import send_notification


class tbldelivery_details(BaseModel):
    deliveryHistoryid = models.ForeignKey(tbldeliveryhistory, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)

# @receiver(post_save, sender=tbldelivery_details)
# def send_delivery_received_email(sender, instance, created, **kwargs):
#     if created:
        
#         sender = env('EMAIL_HOST_USER')
#         mail_list = []
#         from organization.models import MailRecipient, MailSendRecord

#         recipients = MailRecipient.objects.filter(status=True)
#         for r in recipients:
#             mail_list.append(r.email)
#             MailSendRecord.objects.create(mail_recipient=r)
#         if mail_list:
#             sender_email = env('EMAIL_HOST_USER') # Update with your sender email
#             # recipients = ['recipient1@example.com', 'recipient2@example.com']  # Update with your recipient email list or retrieve dynamically
#             subject = 'Order Received Notification'
#             message = f"Dear recipient,\n\nThis is to notify you that the order for {instance.product.title} with quantity {int(instance.quantity)} has been received from customer {instance.deliveryHistoryid.customer.name}.\n\nThank you,\n{Organization.objects.first().org_name}"
        
#         # Send email asynchronously using threading to avoid blocking the request
#         Thread(target=send_mail_to_recipents, args=(subject, message, mail_list, sender_email)).start()



from django.core.mail import send_mail
def send_loyalty_points_email(instance):
    customer_email = instance.customer.email if instance.customer else None
    if customer_email:
        subject = 'Order Confirmation'
        customer = instance.customer.id
        from user.models import Customer
        updated_loyalty_customer = Customer.objects.get(id=customer)
        points = updated_loyalty_customer.loyalty_points
        print(f'Current loyalty points {points}')
        message = f'Hello {updated_loyalty_customer.name}, Your order has been confirmed.\n\nTotal Amount: {instance.grand_total}\n\nYour current Loyalty points -> {points} \n\nThank you for shopping with us!\n\nBest Regards,\n{Organization.objects.first().org_name}' 
        recipent_list = [updated_loyalty_customer.email]

        send_mail(subject, message, None, recipent_list)
        print("Mail Sent")

from user.models import UserBranchLogin
@receiver(post_save, sender=tbldeliveryhistory)
def send_delivery_notification(sender, instance, created, **kwargs):
    print("I am inside")
    if created:
        branch=Branch.objects.first()
        active_users = UserBranchLogin.objects.filter(branch=branch)
        
        if active_users:
            for user in active_users:
                token = user.device_token   
                # print(token)
                print(instance)
                # delivery_details = instance.tbldelivery_details_set.all()
                # print(delivery_details)
                final_msg = str("You have a new order.")

                if token is not None:
                    send_notification(token, "Delivery Received", final_msg)
                else:
                    print("The token is None")
                # else:
                #     print(f"No delivery_details found !!")
        else:
            print(f"No active users in the branch {branch}")