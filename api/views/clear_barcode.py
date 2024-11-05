from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from product.models import Product

class ProductUpdateView(APIView):
    def get(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            product.barcode = None  # Set the barcode to null
            product.save()
            return Response({'message': 'Barcode cleared successfully.'}, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)
    