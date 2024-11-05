# from rest_framework import serializers
# from product.models import ProductPoints, Product
# from api.serializers.get_product import ProductSerializer


# class ProductpointSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Product
#         fields = ['id', 'title']
        
# class ProductPointsSerializer(serializers.ModelSerializer):
#     product = ProductpointSerializer()

#     points = serializers.DecimalField(max_digits=10, decimal_places=2, coerce_to_string=False)
#     class Meta:
#         model = ProductPoints
#         fields = ['id', 'product', 'points']

from rest_framework import serializers
from product.models import ProductPoints, Product, BranchStock

class ProductpointSerializer(serializers.ModelSerializer):


    class Meta:
        model = Product
        fields = ['id', 'title']



class ProductPointsSerializer(serializers.ModelSerializer):
    stock_quantity = serializers.SerializerMethodField()
    product = ProductpointSerializer()
    points = serializers.DecimalField(max_digits=10, decimal_places=2, coerce_to_string=False)

    class Meta:
        model = ProductPoints
        fields = ['id','product', 'points','stock_quantity']

    def get_stock_quantity(self, obj):
        branch = self.context.get("branch")
        print(branch)
        # print(obj.id)
        if branch:
            # Get the related ProductPoints instance
            # product = Product.objects.get(id=obj)
            # product_points_instance = ProductPoints.objects.get(product=obj.product)
            product_points_instance = ProductPoints.objects.filter(product=obj.product, is_deleted=False).first()
            
            if product_points_instance:


            # Use the related Product instance to calculate stock_quantity
                branchstock_data = BranchStock.objects.filter(product=product_points_instance.product, branch__id=int(branch)).values('quantity')
                total_quantity = sum(entry['quantity'] for entry in branchstock_data)
                return total_quantity

        return 0