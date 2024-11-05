# # # serializers.py
# # from rest_framework import serializers
# from product.models import Product

# # class ProductSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = Product
# #         fields = '__all__'

# from rest_framework import serializers

# class ProductSerializer(serializers.ModelSerializer):
#     straintype_title = serializers.SerializerMethodField()
#     budclass_name = serializers.SerializerMethodField()
#     budclass_id = serializers.SerializerMethodField()
#     bag_1_price = serializers.SerializerMethodField()
#     bag_2_price = serializers.SerializerMethodField()
#     bag_3_price = serializers.SerializerMethodField()
#     bag_4_price = serializers.SerializerMethodField()
#     bag_5_price = serializers.SerializerMethodField()
#     bag_6_price = serializers.SerializerMethodField()
#     bag_7_price = serializers.SerializerMethodField()
#     bag_8_price = serializers.SerializerMethodField()
#     class Meta:
#         model = Product
#         exclude = ['created_at', 'status', 'updated_at', 'is_deleted', 'sorting_order']

#     def get_bag_1_price(self, obj):
#         return obj.budclass.bag_1_price if obj.budclass else 0.0

#     def get_bag_2_price(self, obj):
#         return obj.budclass.bag_2_price if obj.budclass else 0.0

#     def get_bag_3_price(self, obj):
#         return obj.budclass.bag_3_price if obj.budclass else 0.0

#     def get_bag_4_price(self, obj):
#         return obj.budclass.bag_4_price if obj.budclass else 0.0

#     def get_bag_5_price(self, obj):
#         return obj.budclass.bag_5_price if obj.budclass else 0.0

#     def get_bag_6_price(self, obj):
#         return obj.budclass.bag_6_price if obj.budclass else 0.0

#     def get_bag_7_price(self, obj):
#         return obj.budclass.bag_7_price if obj.budclass else 0.0

#     def get_bag_8_price(self, obj):
#         return obj.budclass.bag_8_price if obj.budclass else 0.0

#     def get_straintype_title(self, obj):
#         if obj.category:
#             return obj.category.title
#         return None
#     def get_budclass_name(self, obj):
#         if obj.budclass:
#             return obj.budclass.title
#         return None
#     def get_budclass_id(self, obj):
#         if obj.budclass:
#             return obj.budclass.id
#         return None

#     def to_representation(self, instance):
#         data = super().to_representation(instance)
#         rename_fields = self.context.get('rename_fields', {})

#         # Rename 'category' to 'straintype'
#         if 'category' in data:
#             data['straintype'] = data.pop('category')

#         if 'price' in data:
#             data['price'] = round(float(data['price']), 2)

#         if 'quantity' in data:
#             data['quantity'] = round(float(data['quantity']), 2)


#         # Extract only the image filename

# # serializers.py
# from rest_framework import serializers
from product.models import Product

# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = '__all__'

from rest_framework import serializers
from product.models import Product, ProductCategory, BudClass, ProductStock, BranchStock
from decimal import Decimal
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
import jwt

# class ProductSerializer(serializers.ModelSerializer):
#     straintype_title = serializers.SerializerMethodField()
#     budclass_name = serializers.SerializerMethodField()
#     budclass_id = serializers.SerializerMethodField()
#     bag_1_price = serializers.SerializerMethodField()
#     bag_2_price = serializers.SerializerMethodField()
#     bag_3_price = serializers.SerializerMethodField()
#     bag_4_price = serializers.SerializerMethodField()
#     bag_5_price = serializers.SerializerMethodField()
#     bag_6_price = serializers.SerializerMethodField()
#     bag_7_price = serializers.SerializerMethodField()
#     bag_8_price = serializers.SerializerMethodField()

#     class Meta:
#         model = Product
#         exclude = ['created_at', 'status', 'updated_at', 'is_deleted', 'sorting_order']

#     def get_bag_1_price(self, obj):
#         return obj.budclass.bag_1_price if obj.budclass else 0.0

#     def get_bag_2_price(self, obj):
#         return obj.budclass.bag_2_price if obj.budclass else 0.0

#     def get_bag_3_price(self, obj):
#         return obj.budclass.bag_3_price if obj.budclass else 0.0

#     def get_bag_4_price(self, obj):
#         return obj.budclass.bag_4_price if obj.budclass else 0.0

#     def get_bag_5_price(self, obj):
#         return obj.budclass.bag_5_price if obj.budclass else 0.0

#     def get_bag_6_price(self, obj):
#         return obj.budclass.bag_6_price if obj.budclass else 0.0

#     def get_bag_7_price(self, obj):
#         return obj.budclass.bag_7_price if obj.budclass else 0.0

#     def get_bag_8_price(self, obj):
#         return obj.budclass.bag_8_price if obj.budclass else 0.0

#     def get_straintype_title(self, obj):
#         if obj.category:
#             return obj.category.title
#         return None
#     def get_budclass_name(self, obj):
#         if obj.budclass:
#             return obj.budclass.title
#         return None
#     def get_budclass_id(self, obj):
#         if obj.budclass:
#             return obj.budclass.id
#         return None 
    

