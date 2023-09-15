from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import CartItem
from .serializers import CartItemSerializer
from rest_framework.response import Response
from rest_framework import status


class AddToCartView(CreateAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RemoveFromCartView(DestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class ListCartView(ListAPIView):
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user_cart_items = CartItem.objects.filter(user=self.request.user)

        for cart_item in user_cart_items:
            # Calculate the delivery charge for each item
            # Modify this to get the user's address
            start_address = "Attarsuiya"
            # Modify this to get the seller's address
            end_address = "Gurugram"
            weight = 1  # Modify this to get the item's weight

            # Call the function to get the delivery price
            delivery_price = CartItem.get_delivery_price(
                start_address, end_address, weight)

            # Update the delivery_charge field for the cart item
            cart_item.delivery_charge = delivery_price
            cart_item.save()

        return user_cart_items


class UpdateCartItemQuantityView(UpdateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)

        if serializer.is_valid():
            # Only update 'comment' and 'rating' fields
            for attr, value in serializer.validated_data.items():
                if attr in ['quantity']:
                    setattr(instance, attr, value)

            instance.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
