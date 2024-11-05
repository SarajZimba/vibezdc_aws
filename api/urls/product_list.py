# urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views.product_list import ProductListViewSet

router = DefaultRouter()
router.register(r'products', ProductListViewSet, basename='category-products')

# urlpatterns = [
#     # ...
#     path('api/', include(router.urls)),
#     # ...
# ]

urlpatterns = [] + router.urls