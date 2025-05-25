# accounts/authentication.py

from rest_framework_simplejwt.authentication import JWTAuthentication


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        print("Authenticating via cookie…")
        raw_token = request.COOKIES.get("access_token")
        print(request.COOKIES)
        if raw_token is None:
            print("No access token in cookies")
            return None

        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token
