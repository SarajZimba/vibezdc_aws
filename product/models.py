from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from root.utils import BaseModel
from user.models import Customer
from organization.models import Branch


class ProductCategory(BaseModel):
    title = models.CharField(max_length=255, verbose_name="Category Title", unique=True)
    slug = models.SlugField(verbose_name="Category Slug", null=True)
    description = models.TextField(
        verbose_name="Category Description", null=True, blank=True
    )

    def __str__(self):
        return self.title

    # def save(self, *args, **kwargs):
    #     self.title = self.title.lower()

    #     super().save(*args, **kwargs)
    
# class BudClass(BaseModel):
#     title = models.CharField(max_length=255, verbose_name="Bud Title", unique=True)
#     slug = models.SlugField(verbose_name="Bud Slug", null=True)
#     description = models.TextField(
#         verbose_name="Bud Description", null=True, blank=True
#     )

#     def __str__(self):
#         return self.title

class BudClass(BaseModel):
    title = models.CharField(max_length=255, verbose_name="Bud Title", unique=True)
    slug = models.SlugField(verbose_name="Bud Slug", null=True)
    description = models.TextField(
        verbose_name="Bud Description", null=True, blank=True
    )
    bag_1_price = models.FloatField(default=0.0)
    bag_2_price = models.FloatField(default=0.0)
    bag_3_price = models.FloatField(default=0.0)
    bag_4_price = models.FloatField(default=0.0)
    bag_5_price = models.FloatField(default=0.0)
    bag_6_price = models.FloatField(default=0.0)
    bag_7_price = models.FloatField(default=0.0)
    bag_8_price = models.FloatField(default=0.0)

    def __str__(self):
        return self.title
        
class TaxBracket(BaseModel):
    title = models.CharField(max_length=255, verbose_name="Tax Bracket", unique=True)
    slug = models.SlugField(verbose_name="Bud Slug", null=True)
    tax_percent = models.FloatField(default=0.0)
    description = models.TextField(
        verbose_name="Tax Description", null=True, blank=True
    )


    def __str__(self):
        return self.title

from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings
import os
class Product(BaseModel):
    title = models.CharField(max_length=255, verbose_name="Product Name", unique=True, db_index=True)
    slug = models.SlugField(verbose_name="Product Slug", null=True)
    description = models.TextField(
        null=True, blank=True, verbose_name="Product Description"
    )
    unit = models.CharField(null=True, max_length=100, blank=True)
    
    is_taxable = models.BooleanField(default=True)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    image = models.ImageField(upload_to="product/images/", null=True, blank=True)
    category = models.ForeignKey(
        ProductCategory, on_delete=models.CASCADE
    )
    budclass = models.ForeignKey(
        BudClass, on_delete=models.CASCADE
    )
    taxbracket = models.ForeignKey(
        TaxBracket, on_delete=models.CASCADE, null=True, blank=True
    )
    product_id = models.CharField(max_length=255, blank=True, null=True)
    barcode = models.CharField(null=True, max_length=100, blank=True)
    reconcile = models.BooleanField(default=False)
    is_billing_item = models.BooleanField(default=True)
    is_menu_item = models.BooleanField(default=True)
    is_produced = models.BooleanField(default=False)
    display_name = models.CharField(max_length=255, null=True, blank=True)
    # quantity = models.FloatField(default=0.0)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    thc_content = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cbd_content = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    reason = models.TextField(null=True, blank=True, verbose_name='Reason')
    bulk_price_applicable = models.BooleanField(default=False)
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)


    # product_image = models.ImageField(upload_to='product_images/', null=True, blank=True)

    
    @property
    def image_url(self):
        if self.image:
            return self.image.url
        else:
            return ""



    def __str__(self):
        return f"{self.title} - {self.category.title}"

    # def save(self, *args, **kwargs):
    #     # Check if is_taxable is False and there is a taxbracket selected
    #     if not self.is_taxable and self.taxbracket:
    #         self.taxbracket = None

    #     super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        # Check if is_taxable is False and there is a taxbracket selected
        if not self.is_taxable and self.taxbracket:
            self.taxbracket = None

        if not self.thumbnail:  # Only generate thumbnail if it doesn't exist
            self.thumbnail = self.generate_thumbnail()

        super().save(*args, **kwargs)

    def generate_thumbnail(self, thumbnail_size=(100, 100)):
        if self.image:
            image = Image.open(self.image)
            image.thumbnail(thumbnail_size)
            thumbnail_io = BytesIO()
            image.save(thumbnail_io, format='PNG')
            thumbnail_file = InMemoryUploadedFile(thumbnail_io, None, self.image.name.split('.')[0] + '_thumbnail.jpg', 'image/jpeg', thumbnail_io.tell(), None)
            thumbnail_file.seek(0)
            return thumbnail_file
        else:
            return None


class ProductStock(BaseModel):
    product = models.OneToOneField(Product, on_delete=models.PROTECT)
    stock_quantity = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f'{self.product.title} -> {self.stock_quantity}'


''' Signal to create ProductStock after Product instance is created '''


def create_stock(sender, instance, **kwargs):
    try:
        ProductStock.objects.create(product=instance)
    except Exception as e:
        print(e)

post_save.connect(create_stock, sender=Product)


"""      ***********************       """




from django.contrib.auth import get_user_model

User = get_user_model()

class ProductMultiprice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def __str__(self):
        return f"{self.product} - {self.product_price}"



class CustomerProduct(BaseModel):
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True
    )
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.product.title} - Rs. {self.price}"

class BranchStockTracking(BaseModel):
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    date = models.DateField()
    opening = models.IntegerField(default=0)
    received = models.IntegerField(default=0)
    wastage = models.IntegerField(default=0)
    returned = models.IntegerField(default=0)
    sold = models.IntegerField(default=0)
    closing = models.IntegerField(default=0)
    physical = models.IntegerField(default=0)
    discrepancy = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.title}"
    
    class Meta:
        unique_together = "branch", "product", "date"


class BranchStock(BaseModel):
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.product.title} to {self.branch.name}'
    
    # def save(self, *args, **kwargs):
    #     if ProductStock.objects.filter(product=self.product).exists():
    #         product = ProductStock.objects.get(product=self.product)
    #         product.stock_quantity -= self.quantity
    #         product.save()
    #     if self.quantity <= 0:
    #         # If the quantity is zero or negative, mark the entry as deleted
    #         self.is_deleted = True
    #     else:
    #         self.is_deleted = False

    #     super().save(*args, **kwargs)
    

class ItemReconcilationApiItem(BaseModel):
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    date = models.DateField()
    wastage = models.IntegerField(default=0)
    returned = models.IntegerField(default=0)
    physical = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.product.title} -> {self.branch.name}"
    
    class Meta:
        unique_together = 'branch', 'product', 'date'

class ProductPoints(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    points = models.DecimalField(max_digits=10, decimal_places=2, default=0)


    def __str__(self):
        return f"{self.product.title}"
        
class CustomerProductPointsTrack(BaseModel):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True
    )
    starting_points = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    points = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    action = models.CharField(null=True, blank=True, max_length=20)
    remaining_points = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bill_no = models.CharField(max_length=255, null=True, blank=True)