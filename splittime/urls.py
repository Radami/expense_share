from django.urls import path

from . import views

app_name = "splittime"
urlpatterns = [
    # ex: /splittime
    path("", views.index, name="index"),
    # ex: /splittime/group/5
    path("group/<int:group_id>/", views.group_details, name="group_details"),
    # ex: /splittime/expense/5
    path("expense/<int:group_id>/", views.expense_details),
    # es: /splittime/group/5/add_expense
    path("group/<int:group_id>/add_expese", views.add_expense)
]