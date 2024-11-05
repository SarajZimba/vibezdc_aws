# urls.py
from django.urls import path
from api.views.bill_reprint import BillDetailView

urlpatterns = [
    # Other URL patterns
    path('bill-reprint/<str:invoice_number>/', BillDetailView.as_view(), name='bill-detail'),
]
