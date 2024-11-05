from rest_framework import serializers
from bill.models import tbldeliveryhistory, tbldelivery_details
from .get_product import AllProductSerializer
from .user import CustomerSerializer

class DeliveryHistorySerializer(serializers.ModelSerializer):
    customer = CustomerSerializer() 
    class Meta:
        model = tbldeliveryhistory
        exclude = ['status', 'is_deleted', 'is_featured', 'sorting_order']
        
class DeliveryHistorySerializerNoCus(serializers.ModelSerializer):
    class Meta:
        model = tbldeliveryhistory
        exclude = ['status', 'is_deleted', 'is_featured', 'sorting_order']

class DeliveryDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = tbldelivery_details
        exclude = ['status', 'is_deleted', 'is_featured', 'sorting_order']

class DeliveryDetailsSerializer_combine(serializers.ModelSerializer):
    product = AllProductSerializer()
    class Meta:
        model = tbldelivery_details
        exclude = ['status', 'is_deleted', 'is_featured', 'sorting_order', "created_at", "updated_at", "id", "deliveryHistoryid"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Convert the 'quantity' field to an integer
        data['quantity'] = round(float(data['quantity']), 2)

        return data

class CustomerDeliveryHistorySerializer(serializers.ModelSerializer):
    customer = CustomerSerializer() 
    delivery_details = DeliveryDetailsSerializer(many=True, read_only=True, source='tbldelivery_details_set')

    class Meta:
        model = tbldeliveryhistory
        exclude = ['status', 'is_deleted', 'is_featured', 'sorting_order']

