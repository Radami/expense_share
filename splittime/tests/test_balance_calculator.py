from django.test import TestCase

from .helpers import GroupHelpers, UserHelpers
from ..services.balances import BalanceCalculator


class BalanceCalculator2MembersTests(TestCase):

    def setUp(self):
        self.user1 = UserHelpers.create_user()
        self.user2 = UserHelpers.create_user()
        self.group1 = GroupHelpers.create_group(creator=self.user1)
        self.group2 = GroupHelpers.create_group(creator=self.user1)
        GroupHelpers.add_user_to_group(self.group2, self.user2)

    def test_balances_with_1_members(self):
        """
        Balances for a group with 1 member should be empty
        """
        balances = BalanceCalculator.calculateBalances(self.group1)
        GroupHelpers.add_expense(self.group1, self.user1)
        GroupHelpers.add_expense(self.group1, self.user1)
        GroupHelpers.add_expense(self.group1, self.user1)
        self.assertEquals(len(balances), 0)

    def test_balances_2_members_1_expense(self):
        GroupHelpers.add_expense(self.group2, self.user1)
        balances = BalanceCalculator.calculateBalances(self.group2)
        self.assertEquals(len(balances), 2)
        self.assertEqual(balances[self.user1][self.user2]["USD"], 50.0)
        self.assertEqual(balances[self.user2][self.user1]["USD"], -50.0)

    def test_balances_2_members_3_expenses(self):
        GroupHelpers.add_expense(self.group2, self.user1, amount="200")
        balances = BalanceCalculator.calculateBalances(self.group2)
        self.assertEquals(len(balances), 2)
        self.assertEqual(balances[self.user1][self.user2]["USD"], 100.0)
        self.assertEqual(balances[self.user2][self.user1]["USD"], -100.0)
        GroupHelpers.add_expense(self.group2, self.user1, amount="300")
        balances = BalanceCalculator.calculateBalances(self.group2)
        self.assertEquals(len(balances), 2)
        self.assertEqual(balances[self.user1][self.user2]["USD"], 250.0)
        self.assertEqual(balances[self.user2][self.user1]["USD"], -250.0)
        GroupHelpers.add_expense(self.group2, self.user1, amount="400")
        balances = BalanceCalculator.calculateBalances(self.group2)
        self.assertEquals(len(balances), 2)
        self.assertEqual(balances[self.user1][self.user2]["USD"], 450.0)
        self.assertEqual(balances[self.user2][self.user1]["USD"], -450.0)

    def test_balances_2_members_3_expenses_balance_out(self):
        GroupHelpers.add_expense(self.group2, self.user1, amount="400")
        balances = BalanceCalculator.calculateBalances(self.group2)
        self.assertEquals(len(balances), 2)
        self.assertEqual(balances[self.user1][self.user2]["USD"], 200.0)
        self.assertEqual(balances[self.user2][self.user1]["USD"], -200.0)
        GroupHelpers.add_expense(self.group2, self.user2, amount="300")
        balances = BalanceCalculator.calculateBalances(self.group2)
        self.assertEquals(len(balances), 2)
        self.assertEqual(balances[self.user1][self.user2]["USD"], 50.0)
        self.assertEqual(balances[self.user2][self.user1]["USD"], -50.0)
        GroupHelpers.add_expense(self.group2, self.user2, amount="100")
        balances = BalanceCalculator.calculateBalances(self.group2)
        self.assertEquals(len(balances), 2)
        self.assertEqual(balances[self.user1][self.user2]["USD"], 0.0)
        self.assertEqual(balances[self.user2][self.user1]["USD"], 0.0)

    def test_balances_2_members_multiple_cuerrencies(self):
        GroupHelpers.add_expense(self.group2, self.user1, amount="400", currency="USD")
        GroupHelpers.add_expense(self.group2, self.user2, amount="200", currency="GBP")
        balances = BalanceCalculator.calculateBalances(self.group2)
        self.assertEquals(len(balances), 2)
        self.assertEqual(balances[self.user1][self.user2]["USD"], 200.0)
        self.assertEqual(balances[self.user2][self.user1]["USD"], -200.0)
        self.assertEqual(balances[self.user1][self.user2]["GBP"], -100.0)
        self.assertEqual(balances[self.user2][self.user1]["GBP"], 100.0)


