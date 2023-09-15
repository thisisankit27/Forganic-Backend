from rest_framework import serializers
from .models import ItemDimensions

class ItemDimensionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemDimensions
        fields = '__all__'
        
        