#     def to_representation(self, instance):
#         data = super().to_representation(instance)
#         rename_fields = self.context.get('rename_fields', {})

#         # Rename 'category' to 'straintype'
#         if 'category' in data:
#             data['straintype'] = data.pop('category')

#         if 'price' in data:
#             data['price'] = round(float(data['price']), 2)

#         if 'quantity' in data:
#             data['quantity'] = round(float(data['quantity']), 2)


#         # Extract only the image filename
#         # if 'image' in data:
#         #     data['image'] = data['image'].split('/')
#         # if 'image' in data:
#         #     data['image'] = self.context['request'].build_absolute_uri(data['image'])
#         # if 'image' in data:
#         #     image_url_parts = data['image'].split('/')
#         #     data['image'] = '/'.join(image_url_parts[3:])

#         return data

class AllProductSerializer(serializers.ModelSerializer):
    straintype_title = serializers.SerializerMethodField()
    budclass_name = serializers.SerializerMethodField()
    budclass_id = serializers.SerializerMethodField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2, coerce_to_string=False) 
    bag_1_price = serializers.SerializerMethodField()
    bag_2_price = serializers.SerializerMethodField()
    bag_3_price = serializers.SerializerMethodField()
    bag_4_price = serializers.SerializerMethodField()
    bag_5_price = serializers.SerializerMethodField()
    bag_6_price = serializers.SerializerMethodField()
    bag_7_price = serializers.SerializerMethodField()
    bag_8_price = serializers.SerializerMethodField()
    tax_name = serializers.SerializerMethodField()
    tax_percent = serializers.SerializerMethodField()
    stock_quantity = serializers.SerializerMethodField()

    class Meta:
        model = Product
        # fields = '__all__'
        exclude = ['created_at', 'status', 'updated_at', 'is_deleted', 'sorting_order', 'product_id', 'budclass', 'image']

    def get_bag_1_price(self, obj):
        return obj.budclass.bag_1_price if obj.budclass else 0.0

    def get_bag_2_price(self, obj):
        return obj.budclass.bag_2_price if obj.budclass else 0.0

    def get_bag_3_price(self, obj):
        return obj.budclass.bag_3_price if obj.budclass else 0.0

    def get_bag_4_price(self, obj):
        return obj.budclass.bag_4_price if obj.budclass else 0.0

    def get_bag_5_price(self, obj):
        return obj.budclass.bag_5_price if obj.budclass else 0.0

    def get_bag_6_price(self, obj):
        return obj.budclass.bag_6_price if obj.budclass else 0.0

    def get_bag_7_price(self, obj):
        return obj.budclass.bag_7_price if obj.budclass else 0.0

    def get_bag_8_price(self, obj):
        return obj.budclass.bag_8_price if obj.budclass else 0.0

    def get_tax_name(self, obj):
        return obj.taxbracket.title if obj.taxbracket else None
    
    def get_tax_percent(self, obj):
        return obj.taxbracket.tax_percent if obj.taxbracket else 0.0

    def get_straintypeid(self, obj):
        # Assuming you have a ForeignKey from Product to ProductCategory named 'category'
        if obj.category:
            return obj.category.id
        return None
    
    def get_straintype_title(self, obj):
        if obj.category:
            return obj.category.title
        return None

    def get_budclass_name(self, obj):
        # Assuming you have a ForeignKey from Product to BudClass named 'budclass'
        if obj.budclass:
            return obj.budclass.title
        return None
    
    def get_budclass_id(self, obj):
        if obj.budclass:
            return obj.budclass.id
        return None
    

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # if 'image' in data and data['image']:
        #     image_url = data['image']
        #     base_url = self.context.get('request').build_absolute_uri('/')
        #     if image_url.startswith(base_url):
        #         data['image'] = image_url[len(base_url):]

        if 'thumbnail' in data and data['thumbnail']:
            thumbnail_url = data['thumbnail']
            base_url = self.context.get('request').build_absolute_uri('/')
            if thumbnail_url.startswith(base_url):
                data['image'] = thumbnail_url[len(base_url):]

        # if 'image' in data:
        #     image_url_parts = data['image'].split('/')
        #     data['image'] = '/'.join(image_url_parts[3:])

        if 'price' in data and data['price']:

            if isinstance(data['price'], (float, Decimal)):
                data['price'] = round(float(data['price']), 2)

        data['quantity'] = round(float(data['quantity']), 2)
        data['thc_content'] = round(float(data['price']), 2)
        data['cbd_content'] = round(float(data['quantity']), 2)

        return data
    def get_stock_quantity(self, obj):
        branch = self.context.get("branch")
        print(branch)
        if branch:
            branchstock_data = BranchStock.objects.filter(product=obj, branch__id=int(branch)).values('quantity')
            total_quantity = sum(entry['quantity'] for entry in branchstock_data)
            return total_quantity
        return 0
#         # if 'image' in data:
#         #     data['image'] = data['image'].split('/')
#         # if 'image' in data:
#         #     data['image'] = self.context['request'].build_absolute_uri(data['image'])
#         if 'image' in data:
#             image_url_parts = data['image'].split('/')
#             data['image'] = '/'.join(image_url_parts[3:])

#         return data
