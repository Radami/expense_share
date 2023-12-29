from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from django.contrib.auth.models import User

from ..models import Group, GroupMembership, Expense, Debt


class ExpenseDetailsView(generic.DetailView):
    model = Expense
    template_name = "splittime/expense_details.html"


def add_expense(request, group_id):
    group = get_object_or_404(Group, pk=group_id)

    try:
        # Add an expense with the data from the POST request
        expense = Expense()
        expense.name = request.POST["expense_name"]
        expense.currency = request.POST["expense_currency"]
        expense.amount = request.POST["expense_amount"]
        expense.creation_date = timezone.now()
        expense.group = group
        payee_user = get_object_or_404(User, pk=request.POST["payee"])
        expense.payee = payee_user
        expense.save()

        # Add one debt relationship with each other member of the group
        members = GroupMembership.objects.filter(group=group)
        ratio = 1 / len(members) * 100
        for group_member in members:
            if group_member.member.id == payee_user.id:
                continue
            debt = Debt()
            debt.from_user = group_member.member
            debt.to_user = payee_user
            debt.expense = expense
            debt.ratio = ratio
            debt.save()
    except Exception as e:
        print(e)
        expense.delete()

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
