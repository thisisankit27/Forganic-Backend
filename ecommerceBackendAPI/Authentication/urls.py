from django.urls import path

from .views import UserDetailAPI, RegisterUserAPIView, LogoutView, ForgetPasswordView, VerifyEmail, VerifyEmailOTP
from .views import verify_otp

urlpatterns = [
    path('get-details/', UserDetailAPI.as_view(), name="get-details"),
    path('register/', RegisterUserAPIView.as_view(), name='register'),
    path('verify-email/', VerifyEmail.as_view(), name='verify-email'),
    path('verify-email-otp/', VerifyEmailOTP.as_view(), name='verify-email'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('forget-password/', ForgetPasswordView.as_view(), name='forget-password'),
    path('verify-otp/', verify_otp, name='verify-otp'),
]
