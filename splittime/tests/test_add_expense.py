from http import HTTPStatus

from django.test import TestCase

from .helpers import GroupHelpers, UserHelpers
from ..models import Expense, Debt


class AddExpenseTest(TestCase):

    def setUp(self):
        self.user1 = UserHelpers.create_user()
        self.user2 = UserHelpers.create_user()
        self.user3 = UserHelpers.create_user()
        self.group1 = GroupHelpers.create_group(creator=self.user1)

    def test_add_expense_group_with_only_creator(self):
        """
        Test adding an expense to an existing group and that no debt relationships
        are created if the group has just 1 user
        """
        data = {
            "expense_name": "test_expense1",
            "expense_currency": "USD",
            "expense_amount": 100,
            "payee": self.user1.id
        }
        url = "/splittime/group/"+str(self.group1.id) + "/add_expense"
        response = self.client.post(url,
                                    data=data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        # Check the expense was successfully saved
        expense = Expense.objects.get(name="test_expense1")
        self.assertIsNotNone(expense)
        self.assertEqual(expense.name, "test_expense1")
        self.assertEqual(expense.currency, "USD")
        self.assertEqual(expense.amount, 100)
        self.assertEqual(expense.payee.id, self.user1.id)
        # There should be no debt relationships for a group with just the creator
        debt = Debt.objects.filter(expense=expense)
        self.assertEqual(len(debt), 0)

    def test_add_expense_group_with_1_member(self):
        """
        Test that an expense can be added to a group and that a debt relationship
        is created if the group has 1 other member
        """
        data = {
            "expense_name": "test_expense2",
            "expense_currency": "USD",
            "expense_amount": 100,
            "payee": self.user1.id
        }
        GroupHelpers.add_user_to_group(self.group1, self.user2)
        url = "/splittime/group/"+str(self.group1.id) + "/add_expense"
        response = self.client.post(url,
                                    data=data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        # Check the expense was successfully saved
        expense = Expense.objects.get(name="test_expense2")
        self.assertIsNotNone(expense)
        self.assertEqual(expense.name, "test_expense2")
        self.assertEqual(expense.currency, "USD")
        self.assertEqual(expense.amount, 100)
        self.assertEqual(expense.payee.id, self.user1.id)
        # There should be a debt relationship with the other group member
        debt_set = Debt.objects.filter(expense=expense)
        self.assertEqual(len(debt_set), 1)
        debt = debt_set[0]
        self.assertEqual(debt.from_user.id, self.user2.id)
        self.assertEqual(debt.to_user.id, self.user1.id)
        self.assertEqual(debt.ratio, 50)
        self.assertEqual(debt.expense.id, expense.id)

    def test_add_expense_group_with_2_members(self):
        """
        Test that an expense can be added to a group and that a debt relationship
        is created if the group has 1 other member
        """
        data = {
            "expense_name": "test_expense2",
            "expense_currency": "USD",
            "expense_amount": 100,
            "payee": self.user1.id
        }
        GroupHelpers.add_user_to_group(self.group1, self.user2)
        GroupHelpers.add_user_to_group(self.group1, self.user3)
        url = "/splittime/group/"+str(self.group1.id) + "/add_expense"
        response = self.client.post(url,
                                    data=data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        # Check the expense was successfully saved
        expense = Expense.objects.get(name="test_expense2")
        self.assertIsNotNone(expense)
        self.assertEqual(expense.name, "test_expense2")
        self.assertEqual(expense.currency, "USD")
        self.assertEqual(expense.amount, 100)
        self.assertEqual(expense.payee.id, self.user1.id)
        # There should be 2 debt relationships, one with each other group member
        debt_set = Debt.objects.filter(expense=expense)
        self.assertEqual(len(debt_set), 2)
        debt = debt_set[0]
        self.assertEqual(debt.from_user.id, self.user2.id)
        self.assertEqual(debt.to_user.id, self.user1.id)
        self.assertEqual(debt.ratio, 33)
        self.assertEqual(debt.expense.id, expense.id)
        debt = debt_set[1]
        self.assertEqual(debt.from_user.id, self.user3.id)
        self.assertEqual(debt.to_user.id, self.user1.id)
        self.assertEqual(debt.ratio, 33)
        self.assertEqual(debt.expense.id, expense.id)
