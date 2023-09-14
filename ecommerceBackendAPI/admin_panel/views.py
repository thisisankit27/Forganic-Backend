from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from our_product.models import Item
from our_product.serializers import ItemSerializer
from .permissions import CustomPermission


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [CustomPermission]
