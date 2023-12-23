from django.urls import path

from . import views

app_name = "splittime"
urlpatterns = [
    # ex: /splittime
    path("", views.IndexView.as_view(), name="index"),
     # ex: /add_group
    path("add_group", views.add_group, name="add_group"),
    # ex: /splittime/group/5
    path("group/<int:pk>/", views.GroupDetailsView.as_view(), name="group_details"),
    # ex: /splittime/group/5/delete_group
    path("group/<int:pk>/delete_group", views.delete_group, name="delete_group"),
    # ex: /splittime/expense/5
    path("expense/<int:pk>/", views.ExpenseDetailsView.as_view(), name="expense_details"),
    # ex: /splittime/group/5/add_expense
    path("group/<int:group_id>/add_expense", views.add_expense, name="add_expense"),
   
]