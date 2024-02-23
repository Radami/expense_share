from django.test import TestCase
from django.core.exceptions import PermissionDenied

from .helpers import GroupHelpers, UserHelpers
from ..models import Expense
from ..services.expenses import ExpenseService


class DeleteExpenseTest(TestCase):

    def setUp(self):
        self.user1 = UserHelpers.create_user()
        self.user2 = UserHelpers.create_user()
        self.group1 = GroupHelpers.create_group(creator=self.user1)
        self.expense1 = GroupHelpers.add_expense(self.group1, self.user1)
        self.expense2 = GroupHelpers.add_expense(self.group1, self.user1)

    def test_delete_expense(self):
        ExpenseService.delete_expense(self.expense1, self.user1)
        self.assertFalse(Expense.objects.filter(pk=self.expense1.id).exists())

    def test_delete_expense_invalid_user(self):
        self.assertRaises(
            PermissionDenied, ExpenseService.delete_expense, self.expense2, self.user2
        )
