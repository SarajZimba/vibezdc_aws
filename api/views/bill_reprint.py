# views.py
from rest_framework import generics
from bill.models import Bill
from api.serializers.bill_reprint import BillSerializer
from rest_framework import status
from rest_framework.response import Response

class BillDetailView(generics.ListAPIView):
    # queryset = Bill.objects.all()
    serializer_class = BillSerializer
    lookup_field = 'invoice_number'  # Assuming the URL parameter is 'id'

    def get_queryset(self):
        invoice_number = self.kwargs['invoice_number']  # Get the invoice_number from URL
        queryset = Bill.objects.filter(invoice_number=invoice_number)
        return queryset
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

