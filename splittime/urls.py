from django.urls import path

from .views import expense_views, group_views

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
    # ex: /splittile/expense/5/delete_expense
    path("expense/<int:pk>/delete_expense", expense_views.delete_expense, name="delete_expense"),
   
]