from django.urls import reverse
from rest_framework.test import APITestCase

from ..helpers import GroupHelpers, UserHelpers


class GroupDetailsAPITest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.creator = UserHelpers.create_user(user_name="creator_details")
        cls.member = UserHelpers.create_user(user_name="member_details")
        cls.old_group = GroupHelpers.create_group(days=-400, creator=cls.creator)
        cls.new_group = GroupHelpers.create_group(days=-5, creator=cls.creator)
        GroupHelpers.add_user_to_group(cls.old_group, cls.member)

    def setUp(self):
        UserHelpers.login_user(self.client, self.creator)

    def test_no_group(self):
        data = {"group_id": 1234}
        response = self.client.get(reverse("splittime:api_group_details_view"), data=data)
        self.assertEqual(response.status_code, 404)

    def test_old_group(self):
        data = {"group_id": self.old_group.id}
        response = self.client.get(reverse("splittime:api_group_details_view"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.old_group.name)

    def test_recent_group(self):
        data = {"group_id": self.new_group.id}
        response = self.client.get(reverse("splittime:api_group_details_view"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.new_group.name)

    def test_group_creator_displayed_as_member(self):
        data = {"group_id": self.old_group.id}
        response = self.client.get(reverse("splittime:api_group_details_view"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.old_group.name)
        self.assertContains(response, "group_members")
        self.assertContains(response, self.creator.username)
        self.assertContains(response, self.member.username)


class GroupDetailsWithExpensesTests(APITestCase):
    """Exercises serializer expense, totals, and balance amount paths"""

    @classmethod
    def setUpTestData(cls):
        cls.creator = UserHelpers.create_user(user_name="details_exp_creator")
        cls.member = UserHelpers.create_user(user_name="details_exp_member")
        cls.group = GroupHelpers.create_group(creator=cls.creator)
        GroupHelpers.add_user_to_group(cls.group, cls.member)
        cls.expense1 = GroupHelpers.add_expense(
            cls.group, cls.creator, name="Exp A", currency="USD", amount=100.0
        )
        cls.expense2 = GroupHelpers.add_expense(
            cls.group, cls.creator, name="Exp B", currency="USD", amount=200.0
        )

    def test_member_has_non_zero_user_owes(self):
        """member owes creator for both expenses — user_owes is not 'Nothing'"""
        UserHelpers.login_user(self.client, self.member)
        response = self.client.get(
            reverse("splittime:api_group_details_view"),
            data={"group_id": self.group.id},
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data["user_owes"], "Nothing")

    def test_creator_has_non_zero_user_is_owed(self):
        """creator is owed by member — user_is_owed is not 'Nothing'"""
        UserHelpers.login_user(self.client, self.creator)
        response = self.client.get(
            reverse("splittime:api_group_details_view"),
            data={"group_id": self.group.id},
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data["user_is_owed"], "Nothing")

    def test_expenses_list_includes_you_owe_for_member(self):
        """Each expense shows a non-zero you_owe for the non-paying member"""
        UserHelpers.login_user(self.client, self.member)
        response = self.client.get(
            reverse("splittime:api_group_details_view"),
            data={"group_id": self.group.id},
        )
        self.assertEqual(response.status_code, 200)
        expenses = response.data["expenses"]
        self.assertEqual(len(expenses), 2)
        for expense in expenses:
            self.assertGreater(expense["you_owe"], 0)

    def test_totals_accumulate_same_currency(self):
        """Two USD expenses sum correctly in totals"""
        UserHelpers.login_user(self.client, self.creator)
        response = self.client.get(
            reverse("splittime:api_group_details_view"),
            data={"group_id": self.group.id},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("USD", response.data["totals"])
        self.assertAlmostEqual(response.data["totals"]["USD"], 300.0, places=2)


class GroupDetailsAPIViewPermissionTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.creator = UserHelpers.create_user(user_name="creator_details_perm")
        cls.outsider = UserHelpers.create_user(user_name="outsider_details_perm")
        cls.group = GroupHelpers.create_group(creator=cls.creator)

    def test_group_details_login_required(self):
        data = {"group_id": self.group.id}
        response = self.client.get(reverse("splittime:api_group_details_view"), data=data)
        self.assertEqual(response.status_code, 401)

    def test_group_details_permission_as_outsider(self):
        UserHelpers.login_user(self.client, self.outsider)
        data = {"group_id": self.group.id}
        response = self.client.get(reverse("splittime:api_group_details_view"), data=data)
        self.assertEqual(response.status_code, 401)
