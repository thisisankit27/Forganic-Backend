from rest_framework import serializers
from .models import ArticleModel
from our_product.models import Item


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArticleModel
        fields = '__all__'
