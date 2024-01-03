from django.test import TestCase

from .helpers import GroupHelpers, UserHelpers
from ..services.balances import BalanceCalculator


class GroupDetailViewTests(TestCase):

    def setUp(self):
        self.user1 = UserHelpers.create_user()
        self.user2 = UserHelpers.create_user()
        self.user3 = UserHelpers.create_user()
        self.group1 = GroupHelpers.create_group(creator=self.user1)
        self.group2 = GroupHelpers.create_group(creator=self.user1)
        GroupHelpers.add_user_to_group(self.group2, self.user2)
        self.group3 = GroupHelpers.create_group(creator=self.user1)
        GroupHelpers.add_user_to_group(self.group3, self.user2)
        GroupHelpers.add_user_to_group(self.group3, self.user3)

    def test_balances_with_1_members(self):
        """
        Balances for a group with 1 member should be empty
        """
        balances = BalanceCalculator.calculateBalances(self.group1)
        GroupHelpers.add_expense(self.group1, self.user1)
        GroupHelpers.add_expense(self.group1, self.user1)
        GroupHelpers.add_expense(self.group1, self.user1)
        self.assertEquals(len(balances), 0)

    def test_balances_with_2_members(self):
        GroupHelpers.add_expense(self.group2, self.user1)
        balances = BalanceCalculator.calculateBalances(self.group2)
        self.assertEquals(len(balances), 2)
