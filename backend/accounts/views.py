from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse


class UserCreate(APIView):
    """
    Creates the user.
    """

    def post(self, request, format="json"):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)


class CookieTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access = response.data.get("access")
            refresh = response.data.get("refresh")

            cookie_response = JsonResponse({"message": "Login successful"})

            cookie_response.set_cookie(
                key="access_token",
                value=access,
                httponly=True,
                secure=False,  # switch to True in production
                samesite="Lax",
                max_age=60 * 60 * 24 * 7,
            )

            cookie_response.set_cookie(
                key="refresh_token",
                value=refresh,
                httponly=True,
                secure=False,
                samesite="Lax",
                max_age=60 * 60 * 24 * 7,
            )
            return cookie_response
        return response


class CookieTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        access = serializer.validated_data["access"]
        response = JsonResponse({"message": "Token refreshed"})
        response.set_cookie(
            key="access_token",
            value=access,
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=60 * 60 * 24 * 7,
        )
        return response


class CookieTokenInvalidateView(TokenBlacklistView):
    def post(self, request, *args, **kwargs):
        response = JsonResponse({"message": "Logged out successfully"})

        # Get refresh token from cookies
        refresh_token_str = request.COOKIES.get("refresh_token")

        if refresh_token_str:
            try:
                # Only blacklist the refresh token
                refresh_token = RefreshToken(refresh_token_str)
                refresh_token.blacklist()
            except (TokenError, InvalidToken) as e:
                print(f"Error blacklisting refresh token: {e}")
        else:
            print("No refresh token found in cookies for logout.")

        # Always clear both cookies regardless of blacklist success
        response.set_cookie(
            key="access_token",
            value="",
            httponly=True,
            secure=False,  # Match your cookie settings
            samesite="Lax",
            max_age=0,  # Expire immediately
        )

        response.set_cookie(
            key="refresh_token",
            value="",
            httponly=True,
            secure=False,  # Match your cookie settings
            samesite="Lax",
            max_age=0,  # Expire immediately
        )

        return response
