from rest_framework import serializers
from .models import paymentCart

class paymentCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = paymentCart
        fields = '__all__'
        