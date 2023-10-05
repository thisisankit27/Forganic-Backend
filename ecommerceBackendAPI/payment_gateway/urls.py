from django.urls import path
from . import views

urlpatterns = [
    path('payment-gateway/', views.PaymentGatewayView.as_view(), name='payment_gateway'),
    path('payment-success/<str:payment_id>/', views.PaymentSuccessView.as_view(), name='payment_success'),
]
