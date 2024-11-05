from rest_framework import serializers
from product.models import Product, ProductCategory, BudClass, ProductStock, BranchStock

# class BudClassSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BudClass
#         fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    # straintypeid = serializers.SerializerMethodField()
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
    # budclass = BudClassSerializer()
    class Meta:
        model = Product
        # fields = '__all__'
        exclude = ['created_at', 'status', 'updated_at', 'is_deleted', 'sorting_order', 'product_id', 'budclass', 'image']
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
        # Remove the first "/" from the image URL
        # if 'image' in data and data['image']:
        #     data['image'] = data['image'].lstrip('/')
        if 'thumbnail' in data and data['thumbnail']:
            data['image'] = data['thumbnail'].lstrip('/')
        data['price'] = round(float(data['price']), 2)
        data['quantity'] = round(float(data['quantity']), 2)
        data['thc_content'] = round(float(data['thc_content']), 2)
        data['cbd_content'] = round(float(data['cbd_content']), 2)
        
        # if 'straintype' in data:
        #     data['category'] = data.pop('straintype')
        return data
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
        
    def get_stock_quantity(self, obj):
        try:
            product_stock = ProductStock.objects.get(product=obj)
            return product_stock.stock_quantity
        except ProductStock.DoesNotExist:
            return 0
        
    def get_tax_name(self, obj):
        return obj.taxbracket.title if obj.taxbracket else None
    
    def get_tax_percent(self, obj):
        return obj.taxbracket.tax_percent if obj.taxbracket else 0.0
    


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
    stock_quantity = serializers.SerializerMethodField()
    tax_name = serializers.SerializerMethodField()
    tax_percent = serializers.SerializerMethodField()
    # budclass = BudClassSerializer()
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
        
    # def get_stock_quantity(self, obj):
    #     try:
    #         product_stock = ProductStock.objects.get(product=obj)
    #         return product_stock.stock_quantity
    #     except ProductStock.DoesNotExist:
    #         return 0

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
        # Remove the first "/" from the image URL
        # if 'image' in data and data['image']:
        #     data['image'] = data['image'].lstrip('/')

        if 'thumbnail' in data and data['thumbnail']:
            data['image'] = data['thumbnail'].lstrip('/')
        data['price'] = round(float(data['price']), 2)
        data['quantity'] = round(float(data['quantity']), 2)
        data['thc_content'] = round(float(data['thc_content']), 2)
        data['cbd_content'] = round(float(data['cbd_content']), 2)
        # if 'straintype' in data:
        #     data['category'] = data.pop('straintype')
        return data
    def get_stock_quantity(self, obj):
        branch = self.context.get("branch")
        # print(branch)
        if branch:
            branchstock_data = BranchStock.objects.filter(product=obj, branch__id=int(branch)).values('quantity')
            total_quantity = sum(entry['quantity'] for entry in branchstock_data)
            return total_quantity
        return 0
    
class BudClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudClass
        exclude = ['slug', 'description', 'created_at', 'updated_at', 'status', 'is_featured', 'is_deleted', 'sorting_order']

    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Remove the first "/" from the image URL
       
         
        data['bag_1_price'] = round(float(data['bag_1_price']), 2)
        data['bag_2_price'] = round(float(data['bag_2_price']), 2)
        data['bag_3_price'] = round(float(data['bag_3_price']), 2)
        data['bag_4_price'] = round(float(data['bag_4_price']), 2)
        data['bag_5_price'] = round(float(data['bag_5_price']), 2)
        data['bag_6_price'] = round(float(data['bag_6_price']), 2)
        data['bag_7_price'] = round(float(data['bag_7_price']), 2)
        data['bag_8_price'] = round(float(data['bag_8_price']), 2)
       
        # if 'straintype' in data:
        #     data['category'] = data.pop('straintype')
        return data

from django.db.models import Sum

class CategoryProductSerializer(serializers.Serializer):
    # all = serializers.ListField(child=ProductSerializer(), source='products')
    # All = ProductSerializer(many=True)
    budclass_name = serializers.CharField()
    budclassid = serializers.IntegerField()
    # budclass_data = BudClassSerializer()
    products = ProductSerializer(many=True)



    def to_representation(self, instance):
        data = super().to_representation(instance)
        branch = self.context.get("branch")
        # print(branch)
        
        # data['all'] = data['products']
        
        # Rename 'category' to 'straintype' within each product entry
        for product in data['products']:
            if 'category' in product:
                product['straintype'] = product.pop('category')
        
        # for product in data['products']:
            # Replace 'product_id' and 'branch' with your actual keys
            product_id = product.get('id')
            
            # Get branchstock quantity for the product (you may use your logic)
            branchstock_quantity = self.get_branchstock_quantity(product_id, branch)
            
            # Add the 'branchstock_quantity' field to the product
            product['stock_quantity'] = branchstock_quantity

        return data

    def get_branchstock_quantity(self,product_id, branch):
        # Implement your logic to get branchstock_quantity for a specific product
        # You can use BranchStock or any other method as needed
        try:
            # Replace with your actual query
            branchstock_data = BranchStock.objects.filter(product__id=product_id, branch__id=int(branch))
            total_quantity = branchstock_data.aggregate(Sum('quantity'))['quantity__sum']
            return total_quantity if total_quantity is not None else 0
        except BranchStock.DoesNotExist:
            return 0
    


    


