# urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views.get_product import CategoryProductViewSet

router = DefaultRouter()
router.register(r'category-products', CategoryProductViewSet, basename='category-products')

# urlpatterns = [
#     # ...
#     path('api/', include(router.urls)),
#     # ...
# ]

urlpatterns = [] + router.urls