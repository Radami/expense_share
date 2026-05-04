from django.test import TestCase

from splittime.models import Debt, GroupMembership
from ..helpers import GroupHelpers, UserHelpers


class ModelStrTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = UserHelpers.create_user(user_name="str_u1")
        cls.user2 = UserHelpers.create_user(user_name="str_u2")
        cls.group = GroupHelpers.create_group(creator=cls.user1, group_name="Str Test Group")
        GroupHelpers.add_user_to_group(cls.group, cls.user2)
        cls.expense = GroupHelpers.add_expense(
            cls.group, cls.user1, name="Str Expense", currency="USD", amount=100.0
        )

    def test_group_str(self):
        self.assertEqual(str(self.group), "Str Test Group")

    def test_group_membership_str(self):
        gm = GroupMembership.objects.get(group=self.group, member=self.user1)
        self.assertEqual(str(gm), "Str Test Group-str_u1")

    def test_expense_str(self):
        self.assertEqual(str(self.expense), "Str Expense for 100.0 USD")

    def test_debt_str(self):
        debt = Debt.objects.get(expense=self.expense, from_user=self.user2, to_user=self.user1)
        expected = f"str_u2 to str_u1=1 of 100.0USD"
        self.assertEqual(str(debt), expected)

    def test_debt_hash(self):
        """Debt instances must be usable in sets and as dict keys"""
        debt = Debt.objects.filter(expense=self.expense).first()
        debt_set = {debt}
        self.assertIn(debt, debt_set)