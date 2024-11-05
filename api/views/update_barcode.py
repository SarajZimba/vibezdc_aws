# views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from product.models import Product

class ProductBarcodeUpdate(APIView):
    def put(self, request, id, barcode, format=None):
        try:
            product = Product.objects.get(id=id)
            print(product)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        # Update the barcode field of the product
        product.barcode = barcode
        product.save()

        return Response({'message': 'Barcode updated successfully'}, status=status.HTTP_200_OK)
