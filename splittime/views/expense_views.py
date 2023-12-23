from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic

from ..models import Group, GroupMembership, Expense


class ExpenseDetailsView(generic.DetailView):
    model = Expense
    template_name = "splittime/expense_details.html"


def add_expense(request, group_id):
    group = get_object_or_404(Group, pk=group_id)

    expense = Expense()
    expense.name = request.POST["expense_name"]
    expense.currency = request.POST["expense_currency"]
    expense.amount = request.POST["expense_amount"]
    expense.group = group
    expense.save()
    return HttpResponseRedirect(reverse("splittime:group_details",
                                        args=(group_id,)))


def delete_expense(request, pk):
    expense = get_object_or_404(Expense, pk=pk)

    # Check if the user performing the delete is a member of the group, 
    # otherwise error
    group = expense.group
    memberships = GroupMembership.objects.filter(group=group)
    found = False
    for gm in memberships:
        if request.user == gm.member:
            found = True
    if found is False:
        raise PermissionDenied()

    expense.delete()

    return HttpResponseRedirect(reverse("splittime:group_details",
                                        args=(group.id,)))
