from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import TokenAuthentication

from .models import VerifiedEmail


class CustomTokenAuthentication(TokenAuthentication):
    def authenticate_credentials(self, key):
        user, token = super().authenticate_credentials(key)

        try:
            flag = VerifiedEmail.objects.get(user=user)
            if not flag.verified:
                raise AuthenticationFailed("User's email is not verified.")
        except VerifiedEmail.DoesNotExist:
            raise AuthenticationFailed("User's email is not verified.")

        return user, token
