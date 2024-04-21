from django.test import TestCase
from django.urls import reverse

from .helpers import GroupHelpers, UserHelpers
from ..models import Expense


class DeleteExpenseTest(TestCase):

    def setUp(self):
        self.user1 = UserHelpers.create_user()
        self.user2 = UserHelpers.create_user()
        self.user3 = UserHelpers.create_user()
        self.group1 = GroupHelpers.create_group(creator=self.user1)
        GroupHelpers.add_user_to_group(self.group1, self.user2)
        self.expense1 = GroupHelpers.add_expense(self.group1, self.user1)
        self.expense2 = GroupHelpers.add_expense(self.group1, self.user1)

    def test_delete_expense_creator(self):
        self.assertEqual(
            self.client.login(
                username=self.user1.username,
                password="glassonion123",
            ),
            True,
        )
        url = reverse(
            "splittime:delete_expense",
            args=(self.expense1.id,),
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/splittime/group/" + str(self.group1.id) + "/")
        self.assertFalse(Expense.objects.filter(pk=self.expense1.id).exists())
        self.assertTrue(Expense.objects.filter(pk=self.expense2.id).exists())

    def test_delete_expense_participant(self):
        self.assertEqual(
            self.client.login(
                username=self.user2.username,
                password="glassonion123",
            ),
            True,
        )
        url = reverse(
            "splittime:delete_expense",
            args=(self.expense1.id,),
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/splittime/group/" + str(self.group1.id) + "/")
        self.assertFalse(Expense.objects.filter(pk=self.expense1.id).exists())
        self.assertTrue(Expense.objects.filter(pk=self.expense2.id).exists())

    def test_delete_expense_outsider(self):
        self.assertEqual(
            self.client.login(
                username=self.user3.username,
                password="glassonion123",
            ),
            True,
        )
        url = reverse(
            "splittime:delete_expense",
            args=(self.expense1.id,),
        )
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Expense.objects.filter(pk=self.expense1.id).exists())
        self.assertTrue(Expense.objects.filter(pk=self.expense2.id).exists())

    def test_delete_expense_not_logged_in(self):
        url = reverse(
            "splittime:delete_expense",
            args=(self.expense1.id,),
        )
        response = self.client.post(url)
        self.assertEqual(
            "/splittime/login?next=/splittime/expense/" + str(self.expense1.id) + "/delete_expense",
            response.url,
        )
        self.assertTrue(Expense.objects.filter(pk=self.expense1.id).exists())
        self.assertTrue(Expense.objects.filter(pk=self.expense2.id).exists())
