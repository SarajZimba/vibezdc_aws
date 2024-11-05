from django.urls import path
from api.views.give_product_points import ProductPointsList

urlpatterns = [
    path('product-points', ProductPointsList.as_view(), name='product-points-list' )
]