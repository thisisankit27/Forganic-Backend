from rest_framework import serializers
from .models import Item, Comments


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'
        extra_kwargs = {
            'name': {'required': True},
            'price': {'required': True},
            'description': {'required': True},
            'discount_amount': {'required': True},
            'availability': {'required': True},
        }


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'
        extra_kwargs = {
            'item_id': {'required': True},
            'comment': {'required': True},
            'rating': {'required': True},
        }
