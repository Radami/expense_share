from typing import Any
from django.views import generic
from django.utils import timezone
from datetime import datetime, timedelta
from django.http import HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.core.exceptions import PermissionDenied

from ..models import Group, GroupMembership, Expense

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
    
def add_group(request):
    try:
        group = Group()
        group.name = request.POST["group_name"]
        group.description = request.POST["group_description"]
        group.creation_date = datetime.now()
        group.creator = request.user

        group.save()

        gm = GroupMembership()
        gm.group = group
        gm.member = request.user
        gm.save()
    except():
        group.delete()
        gm.delete()
        return HttpResponseServerError()
    return HttpResponseRedirect(reverse("splittime:group_details", args=(group.id,)))

def delete_group(request, pk):
    group = get_object_or_404(Group, pk=pk)

    if group.creator != request.user:
         raise PermissionDenied()
    
    group.delete()

    return HttpResponseRedirect(reverse("splittime:index"))
