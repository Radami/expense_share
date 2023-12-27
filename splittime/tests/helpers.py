import datetime
from django.utils import timezone
from django.contrib.auth.models import User

from ..models import Group, GroupMembership


class GroupHelpers():

    def create_group(group_name="Default name",
                     group_description="Default description",
                     days=0,
                     creator=None):
        """
        Creates a group with the given description an published the number of
        days offset to now (negative for past, positive for future)
        """
        time = timezone.now() + datetime.timedelta(days=days)
        if creator is None:
            creator = User.objects.get(username='testuser')
        return Group.objects.create(name=group_name,
                                    creator=creator,
                                    description=group_description,
                                    creation_date=time)

    def add_user_to_group(group, user):
        """
        Add specified user to the group
        """
        gm = GroupMembership()
        gm.group = group
        gm.member = user
        gm.save()


class UserHelpers():

    def create_user(user_name="Default name",
                    user_email="user@email.com"):
        """
        Creates a new user that can be added to groups
        """
        return User.objects.create_user(username=user_name,
                                        email=user_email,
                                        password='glassonion123')
