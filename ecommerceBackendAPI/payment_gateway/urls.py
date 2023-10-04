from django.urls import path
from . import views

urlpatterns = [
    path('payment-gateway/', views.PaymentGatewayView.as_view(), name='payment_gateway'),
]
