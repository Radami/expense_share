from django.test import TestCase

from .helpers import GroupHelpers, UserHelpers
from ..views.group_views import BalanceCalculator


class GroupDetailViewTests(TestCase):

    def setUp(self):
        self.user1 = UserHelpers.create_user()
        self.user2 = UserHelpers.create_user()
        self.user3 = UserHelpers.create_user()
        self.group1 = GroupHelpers.create_group(creator=self.user1)

    def test_balances_with_2_members(self):
        balances = BalanceCalculator.calculateBalances(self.group1)
        self.assertEquals(len(balances), 0)

    def test_balances_with_2_members(self):
        GroupHelpers.add_expense(self.group1, self.user1)
        balances = BalanceCalculator.calculateBalances(self.group1)
       # self.assertNotEquals(len(balances), 0)
