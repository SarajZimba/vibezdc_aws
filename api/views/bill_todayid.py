# # views.py
# from rest_framework import generics
# from bill.models import Bill
# from api.serializers.bill_todayid import BillSerializer
# from rest_framework import status
# from rest_framework.response import Response

# class BillDetailView(generics.ListAPIView):
#     # queryset = Bill.objects.all()
#     serializer_class = BillSerializer
#     lookup_field = 'id'  # Assuming the URL parameter is 'id'

#     def get_queryset(self):
#         id = self.kwargs['id']  # Get the invoice_number from URL
#         queryset = Bill.objects.filter(id=id)
#         return queryset
    
#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

from rest_framework import generics
from bill.models import Bill
from api.serializers.bill_todayid import BillSerializer
from rest_framework import status
from rest_framework.response import Response

class BillDetailView(generics.RetrieveAPIView):
    serializer_class = BillSerializer
    lookup_field = 'id'  # Assuming the URL parameter is 'id'

    def get_queryset(self):
        return Bill.objects.all()
    
    def get_object(self):
        id = self.kwargs['id']
        return self.get_queryset().get(id=id)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


