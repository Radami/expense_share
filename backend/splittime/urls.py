from django.urls import path

from .views import expense_views, group_views, user_views

app_name = "splittime"
urlpatterns = [
    path("register", user_views.register_request, name="register"),
    path("login", user_views.login_request, name="login"),
    path("logout", user_views.logout_request, name="logout"),
    path("api/group_index", group_views.GroupIndexView.as_view(), name="api_index_view"),
    path("api/add_group", group_views.AddGroupView.as_view(), name="api_add_group"),
    path("api/delete_group", group_views.DeleteGroupView.as_view(), name="api_delete_group"),
    path(
        "api/group_details",
        group_views.GroupDetailsAPIView.as_view(),
        name="api_group_details_view",
    ),
    path(
        "api/delete_group_member",
        group_views.DeleteGroupMemberAPIView.as_view(),
        name="api_delete_group_member_view",
    ),
    path(
        "api/add_group_member",
        group_views.AddGroupMemberAPIView.as_view(),
        name="api_add_group_member_view",
    ),
    path(
        "api/add_group_expense",
        expense_views.AddExpenseAPIView.as_view(),
        name="api_add_group_expense_view",
    ),
    path(
        "api/delete_group_expense",
        expense_views.DeleteExpenseAPIView.as_view(),
        name="api_delete_group_expense_view",
    ),
]
