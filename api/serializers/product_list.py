# serializers.py

from rest_framework import serializers
from product.models import Product, ProductCategory, BudClass

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
        # if 'straintype' in data:
        #     data['category'] = data.pop('straintype')
        if 'category' in data:
                data['straintype'] = data.pop('category')
        return data

class CategoryProductSerializer(serializers.Serializer):
    # straintype = serializers.CharField()
    # straintypeid = serializers.IntegerField()
    products = ProductSerializer(many=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        # Rename 'category' to 'straintype' within each product entry
        for product in data['products']:
            if 'category' in product:
                product['straintype'] = product.pop('category')
        
        return data