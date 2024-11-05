from django.forms import ValidationError
from rest_framework.response import Response
from api.serializers.product import (
    CustomerProductDetailSerializer,
    CustomerProductSerializer,
    ProductSerializer,
    BulkItemReconcilationApiItemSerializer
)
from rest_framework.views import APIView

from rest_framework.generics import ListAPIView, RetrieveAPIView

from product.models import CustomerProduct, Product,ProductMultiprice, BranchStock, ItemReconcilationApiItem
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
import json
from django.shortcuts import get_object_or_404
from organization.models import Branch



class ProductMultipriceapi(ListAPIView):
    def get(self, request):
        try:
            products_list = Product.objects.all().values(
        "id",
        "title",
        "slug",
        "description",
        "image",
        "price",
        "is_taxable",
        "product_id",
        "unit",
        "category",
        "barcode"
        )
            temp_data = products_list
            for index,item in enumerate(products_list):
                print(item["id"])
                queryset = ProductMultiprice.objects.filter(product_id=item["id"]).values()
                temp_data[index]["multiprice"]=queryset
            return Response(temp_data,200)

        except Exception as error:
            return Response({"message":str(error)})






class ProductList(ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = None

    def get_queryset(self):
        return Product.objects.active()


class ProductDetail(RetrieveAPIView):
    serializer_class = ProductSerializer
    lookup_field = "pk"

    def get_queryset(self):
        return Product.objects.active()


class CustomerProductAPI(ModelViewSet):
    serializer_class = CustomerProductSerializer
    queryset = CustomerProduct.objects.active()

    def create(
        self,
        request,
        *args,
        **kwargs,
    ):

        is_added = CustomerProduct.objects.filter(
            is_deleted=False,
            status=True,
            customer=request.data["customer"],
            product=request.data["product"],
        )

        if not is_added:
            return super().create(request, *args, **kwargs)
        else:
            return Response(
                {"message": "This product is already added to the customer"},
            )

    def get_queryset(self, *args, **kwargs):
        customer_id = self.request.query_params.get("customerId")
        if customer_id:
            queryset = CustomerProduct.objects.filter(
                is_deleted=False, status=True, customer=customer_id
            )

            return queryset
        else:
            return super().get_queryset()

    def get_serializer_class(self):
        detail_actions = ["retrieve", "list"]
        if self.action in detail_actions:
            return CustomerProductDetailSerializer
        return super().get_serializer_class()


@api_view(['POST'])
@permission_classes([AllowAny])
def bulk_product_requisition(request):
    data = request.data.get('data', None)
    if data:
        data = json.loads(data)
        for d in data:
            quantity = int(d['quantity'])
            BranchStock.objects.create(branch_id=d['branch_id'], product_id=d['product_id'], quantity=quantity)
        return Response({'detail':'ok'}, 201)
    return Response({'detail':'Invalid data'}, 400)



from organization.models import EndDayRecord, EndDayDailyReport
from datetime import date
from bill.models import Bill
class ApiItemReconcilationView(APIView):

    def post(self, request):
        serializer = BulkItemReconcilationApiItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        EndDayRecord.objects.create(branch_id = serializer.validated_data.get('branch'),
                                     terminal=serializer.validated_data.get('terminal'),
                                     date = serializer.validated_data.get('date')
                                     )
        report_total = serializer.validated_data.get("report_total")
        new_data = {'branch_id':serializer.validated_data.get('branch'),'terminal':serializer.validated_data.get('terminal'), **report_total}
        EndDayDailyReport.objects.create(**new_data)

        # Update is_end_day status for relevant Bill objects
        Bill.objects.filter(branch_id=serializer.validated_data.get('branch'), terminal=serializer.validated_data.get('terminal'), is_end_day=False).update(is_end_day=True)
        return Response({'details':'success'}, 201)
    
class CheckAllowReconcilationView(APIView):

    def get(self, request):
        today_date = date.today()
        branch_id = request.GET.get('branch_id', None)
        if not branch_id:
            return Response({'detail':'Please provide branch_id in url params'}, 400)
        branch = get_object_or_404(Branch, pk=branch_id)
        if ItemReconcilationApiItem.objects.filter(date=today_date, branch = branch).exists():
            return Response({'detail':'Items already reconciled for today!! Please Contact Admin'}, 400)
        return Response({'details':'ok'}, 200)