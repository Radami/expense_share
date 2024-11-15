from django.urls import reverse

from rest_framework.test import APITestCase

from ..helpers import GroupHelpers, UserHelpers
from splittime.models import Expense


class AddExpenseAPITestView(APITestCase):

    @classmethod
    def setUpTestData(self):
        self.user1 = UserHelpers.create_user()
        self.user2 = UserHelpers.create_user()
        self.user3 = UserHelpers.create_user()
        self.group1 = GroupHelpers.create_group(creator=self.user1)
        GroupHelpers.add_user_to_group(self.group1, self.user2)
        self.expense1 = GroupHelpers.add_expense(self.group1, self.user1)
        self.expense2 = GroupHelpers.add_expense(self.group1, self.user1)

    def login(self, user):
        self.assertEqual(
            self.client.login(username=user.username, password="glassonion123"),
            True,
        )
        response = self.client.post(
            reverse("users:token_obtain"),
            {"username": user.username, "password": "glassonion123"},
        )
        self.assertEqual(response.status_code, 200)
        token = response.data.get("access")
        self.assertIsNotNone(token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_delete_expense_creator(self):
        self.login(self.user1)
        data = {"expense_id": self.expense1.id}

        response = self.client.post(reverse("splittime:api_delete_group_expense_view"), data=data)
        self.assertEqual(response.status_code, 200)

        self.assertFalse(Expense.objects.filter(pk=self.expense1.id).exists())
        self.assertTrue(Expense.objects.filter(pk=self.expense2.id).exists())

    def test_delete_expense_participant(self):
        self.login(self.user2)
        data = {"expense_id": self.expense1.id}

        response = self.client.post(reverse("splittime:api_delete_group_expense_view"), data=data)
        self.assertEqual(response.status_code, 200)

        self.assertFalse(Expense.objects.filter(pk=self.expense1.id).exists())
        self.assertTrue(Expense.objects.filter(pk=self.expense2.id).exists())

    def test_delete_expense_outsider(self):
        self.login(self.user3)
        data = {"expense_id": self.expense1.id}

        response = self.client.post(reverse("splittime:api_delete_group_expense_view"), data=data)
        self.assertEqual(response.status_code, 403)

        self.assertTrue(Expense.objects.filter(pk=self.expense1.id).exists())
        self.assertTrue(Expense.objects.filter(pk=self.expense2.id).exists())

    def test_delete_expense_not_logged_in(self):
        data = {"expense_id": self.expense1.id}

        response = self.client.post(reverse("splittime:api_delete_group_expense_view"), data=data)
        self.assertEqual(response.status_code, 401)

        self.assertTrue(Expense.objects.filter(pk=self.expense1.id).exists())
        self.assertTrue(Expense.objects.filter(pk=self.expense2.id).exists())
