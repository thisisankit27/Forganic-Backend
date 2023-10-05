from rest_framework import views, status
from rest_framework.response import Response
from Cart.models import CartItem
from .models import paymentCart
from Cart.serializers import CartItemSerializer  # You need to create a serializer for CartItem
from .serializers import paymentCartSerializer
from rest_framework.permissions import IsAuthenticated
import math

import razorpay
from django.conf import settings

class PaymentGatewayView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_cart_items = CartItem.objects.filter(user=self.request.user)
        
        total_amount = 0
        cart_items_prices = []  # List to store prices of each item

        for cart_item in user_cart_items:
            item_price = cart_item.item.price
            delivery_charge = cart_item.delivery_charge
            quantity = cart_item.quantity

            total_amount += delivery_charge + (quantity * item_price)
            
            # Store the price of each item in the list
            cart_items_prices.append({
                'id': cart_item.id,
                'item_id': cart_item.item.id,
                'item_name': cart_item.item.name,
                'item_price': item_price,
                'item_quantity': quantity,
                'item_total_price': quantity * item_price,
                'delivery_charge': delivery_charge
            })

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        order_params = {
            'amount': math.ceil(total_amount)*100,  # Razorpay expects amount in paisa, so multiply by 100
            'currency': 'INR',
            'payment_capture': 1,
        }

        try:
            payment = client.order.create(order_params)
        except razorpay.errors.BadRequestError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        cart_obj = paymentCart.objects.create(
            user=self.request.user,
            coupon=None,
            is_paid=False,
            razorpay_order_id=payment['id']
        )
        cart_obj.save()
        # Assuming you have a serializer for CartItem
        # cart_items_serializer = CartItemSerializer(user_cart_items, many=True)
        cart_obj_serializer = paymentCartSerializer(cart_obj)
        context = {
            'payment': payment,
            # 'user_cart_items': cart_items_serializer.data,
            'cart_items_prices': cart_items_prices,  # Include the list of item prices
            'paymentCart': cart_obj_serializer.data
        }

        return Response(context, status=status.HTTP_200_OK)

# def payment_success(request, payment_id):
#     order_id = request.GET.get('razorpay_order_id')
#     cart_obj = paymentCart.objects.filter(razorpay_order_id=order_id).first()
#     cart_obj.is_paid = True
#     cart_obj.save()
#     cart_items = CartItem.objects.filter(id__in=cart_obj.cartitem_set.values_list('id', flat=True))
#     return Response({'message': 'Payment successful'},status=status.HTTP_200_OK)

# https://razorpay.com/docs/payments/server-integration/python/payment-gateway/build-integration/
class PaymentSuccessView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, payment_id):
        # order_id = request.GET.get('razorpay_order_id')
        order_id = payment_id
        cart_obj = paymentCart.objects.filter(razorpay_order_id=order_id).first()

        if cart_obj:
            cart_obj.is_paid = True
            cart_obj.save()
            # You can include additional logic or update other models as needed.
            cart_items = CartItem.objects.filter(user=self.request.user)
            cart_items.delete()

            return Response({'message': 'Payment successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)