from django.db import IntegrityError
from django.utils import timezone

from ..models import Group, GroupMembership
from ..exceptions import DuplicateEntryException


class GroupService:
    def add_group(group_data):
        group = Group(
            name=group_data["name"],
            description=group_data["description"],
            creation_date=timezone.now(),
            creator=group_data["creator"],
        )
        gm = GroupMembership(group=group, member=group_data["creator"])

        try:
            group.save()
            gm.save()
        except Exception as e:
            print(e)
            group.delete()
            gm.delete()
            raise Exception(e)
        return group

    def delete_group(group):
        try:
            group.delete()
        except Exception as e:
            print(e)
            raise Exception(e)

    def add_group_member(group, user):
        gm = GroupMembership(group=group, member=user)
        try:
            gm.save()
        except Exception as e:
            if type(e) is IntegrityError:
                raise DuplicateEntryException
            raise Exception(e)

    def delete_group_member(group_membership):
        try:
            group_membership.delete()
        except Exception as e:
            print(e)
            raise Exception(e)
