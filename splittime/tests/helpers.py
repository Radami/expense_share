import datetime
from django.utils import timezone
from django.contrib.auth.models import User

from ..models import Group, GroupMembership, Expense, Debt


class GroupHelpers():

    seed = 1

    def create_group(group_name=None,
                     group_description=None,
                     days=0,
                     creator=None,):
        """
        Creates a group with the given description an published the number of
        days offset to now (negative for past, positive for future). If no name
        or description are provided, default ones + seed will be used
        """
        if group_name is None:
            group_name = "Group " + str(GroupHelpers.seed)
        if group_description is None:
            group_description = "Descrtiption for " + str(group_name)
        GroupHelpers.seed += 1

        time = timezone.now() + datetime.timedelta(days=days)
        if creator is None:
            creator = UserHelpers.create_user()
        group = Group.objects.create(name=group_name,
                                     creator=creator,
                                     description=group_description,
                                     creation_date=time)
        GroupHelpers.add_user_to_group(group, creator)
        return group

    def add_user_to_group(group, user):
        """
        Add specified user to the group
        """
        gm = GroupMembership()
        gm.group = group
        gm.member = user
        gm.save()

    def add_expense(group, payee, name=None, currency="USD", amount=100):
        if group is None or payee is None:
            raise (Exception)
        memberships = GroupMembership.objects.filter(group=group)
        member_ids = [gm.id for gm in memberships]
        if payee.id not in member_ids:
            raise (Exception)
        if name is None:
            name = "Expense " + str(GroupHelpers.seed)
        expense = Expense()
        expense.group = group
        expense.name = name
        expense.currency = currency
        expense.amount = amount
        expense.creation_date = timezone.now()
        expense.payee = payee
        expense.save()
        return expense


class UserHelpers():

    seed = 1

    def create_user(user_name=None, user_email=None):
        """
        Creates a new user that can be added to groups, If no username or email are
        provided, it will use default ones, with the seed appended
        """
        if user_name is None:
            user_name = "test_user" + str(UserHelpers.seed)
        if user_email is None:
            user_email = str(user_name) + str(UserHelpers.seed) + "@email.com"
        UserHelpers.seed += 1

        return User.objects.create_user(username=user_name,
                                        email=user_email,
                                        password='glassonion123')

