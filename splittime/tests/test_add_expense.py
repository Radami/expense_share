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

    def test_add_expense_with_only_creator(self):
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
        self.assertEqual(expense.currency, "USD")
        self.assertEqual(expense.amount, 100)
        self.assertEqual(expense.payee.id, self.user1.id)
        # There should be one relationship for the payee of the expense
        debt = Debt.objects.filter(expense=expense)
        self.assertEqual(len(debt), 1)

    def test_add_1_expense_with_1_group_member(self):
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
        self.assertEqual(expense.currency, "USD")
        self.assertEqual(expense.amount, 100)
        self.assertEqual(expense.payee.id, self.user1.id)
        # There should be a debt relationship with the other group member
        debt_set = Debt.objects.filter(expense=expense)
        self.assertEqual(len(debt_set), 2)
        debt1 = Debt(from_user=self.user1, to_user=self.user1, shares=1, expense=expense)
        debt2 = Debt(from_user=self.user2, to_user=self.user1, shares=1, expense=expense)
        self.assertIn(debt1, debt_set)
        self.assertIn(debt2, debt_set)

    def test_add_2_expenses_with_1_group_member(self):
        """
        Test that 2 expense can be added to a group and that 2 debt relationships
        is created if the group has 1 other member
        """
        data = {
            "expense_name": "test_3_expense_1",
            "expense_currency": "USD",
            "expense_amount": 100,
            "payee": self.user1.id
        }
        GroupHelpers.add_user_to_group(self.group1, self.user2)
        url = "/splittime/group/"+str(self.group1.id) + "/add_expense"
        response = self.client.post(url,
                                    data=data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        expense1 = Expense.objects.get(name="test_3_expense_1")
        self.assertIsNotNone(expense1)
        self.assertEqual(expense1.currency, "USD")
        self.assertEqual(expense1.amount, 100)
        self.assertEqual(expense1.payee.id, self.user1.id)
        # Add second expense
        data = {
            "expense_name": "test_3_expense_2",
            "expense_currency": "GBP",
            "expense_amount": 200,
            "payee": self.user2.id
        }
        url = "/splittime/group/"+str(self.group1.id) + "/add_expense"
        response = self.client.post(url,
                                    data=data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        # Check the expense was successfully saved
        expense2 = Expense.objects.get(name="test_3_expense_2")
        self.assertIsNotNone(expense2)
        self.assertEqual(expense2.currency, "GBP")
        self.assertEqual(expense2.amount, 200)
        self.assertEqual(expense2.payee.id, self.user2.id)
        # There should be a debt relationship for each expense with the other group member
        debt_set = Debt.objects.filter(expense=expense1)
        self.assertEqual(len(debt_set), 2)
        debt1 = Debt(from_user=self.user2, to_user=self.user1, shares=1, expense=expense1)
        self.assertIn(debt1, debt_set)
        debt_set = Debt.objects.filter(expense=expense2)
        self.assertEqual(len(debt_set), 2)
        debt2 = Debt(from_user=self.user1, to_user=self.user2, shares=1, expense=expense2)
        self.assertIn(debt2, debt_set)

    def test_add_expense_with_2_group_members(self):
        """
        Test that an expense can be added to a group and that a debt relationship
        is created for each of the other group members
        """
        data = {
            "expense_name": "test_4_expense_1",
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
        expense = Expense.objects.get(name="test_4_expense_1")
        self.assertIsNotNone(expense)
        self.assertEqual(expense.currency, "USD")
        self.assertEqual(expense.amount, 100)
        self.assertEqual(expense.payee.id, self.user1.id)
        # There should be 2 debt relationships, one with each other group member
        debt_set = Debt.objects.filter(expense=expense)
        self.assertEqual(len(debt_set), 3)
        debt1 = Debt(from_user=self.user1, to_user=self.user1, shares=1, expense=expense)
        debt2 = Debt(from_user=self.user2, to_user=self.user1, shares=1, expense=expense)
        debt3 = Debt(from_user=self.user3, to_user=self.user1, shares=1, expense=expense)
        self.assertIn(debt1, debt_set)
        self.assertIn(debt2, debt_set)
        self.assertIn(debt3, debt_set)

    def test_add_2_expenses_with_2_group_members(self):
        """
        Test that multiple expenses can be added to a group and that a debt relationship
        is created for each of the other group members
        """
        data = {
            "expense_name": "test_5_expense_1",
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
        # Check the first expense was successfully saved
        expense1 = Expense.objects.get(name="test_5_expense_1")
        self.assertIsNotNone(expense1)
        self.assertEqual(expense1.currency, "USD")
        self.assertEqual(expense1.amount, 100)
        self.assertEqual(expense1.payee.id, self.user1.id)
        # Create second expense
        data = {
            "expense_name": "test_5_expense_2",
            "expense_currency": "EUR",
            "expense_amount": 300,
            "payee": self.user2.id
        }
        url = "/splittime/group/"+str(self.group1.id) + "/add_expense"
        response = self.client.post(url,
                                    data=data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        # Check the second expense was successfully saved
        expense2 = Expense.objects.get(name="test_5_expense_2")
        self.assertIsNotNone(expense2)
        self.assertEqual(expense2.currency, "EUR")
        self.assertEqual(expense2.amount, 300)
        self.assertEqual(expense2.payee.id, self.user2.id)
        # There should be 3 debt relationships for each expense, one with each other group member
        debt_set = Debt.objects.filter(expense=expense1)
        self.assertEqual(len(debt_set), 3)
        debt1 = Debt(from_user=self.user1, to_user=self.user1, shares=1, expense=expense1)
        debt2 = Debt(from_user=self.user2, to_user=self.user1, shares=1, expense=expense1)
        debt3 = Debt(from_user=self.user3, to_user=self.user1, shares=1, expense=expense1)
        self.assertIn(debt1, debt_set)
        self.assertIn(debt2, debt_set)
        self.assertIn(debt3, debt_set)
        debt_set = Debt.objects.filter(expense=expense2)
        self.assertEqual(len(debt_set), 3)
        debt1 = Debt(from_user=self.user1, to_user=self.user2, shares=1, expense=expense2)
        debt2 = Debt(from_user=self.user2, to_user=self.user2, shares=1, expense=expense2)
        debt3 = Debt(from_user=self.user3, to_user=self.user2, shares=1, expense=expense2)
        self.assertIn(debt1, debt_set)
        self.assertIn(debt2, debt_set)
        self.assertIn(debt3, debt_set)
