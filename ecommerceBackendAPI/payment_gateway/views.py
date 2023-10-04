# import razorpay
# from django.conf import settings

# from Cart.models import CartItem

# def payment_gateway(request):
#     if request.method == 'POST':
#         user_cart_items = CartItem.objects.filter(user=request.user, is_payment_confirmed=False)
#         total_amount = 0
#         for cart_item in user_cart_items:
#             total_amount += cart_item.delivery_charge

#         client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))
#         order_params = {
#             'amount': total_amount * 100, # Razorpay expects amount in paisa, so multiply by 100
#             'currency': 'INR',
#             'payment_capture': 1,
#         }
#         payment = client.order.create(order_params)
#         context = {
#             'payment': payment,
#             'user_cart_items': user_cart_items
#         }
from rest_framework import views, status
from rest_framework.response import Response
from Cart.models import CartItem
from Cart.serializers import CartItemSerializer  # You need to create a serializer for CartItem
from rest_framework.permissions import IsAuthenticated
import math

import razorpay
from django.conf import settings

class PaymentGatewayView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_cart_items = CartItem.objects.filter(user=self.request.user, is_payment_confirmed=False)
        
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
                'delivery_charge': delivery_charge,
                'is_payment_confirmed': cart_item.is_payment_confirmed
            })

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        order_params = {
            'amount': math.ceil(total_amount),  # Razorpay expects amount in paisa, so multiply by 100
            'currency': 'INR',
            'payment_capture': 1,
        }

        try:
            payment = client.order.create(order_params)
        except razorpay.errors.BadRequestError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Assuming you have a serializer for CartItem
        cart_items_serializer = CartItemSerializer(user_cart_items, many=True)
        
        context = {
            'payment': payment,
            # 'user_cart_items': cart_items_serializer.data,
            'cart_items_prices': cart_items_prices,  # Include the list of item prices
        }

        return Response(context, status=status.HTTP_200_OK)
