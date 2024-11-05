# # urls.py
# from django.urls import path
# from api.views.customer import BillDetailView, RedeemProduct

# urlpatterns = [
#     # Other URL patterns
#     path('customer-billshistory/<int:customer>/', BillDetailView.as_view(), name='bill-detail'),
#     path('product-redeem-customer/<int:customer>/<int:loyalty_id>/', RedeemProduct.as_view(), name='product-redeem')
# ]

# urls.py
from django.urls import path
from api.views.customer import BillDetailView, RedeemProduct

urlpatterns = [
    # Other URL patterns
    path('customer-billshistory/<int:customer>/', BillDetailView.as_view(), name='bill-detail'),
    path('product-redeem-customer/<int:customer>/', RedeemProduct.as_view(), name='product-redeem')
]
    