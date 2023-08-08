from rest_framework import serializers

from .models import *

class OrderListSerializer(serializers.ModelSerializer):

    products = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    
    class Meta:
        model = Order
        fields = ('date_of_created', 'net_weight', 'products')
        
    pass
