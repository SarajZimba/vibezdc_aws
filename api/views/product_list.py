# views.py

from rest_framework import viewsets
from rest_framework.response import Response
from product.models import ProductCategory, Product
from api.serializers.product_list import ProductSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication


class ProductListViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]

    def list(self, request):
        # Retrieve all products and order them by the 'created_at' field in descending order
        products = Product.objects.all().order_by('-created_at')
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
