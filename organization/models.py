from django.db import models
from root.utils import BaseModel, SingletonModel
from django.db.models.signals import post_save
from django.dispatch import receiver
import environ
env = environ.Env(DEBUG=(bool, False))

class StaticPage(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    content = models.TextField(null=True, blank=True)
    is_published = models.BooleanField(default=False)
    published_date = models.DateField(null=True, blank=True)
    keywords = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class Organization(SingletonModel, BaseModel):
    # basic company details
    org_name = models.CharField(max_length=255)
    org_logo = models.ImageField(
        upload_to="organization/images/", null=True, blank=True
    )
    tax_number = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="PAN/VAT Number"
    )
    website = models.URLField(null=True, blank=True)
    current_fiscal_year = models.CharField(null=True, max_length=20)
    start_year = models.IntegerField()
    end_year = models.IntegerField()
    # contact details
    company_contact_number = models.CharField(max_length=255, null=True, blank=True)
    company_contact_email = models.EmailField(null=True, blank=True)
    contact_person_name = models.CharField(max_length=255, null=True, blank=True)
    contact_person_number = models.CharField(max_length=255, null=True, blank=True)
    company_address = models.CharField(max_length=255, null=True, blank=True)
    company_bank_qr = models.ImageField(
        upload_to="organization/images/", null=True, blank=True
    )
    loyalty_percentage =models.DecimalField(max_digits=10, decimal_places=2, default=0)
    end_day_time = models.TimeField(null=True, blank=True)


    def __str__(self):
        return self.org_name
    
    def get_fiscal_year(self):
        return f'{self.start_year}-{self.end_year}'



from uuid import uuid4


def get_default_uuid():
    return uuid4().hex


class Branch(BaseModel):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True, blank=True)
    contact_number = models.CharField(max_length=50, null=True, blank=True)
    branch_manager = models.CharField(max_length=255, null=True, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    branch_code = models.CharField(
        max_length=255, null=False, blank=False, unique=True, default=get_default_uuid
    )
    is_central_billing = models.BooleanField(default=False, verbose_name='For Central Billing (Web)')

    def __str__(self):
        return f"{self.organization.org_name} - {self.name} Branch"

    # def save(self, *args, **kwargs):
    #     unique_id = shortuuid.ShortUUID().random(length=3)
    #     branch_char_list = [b[0].upper() for b in self.name.split()]
    #     branch_code = "".join(branch_char_list)
    #     self.branch_code = f"{branch_code}-{str(unique_id).upper()}"
    #     super(Branch, self).save(*args, **kwargs)

    # return super().save(*args, **kwargs)


class EndDayRecord(BaseModel):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    terminal = models.CharField(max_length=10)
    date = models.DateField()

    def __str__(self):
        return self.branch.name



class MailRecipient(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class MailSendRecord(models.Model):
    mail_recipient = models.ForeignKey(MailRecipient, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.mail_recipient.name


class EndDayDailyReport(BaseModel):
    employee_name = models.CharField(max_length=50)
    net_sales = models.FloatField()
    vat = models.FloatField()
    total_discounts = models.FloatField()
    cash = models.FloatField()
    credit = models.FloatField()
    credit_card = models.FloatField()
    mobile_payment = models.FloatField()
    complimentary = models.FloatField()
    start_bill = models.CharField(max_length=20)
    end_bill = models.CharField(max_length=20)
    date_time = models.CharField(max_length=100, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    terminal = models.CharField(max_length=10, null=True)
    total_sale = models.FloatField(default=0)

    def __str__(self):
        return 'Report'
    
    def save(self, *args, **kwargs):
        self.total_sale = self.net_sales + self.vat
        return super().save()

from .utils import send_mail_to_receipients
from threading import Thread
from datetime import datetime
from decimal import Decimal

@receiver(post_save, sender=EndDayDailyReport)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.employee_name != 'system':
            sender = env('EMAIL_HOST_USER')
            mail_list = []
            recipients = MailRecipient.objects.filter(status=True)
            for r in recipients:
                mail_list.append(r.email)
                MailSendRecord.objects.create(mail_recipient=r)
            if mail_list:
                dt_now = datetime.now()
                date_now = dt_now.date()
                time_now = dt_now.time().strftime('%I:%M %p')
                org = Organization.objects.first().org_name
                from bill.models import Bill
                bills = Bill.objects.filter(is_end_day=False, branch=instance.branch, terminal=instance.terminal)
                total_transactions = bills.count()
                total_grand_total_by_category = {}

                for bill in bills:
                    for bill_item in bill.bill_items.all():
                        product_category = bill_item.product.category.title

                        # Calculate tax_amount if the product is taxable
                        # if bill_item.product.is_taxable and bill_item.product.taxbracket:
                        #     tax_percent = Decimal(bill_item.product.taxbracket.tax_percent)
                        #     tax_amount = (bill_item.amount * tax_percent) / 100
                        # else:
                        #     tax_amount = 0

                        # Update the total_grand_total_by_category dictionary
                        total_grand_total_by_category[product_category] = (
                            total_grand_total_by_category.get(product_category, 0) + bill_item.amount 
                        )

                print(total_grand_total_by_category)
                report_data = {
                    'org_name':org,
                    'date_now': date_now,
                    'time_now': time_now,
                    'total_sale': instance.total_sale,
                    'date_time':instance.date_time,
                    'employee_name': instance.employee_name,
                    'net_sales': instance.net_sales,
                    'vat': instance.vat,  
                    'total_discounts': instance.total_discounts,
                    'cash': instance.cash,
                    'credit': instance.credit,
                    'credit_card': instance.credit_card,
                    'mobile_payment': instance.mobile_payment,
                    'complimentary': instance.complimentary,
                    'start_bill': instance.start_bill,
                    'end_bill': instance.end_bill,
                    'branch': instance.branch.name,
                    'terminal': instance.terminal,
                    'total_transactions': total_transactions,
                    'total_grand_total_by_category':total_grand_total_by_category,
                }
                Thread(target=send_mail_to_receipients, args=(report_data, mail_list, sender)).start()

        else:
            print("The endday was created by the system")

            