class BalanceCalculator3MembersTests(TestCase):
    def setUp(self):
        self.user1 = UserHelpers.create_user()
        self.user2 = UserHelpers.create_user()
        self.user3 = UserHelpers.create_user()
        self.group1 = GroupHelpers.create_group(creator=self.user1)
        GroupHelpers.add_user_to_group(self.group1, self.user2)
        GroupHelpers.add_user_to_group(self.group1, self.user3)

    def test_balances_3_members_1_expense(self):
        GroupHelpers.add_expense(self.group1, self.user1, amount="300", currency="USD")
        balances = BalanceCalculator.calculateBalances(self.group1)
        self.assertEquals(len(balances), 3)
        self.assertEqual(balances[self.user1][self.user2]["USD"], 100.0)
        self.assertEqual(balances[self.user2][self.user1]["USD"], -100.0)
        self.assertEqual(balances[self.user1][self.user3]["USD"], 100.0)
        self.assertEqual(balances[self.user3][self.user1]["USD"], -100.0)

    def test_balances_3_members_3_expenses_1_owner(self):
        GroupHelpers.add_expense(self.group1, self.user1, amount="300", currency="USD")
        balances = BalanceCalculator.calculateBalances(self.group1)
        self.assertEquals(len(balances), 3)
        self.assertEqual(balances[self.user1][self.user2]["USD"], 100.0)
        self.assertEqual(balances[self.user2][self.user1]["USD"], -100.0)
        self.assertEqual(balances[self.user1][self.user3]["USD"], 100.0)
        self.assertEqual(balances[self.user3][self.user1]["USD"], -100.0)
        GroupHelpers.add_expense(self.group1, self.user1, amount="600", currency="USD")
        balances = BalanceCalculator.calculateBalances(self.group1)
        self.assertEquals(len(balances), 3)
        self.assertEqual(balances[self.user1][self.user2]["USD"], 300.0)
        self.assertEqual(balances[self.user2][self.user1]["USD"], -300.0)
        self.assertEqual(balances[self.user1][self.user3]["USD"], 300.0)
        self.assertEqual(balances[self.user3][self.user1]["USD"], -300.0)
        GroupHelpers.add_expense(self.group1, self.user1, amount="900", currency="USD")
        balances = BalanceCalculator.calculateBalances(self.group1)
        self.assertEquals(len(balances), 3)
        self.assertEqual(balances[self.user1][self.user2]["USD"], 600.0)
        self.assertEqual(balances[self.user2][self.user1]["USD"], -600.0)
        self.assertEqual(balances[self.user1][self.user3]["USD"], 600.0)
        self.assertEqual(balances[self.user3][self.user1]["USD"], -600.0)

    def test_balances_3_members_expenses_balancing_out(self):
        GroupHelpers.add_expense(self.group1, self.user1, amount="300", currency="USD")
        balances = BalanceCalculator.calculateBalances(self.group1)
        self.assertEquals(len(balances), 3)
        self.assertEqual(balances[self.user1][self.user2]["USD"], 100.0)
        self.assertEqual(balances[self.user2][self.user1]["USD"], -100.0)
        self.assertEqual(balances[self.user1][self.user3]["USD"], 100.0)
        self.assertEqual(balances[self.user3][self.user1]["USD"], -100.0)
        GroupHelpers.add_expense(self.group1, self.user2, amount="300", currency="USD")
        balances = BalanceCalculator.calculateBalances(self.group1)
        self.assertEquals(len(balances), 3)
        self.assertEqual(balances[self.user1][self.user2]["USD"], 0.0)
        self.assertEqual(balances[self.user2][self.user1]["USD"], 0.0)
        self.assertEqual(balances[self.user1][self.user3]["USD"], 100.0)
        self.assertEqual(balances[self.user3][self.user1]["USD"], -100.0)
        self.assertEqual(balances[self.user2][self.user3]["USD"], 100.0)
        self.assertEqual(balances[self.user3][self.user2]["USD"], -100.0)
        GroupHelpers.add_expense(self.group1, self.user3, amount="300", currency="USD")
        balances = BalanceCalculator.calculateBalances(self.group1)
        self.assertEquals(len(balances), 3)
        self.assertEqual(balances[self.user1][self.user2]["USD"], 0.0)
        self.assertEqual(balances[self.user2][self.user1]["USD"], 0.0)
        self.assertEqual(balances[self.user1][self.user3]["USD"], 0.0)
        self.assertEqual(balances[self.user3][self.user1]["USD"], 0.0)
        self.assertEqual(balances[self.user2][self.user3]["USD"], 0.0)
        self.assertEqual(balances[self.user3][self.user2]["USD"], 0.0)

    def test_balances_3_members_3_expenses_different_currencies(self):
        GroupHelpers.add_expense(self.group1, self.user1, amount="300", currency="USD")
        GroupHelpers.add_expense(self.group1, self.user2, amount="600", currency="GBP")
        GroupHelpers.add_expense(self.group1, self.user3, amount="900", currency="EUR")
        balances = BalanceCalculator.calculateBalances(self.group1)
        self.assertEquals(len(balances), 3)
        self.assertEqual(balances[self.user1][self.user2]["USD"], 100.0)
        self.assertEqual(balances[self.user2][self.user1]["USD"], -100.0)
        self.assertEqual(balances[self.user1][self.user3]["USD"], 100.0)
        self.assertEqual(balances[self.user3][self.user1]["USD"], -100.0)
        self.assertEqual(balances[self.user2][self.user3]["GBP"], 200.0)
        self.assertEqual(balances[self.user3][self.user2]["GBP"], -200.0)
        self.assertEqual(balances[self.user2][self.user1]["GBP"], 200.0)
        self.assertEqual(balances[self.user1][self.user2]["GBP"], -200.0)
        self.assertEqual(balances[self.user3][self.user1]["EUR"], 300.0)
        self.assertEqual(balances[self.user1][self.user3]["EUR"], -300.0)
        self.assertEqual(balances[self.user3][self.user2]["EUR"], 300.0)
        self.assertEqual(balances[self.user2][self.user3]["EUR"], -300.0)
