from typing import Any
from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import (
    HttpResponseRedirect,
    HttpResponseServerError,
    HttpResponseForbidden,
    HttpResponseNotFound,
)
from django.shortcuts import get_object_or_404
from django.views import generic
from django.urls import reverse
from django.utils import timezone

from ..models import Group, GroupMembership, Expense
from ..services.balances import BalanceCalculator
from ..services.groups import GroupService
from ..exceptions import DuplicateEntryException


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = "splittime/index.html"
    context_object_name = "latest_group_list"

    def get_queryset(self):
        """Returns empy as everything is populated by get_context_data"""
        return []

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        creation_date = timezone.make_aware(
            datetime.now() - timedelta(days=365), timezone.get_current_timezone()
        )
        group_memberships = GroupMembership.objects.filter(member=self.request.user)
        # latest_group_list = Group.objects.filter(creator=self.request.user).filter(
        #   creation_date__gte=creation_date).order_by("-creation_date")[:5]
        latest_group_list = [
            gm.group
            for gm in group_memberships
            if gm.group.creation_date >= creation_date
        ]
        latest_group_list.sort(key=lambda x: x.creation_date, reverse=True)
        context = {"latest_group_list": latest_group_list}
        return context


class GroupDetailsView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = Group
    template_name = "splittime/group_details.html"

    def test_func(self):
        try:
            group = Group.objects.get(pk=self.kwargs["pk"])
        except ObjectDoesNotExist as e:
            return HttpResponseNotFound(e)
        return group.has_member(self.request.user)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(GroupDetailsView, self).get_context_data(**kwargs)
        group = Group.objects.get(pk=self.kwargs["pk"])
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


@login_required
def add_group(request):
    if request.method == "POST":
        group_data = {
            "name": request.POST["group_name"],
            "description": request.POST["group_description"],
            "creator": request.user,
        }
        group = Group()
        try:
            group = GroupService.add_group(group_data)
        except Exception as e:
            return HttpResponseServerError(e)
        return HttpResponseRedirect(
            reverse("splittime:group_details", args=(group.id,))
        )
    return HttpResponseRedirect(
        reverse(
            "splittime:index",
        )
    )


@login_required
def delete_group(request, pk):
    if request.method == "POST":
        group = get_object_or_404(Group, pk=pk)

        if group.creator.id != request.user.id:
            return HttpResponseForbidden()

        try:
            GroupService.delete_group(group)
        except Exception as e:
            return HttpResponseServerError(e)
    return HttpResponseRedirect(reverse("splittime:index"))


@login_required
def add_group_member(request, group_id):
    user = get_object_or_404(User, email=request.POST["member_email"])
    group = get_object_or_404(Group, pk=group_id)

    if not group.has_member(request.user):
        return HttpResponseForbidden()
    try:
        GroupService.add_group_member(group, user)
    except Exception as e:
        if type(e) is DuplicateEntryException:
            # messages.add_message(request, messages.INFO, "Member already added")
            return HttpResponseRedirect(
                reverse("splittime:group_details", args=(group.id,))
            )
        return HttpResponseServerError(e)
    return HttpResponseRedirect(reverse("splittime:group_details", args=(group.id,)))


@login_required
def delete_group_member(request, group_id, user_id):
    user = get_object_or_404(User, pk=user_id)
    group = get_object_or_404(Group, pk=group_id)
    gm = get_object_or_404(GroupMembership, member=user, group=group)

    if not group.has_member(request.user):
        return HttpResponseForbidden()
    try:
        GroupService.delete_group_member(gm)
    except Exception as e:
        return HttpResponseServerError(e)

    return HttpResponseRedirect(reverse("splittime:group_details", args=(group.id,)))
