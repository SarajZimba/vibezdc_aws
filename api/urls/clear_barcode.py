from django.urls import path
from api.views.clear_barcode import ProductUpdateView

urlpatterns = [
    # Other URL patterns...
    path('clear-barcode/<int:product_id>/', ProductUpdateView.as_view(), name='clear-barcode'),
]
