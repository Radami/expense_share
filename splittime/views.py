from typing import Any
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404,render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from datetime import datetime, timedelta

from .models import Group, GroupMembership, Expense

class IndexView(generic.ListView):
    template_name = "splittime/index.html"
    context_object_name = "latest_group_list"

    def get_queryset(self):
        """Returns empy as everything is populated by get_context_data"""
        return []

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        creation_date = timezone.make_aware(datetime.now() - timedelta(days=365), timezone.get_current_timezone())
        latest_group_list = Group.objects.filter(creation_date__gte=creation_date).order_by("-creation_date")[:5]
        context = {
            "latest_group_list": latest_group_list
        }
        return context

class GroupDetailsView(generic.DetailView):
    model = Group
    template_name = "splittime/group_details.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(GroupDetailsView, self).get_context_data(**kwargs)
        group = Group.objects.get(pk=self.kwargs['pk'])
        group_memberships = GroupMembership.objects.filter(group=group)
        members = [gm.member.username for gm in group_memberships]

        expenses = Expense.objects.filter(group=group)
        context = {
            "group": group,
            "members": members,
            "expenses": expenses
        }
        return context
        
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
   
    return HttpResponseRedirect(reverse("splittime:group_details", args=(group_id,)))
