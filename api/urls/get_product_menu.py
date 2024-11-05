# urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views.get_product_menu import CategoryProductViewSetMenu


router = DefaultRouter()
router.register(r'category-products-menu', CategoryProductViewSetMenu, basename='category-products-menu')

# urlpatterns = [
#     # ...
#     path('api/', include(router.urls)),
#     # ...
# ]

urlpatterns = [] + router.urls