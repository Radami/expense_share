import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

from splittime.services.groups import GroupService

from ..models import Expense, Group, GroupMembership
from ..services.expenses import ExpenseService


class GroupHelpers:

    seed = 1

    def create_group(
        group_name: str = None,
        group_description: str = None,
        days: int = 0,
        creator: User = None,
    ) -> Group:
        """
        Creates a group with the given description and published the number of
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

        group_data = {
            "name": group_name,
            "description": group_description,
            "creation_date": time,
            "creator": creator,
        }
        group = GroupService.add_group(group_data)
        return group

    def add_user_to_group(group: Group, user: User) -> None:
        GroupService.add_group_member(group, user)

    def add_expense(
        group: Group, payee: User, name: str = None, currency: str = "USD", amount: float = 100.0
    ) -> Expense:
        if group is None or payee is None:
            raise (Exception)
        memberships = GroupMembership.objects.filter(group=group)
        member_ids = [gm.member.id for gm in memberships]
        if payee.id not in member_ids:
            raise (Exception)
        if name is None:
            name = "Expense " + str(GroupHelpers.seed)

        expense = {
            "group": group,
            "name": name,
            "currency": currency,
            "amount": amount,
            "payee": payee,
        }
        return ExpenseService.add_expense(expense)

    def delete_expense(expense: Expense, user: User) -> None:
        ExpenseService.delete_expense(expense, user)


class UserHelpers:

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

        return User.objects.create_user(
            username=user_name, email=user_email, password="glassonion123"
        )

    @staticmethod
    def login_user(client, user):
        """
        Login a user and set the authentication cookies on the test client.
        """
        response = client.post(
            reverse("users:token_obtain"),
            {"username": user.username, "password": "glassonion123"},
        )
        assert response.status_code == 200, "Failed to obtain token"

        access_token = response.cookies.get("access_token")
        refresh_token = response.cookies.get("refresh_token")

        assert access_token is not None, "Access token not found in cookies"
        assert refresh_token is not None, "Refresh token not found in cookies"

        client.cookies["access_token"] = access_token
        client.cookies["refresh_token"] = refresh_token
        return client
