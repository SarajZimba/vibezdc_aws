# urls.py
from django.urls import path
from api.views.search import ProductSearchAPIView

urlpatterns = [
    # ... other URL patterns ...
    path('product/search/', ProductSearchAPIView.as_view(), name='product-search'),
]