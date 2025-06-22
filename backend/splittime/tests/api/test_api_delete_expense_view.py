from django.urls import reverse

from rest_framework.test import APITestCase

from ..helpers import GroupHelpers, UserHelpers
from splittime.models import Expense


class AddExpenseAPITestView(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = UserHelpers.create_user(user_name="user1_del_exp")
        cls.user2 = UserHelpers.create_user(user_name="user2_del_exp")
        cls.user3 = UserHelpers.create_user(user_name="user3_del_exp")
        cls.group1 = GroupHelpers.create_group(creator=cls.user1)
        GroupHelpers.add_user_to_group(cls.group1, cls.user2)
        cls.expense1 = GroupHelpers.add_expense(cls.group1, cls.user1)
        cls.expense2 = GroupHelpers.add_expense(cls.group1, cls.user1)

    def test_delete_expense_creator(self):
        UserHelpers.login_user(self.client, self.user1)
        data = {"expense_id": self.expense1.id}

        response = self.client.post(reverse("splittime:api_delete_group_expense_view"), data=data)
        self.assertEqual(response.status_code, 200)

        self.assertFalse(Expense.objects.filter(pk=self.expense1.id).exists())
        self.assertTrue(Expense.objects.filter(pk=self.expense2.id).exists())

    def test_delete_expense_participant(self):
        UserHelpers.login_user(self.client, self.user2)
        data = {"expense_id": self.expense1.id}

        response = self.client.post(reverse("splittime:api_delete_group_expense_view"), data=data)
        self.assertEqual(response.status_code, 200)

        self.assertFalse(Expense.objects.filter(pk=self.expense1.id).exists())
        self.assertTrue(Expense.objects.filter(pk=self.expense2.id).exists())

    def test_delete_expense_outsider(self):
        UserHelpers.login_user(self.client, self.user3)
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
