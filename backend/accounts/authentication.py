from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import AccessToken


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        # First try to get the token from the cookie
        access_token = request.COOKIES.get(settings.SIMPLE_JWT["AUTH_COOKIE"])

        if access_token:
            try:
                validated_token = self.get_validated_token(access_token)
                return self.get_user(validated_token), validated_token
            except (InvalidToken, TokenError):
                pass

        # If cookie authentication fails, fall back to header-based authentication
        return super().authenticate(request)
