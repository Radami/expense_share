from typing import Any
from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import get_object_or_404
from django.views import generic
from django.urls import reverse
from django.utils import timezone

from ..models import Group, GroupMembership, Expense
from ..services.balances import BalanceCalculator
from ..services.groups import GroupService


class IndexView(generic.ListView):
    template_name = "splittime/index.html"
    context_object_name = "latest_group_list"

    def get_queryset(self):
        """Returns empy as everything is populated by get_context_data"""
        return []

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        creation_date = timezone.make_aware(
            datetime.now() - timedelta(days=365),
            timezone.get_current_timezone()
        )
        latest_group_list = Group.objects.filter(
            creation_date__gte=creation_date).order_by("-creation_date")[:5]
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

        expenses = Expense.objects.filter(group=group).order_by("creation_date")

        totals = {}
        for e in expenses:
            if e.currency not in totals:
                totals[e.currency] = e.amount
                continue
            totals[e.currency] += e.amount

        balances = BalanceCalculator.calculateBalances(group)

        context = {
            "group": group,
            "group_members": group_memberships,
            "expenses": expenses,
            "totals": totals,
            "balances": balances,
        }
        return context


def add_group(request):

    group_data = {
        "name": request.POST["group_name"],
        "description": request.POST["group_description"],
        "creator": request.user
    }
    group = Group()
    try:
        group = GroupService.add_group(group_data)
    except Exception as e:
        return HttpResponseServerError(e)
    return HttpResponseRedirect(reverse("splittime:group_details",
                                        args=(group.id,)))


def delete_group(request, pk):
    group = get_object_or_404(Group, pk=pk)

    if group.creator != request.user:
        raise PermissionDenied()

    try:
        GroupService.delete_group(group)
    except Exception as e:
        return HttpResponseServerError(e)

    return HttpResponseRedirect(reverse("splittime:index"))


def add_group_member(request, group_id):
    # TODO: add permission checks - only creator and members can add
    user = get_object_or_404(User, email=request.POST["member_email"])
    group = get_object_or_404(Group, pk=group_id)
    try:
        GroupService.add_group_member(group, user)
    except Exception as e:
        return HttpResponseServerError(e)
    return HttpResponseRedirect(reverse("splittime:group_details",
                                        args=(group.id,)))


def delete_group_member(request, group_id, user_id):
    # TODO: add permission checks - only creator and members can delete
    user = get_object_or_404(User, pk=user_id)
    group = get_object_or_404(Group, pk=group_id)
    gm = get_object_or_404(GroupMembership, member=user, group=group)

    try:
        GroupService.delete_group_member(gm)
    except Exception as e:
        return HttpResponseServerError(e)

    return HttpResponseRedirect(reverse("splittime:group_details",
                                        args=(group.id,)))
