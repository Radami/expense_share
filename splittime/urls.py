from django.urls import path

from . import views

app_name = "splittime"
urlpatterns = [
    # ex: /splittime
    path("", views.IndexView.as_view(), name="index"),
    # ex: /splittime/group/5
    path("group/<int:pk>/", views.GroupDetailsView.as_view(), name="group_details"),
    # ex: /splittime/expense/5
    path("expense/<int:pk>/", views.ExpenseDetailsView.as_view(), name="expense_details"),
    # es: /splittime/group/5/add_expense
    path("group/<int:group_id>/add_expense", views.add_expense, name="add_expense")
]