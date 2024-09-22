from django.urls import path

from .views import expense_views, group_views, friend_views, user_views

app_name = "splittime"
urlpatterns = [
    # ex: /splittime
    path("", group_views.IndexView.as_view(), name="index"),
    # ex: /add_group
    path("add_group", group_views.add_group, name="add_group"),
    # ex: /splittime/group/5
    path("group/<int:pk>/", group_views.GroupDetailsView.as_view(), name="group_details"),
    # ex: /splittime/group/5/delete_group
    path("group/<int:pk>/delete_group", group_views.delete_group, name="delete_group"),
    # ex: /splittime/expense/5
    path("expense/<int:pk>/", expense_views.ExpenseDetailsView.as_view(), name="expense_details"),
    # ex: /splittime/group/5/add_expense
    path("group/<int:group_id>/add_expense", expense_views.add_expense, name="add_expense"),
    # ex" /splittime/group/5/add_member
    path("group/<int:group_id>/add_member", group_views.add_group_member, name="add_group_member"),
    path(
        "group/<int:group_id>/delete_group_member/<int:user_id>",
        group_views.delete_group_member,
        name="delete_group_member",
    ),
    # ex: /splittile/expense/5/delete_expense
    path("expense/<int:pk>/delete_expense", expense_views.delete_expense, name="delete_expense"),
    path("friends/", friend_views.FriendsView.as_view(), name="friends"),
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
]
