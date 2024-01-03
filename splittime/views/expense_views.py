from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from django.contrib.auth.models import User

from ..models import Group, Expense
from ..services.expenses import ExpenseService


class ExpenseDetailsView(generic.DetailView):
    model = Expense
    template_name = "splittime/expense_details.html"


def add_expense(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    payee = get_object_or_404(User, pk=request.POST["payee"])

    try:
        # Add an expense with the data from the POST request
        expense = {
            "name": request.POST["expense_name"],
            "currency": request.POST["expense_currency"],
            "amount": request.POST["expense_amount"],
            "creation_date": timezone.now(),
            "group": group,
            "payee": payee
        }
        ExpenseService.add_expense(expense)
    except Exception as e:
        print(e)
        return HttpResponseBadRequest(e)

    return HttpResponseRedirect(reverse("splittime:group_details",
                                        args=(group_id,)))


def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)

    # Check if the user performing the delete is a member of the group,
    # otherwise error
    try:
        ExpenseService.delete_expense(expense, request.user)
    except PermissionDenied as exception:
        return HttpResponseNotAllowed(exception)

    return HttpResponseRedirect(reverse("splittime:group_details",
                                        args=(expense.group.id,)))
