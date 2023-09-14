from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import UserSerializer, RegisterSerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics

import pyotp
from django.core.mail import send_mail
from rest_framework.decorators import api_view
from rest_framework import status
from django.conf import settings
from .serializers import VerifyOTPSerializer, ForgetPasswordSerializer
import jwt


from .serializers import VerifiedEmailSerializer
from .models import VerifiedEmail
import logging

from .authentication import CustomTokenAuthentication


def generate_and_send_otp_email(email, subject='Your OTP', user_id=None):
    otp_secret = pyotp.random_base32()
    totp = pyotp.TOTP(otp_secret)
    otp = totp.now()

    subject = subject
    message = f'Your OTP is: {otp}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

    try:
        send_mail(subject, message, from_email,
                  recipient_list, fail_silently=False)
        return otp
    except Exception as e:
        error_message = f"Verification-Email sending error: {e}"
        logging.error(error_message)
        return None


class UserDetailAPI(APIView):
    authentication_classes = (CustomTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmail(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ForgetPasswordSerializer

    def post(self, request):
        serializer = ForgetPasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Get the email from the request data
            email = request.data.get('email')

            try:
                # Retrieve the user based on the provided email
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'error': 'User with this email does not exist.'}, status=400)

            # Generate JWT token with OTP and user data
            otp = generate_and_send_otp_email(
                user.email, 'Your OTP for Email Verification', user.id)

            jwt_data = {
                'user_id': user.id,
                'email': email,
                'otp': otp,
            }

            jwt_key = settings.JWT_KEY  # Access the JWT key from settings
            encrypted_token = jwt.encode(jwt_data, jwt_key, algorithm='HS256')

            # Send the encrypted token as a response
            return Response({'token': encrypted_token, 'message': 'OTP sent successfully.'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailOTP(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = VerifiedEmailSerializer

    def post(self, request, *args, **kwargs):
        serializer = VerifiedEmailSerializer(data=request.data)
        if serializer.is_valid():
            encrypted_token = serializer.validated_data.get('token')
            user_otp = serializer.validated_data.get('user_otp')
            jwt_key = settings.JWT_KEY

            try:
                jwt_data = jwt.decode(
                    encrypted_token, jwt_key, algorithms=['HS256'])

                user = User.objects.get(id=jwt_data['user_id'])

                if jwt_data['otp'] == user_otp:  # You can directly access the OTP from jwt_data
                    verification = VerifiedEmail.objects.create(
                        user=user, verified=True
                    )
                    verification.save()
                    return Response({'message': 'Email Verified successfully.'})
                else:
                    return Response({'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)
            except jwt.ExpiredSignatureError:
                otp = generate_and_send_otp_email(
                    user.email, 'Email Verification OTP', user.id)

                # Generate JWT token with OTP and user data
                jwt_data = {
                    'user_id': user.id,
                    'email': user.email,
                    'otp': otp,
                }

                jwt_key = settings.JWT_KEY  # Access the JWT key from settings
                encrypted_token = jwt.encode(
                    jwt_data, jwt_key, algorithm='HS256')

                # Send the encrypted token as a response
                response_data = {
                    'token': encrypted_token,
                    'message': 'Email-Verification OTP sent successfully.',
                    'serializer_data': serializer.data,
                    'error': 'Token has expired.',
                }
                return Response(response_data, status=status.HTTP_401)
            except jwt.InvalidTokenError:
                return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        # Invalidate the user's token to log them out
        request.auth.delete()
        return Response(status=status.HTTP_200_OK)


class ForgetPasswordView(APIView):
    def post(self, request):
        serializer = ForgetPasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Get the email from the request data
            email = request.data.get('email')

            try:
                # Retrieve the user based on the provided email
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'error': 'User with this email does not exist.'}, status=400)

            # Generate JWT token with OTP and user data
            otp = generate_and_send_otp_email(
                user.email, 'Your OTP for Password Reset')

            jwt_data = {
                'user_id': user.id,
                'email': email,
                'otp': otp,
            }

            jwt_key = settings.JWT_KEY  # Access the JWT key from settings
            encrypted_token = jwt.encode(jwt_data, jwt_key, algorithm='HS256')

            # Send the encrypted token as a response
            return Response({'token': encrypted_token, 'message': 'OTP sent successfully.'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Your new view for OTP verification


@api_view(['POST'])
def verify_otp(request):

    serializer = VerifyOTPSerializer(data=request.data)

    if serializer.is_valid():
        encrypted_token = serializer.validated_data.get('token')
        user_otp = serializer.validated_data.get('user_otp')
        new_password = serializer.validated_data.get('new_password')

        # Retrieve the JWT key from settings
        jwt_key = settings.JWT_KEY

        try:
            # Decode the JWT token
            jwt_data = jwt.decode(
                encrypted_token, jwt_key, algorithms=['HS256'])

            user = User.objects.get(id=jwt_data['user_id'])

            if jwt_data['otp'] == user_otp:
                # Reset the user's password
                user.set_password(new_password)
                user.save()
                return Response({'message': 'Password reset successfully.'})
            else:
                return Response({'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token has expired.'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.InvalidTokenError:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        # Return validation errors if the JSON format is unexpected
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
