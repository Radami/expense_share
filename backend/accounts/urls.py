from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenVerifyView
from .views import CookieTokenObtainPairView, CookieTokenRefreshView

app_name = "users"
urlpatterns = [
    path("api/token/", CookieTokenObtainPairView.as_view(), name="token_obtain"),
    path("api/token/refresh", CookieTokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify", TokenVerifyView.as_view(), name="token_verify"),
    path("api/profile/", views.ProfileView.as_view(), name="get_user_profile"),
    path("api/users/", views.UserCreate.as_view(), name="account_create"),
]
