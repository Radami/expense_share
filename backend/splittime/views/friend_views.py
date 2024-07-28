from typing import Any
from django.views import generic

from ..models import GroupMembership


class FriendsView(generic.ListView):

    template_name = "splittime/friends.html"

    def get_queryset(self):
        """Returns empy as everything is populated by get_context_data"""
        return []

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        gm = GroupMembership.objects.filter(member=self.request.user)
        groups = [g.group for g in gm]
        friends = []
        for g in groups:
            memberships = GroupMembership.objects.filter(group=g)
        for m in memberships:
            if m.member.id != self.request.user:
                friends.append(m.member)
        context = {
            "friends": friends
        }
        return context
