# urls.py

from django.urls import path
from api.views.update_barcode import ProductBarcodeUpdate

urlpatterns = [
    # ... Other URL patterns
    path('products/update-barcode/<int:id>/<str:barcode>/', ProductBarcodeUpdate.as_view(), name='product-update-barcode'),
]
