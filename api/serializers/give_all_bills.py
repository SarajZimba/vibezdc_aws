# serializers.py
from rest_framework import serializers
from bill.models import Bill, BillItem
from product.models import Product

class BillItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillItem
        exclude = [
            "created_at",
            "updated_at",
            "status",
            "is_deleted",
            "sorting_order",
            "is_featured",
            "unit_title",
            "is_taxable",
            "agent",
        ]
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Remove the first "/" from the image URL
       
        data['rate'] = round(float(data['rate']), 2)
        data['amount'] = round(float(data['amount']), 2)
        # if 'straintype' in data:
        #     data['category'] = data.pop('straintype')
        return data

class BillSerializer(serializers.ModelSerializer):
    # bill_items = BillItemSerializer(many=True)
    class Meta:
        model = Bill
        # exclude = [
        #     "created_at",
        #     "updated_at",
        #     "status",
        #     "is_deleted",
        #     "sorting_order",
        #     "is_featured",
        #     "transaction_miti"
        # ]

        fields = ['id','invoice_number', 'created_at', 'payment_mode', 'grand_total', 'status']

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # data['sub_total'] = round(float(data['sub_total']), 2)
        # data['discount_amount'] = round(float(data['discount_amount']), 2)
        # data['taxable_amount'] = round(float(data['taxable_amount']), 2)
        # data['tax_amount'] = round(float(data['tax_amount']), 2)
        data['grand_total'] = round(float(data['grand_total']), 2)
        # data['service_charge'] = round(float(data['service_charge']), 2)
        if  data['status'] == False:
            data['payment_mode'] = "VOID"

        return data
    
    # def get_bill_items_total(self, instance):
    #     bill_items = instance.bill_items.all()
    #     product_quantities = {}  # Dictionary to store product quantities

    #     for bill_item in bill_items:
    #         product_id = bill_item.product.id
    #         quantity = bill_item.product_quantity

    #         if product_id in product_quantities:
    #             product_quantities[product_id] += quantity
    #         else:
    #             product_quantities[product_id] = quantity

    #     # Convert the product quantities back to a list of dictionaries
    #     bill_items_total = []
    #     for product_id, quantity in product_quantities.items():
    #         # Find the associated product
    #         product = Product.objects.get(id=product_id)
    #         # Create a dictionary for the bill item
    #         bill_item_total = {
    #             'title': product.title,
    #             'quantity': quantity,
    #             'rate': product.rate,
    #             'amount': product.rate * quantity,
    #             'product': product_id,
    #         }
    #         bill_items_total.append(bill_item_total)

    #     return bill_items_total
    
class PaymentModeSerializer(serializers.Serializer):
    payment_mode = serializers.CharField()
    total_amount = serializers.DecimalField(max_digits=9, decimal_places=2, coerce_to_string=False)
    




