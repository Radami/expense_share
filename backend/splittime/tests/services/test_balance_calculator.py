from django.test import TestCase

from ..helpers import GroupHelpers, UserHelpers
from splittime.services.balances import BalanceCalculator


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
        balances = BalanceCalculator.calculateBalancesAPI(self.group1)
        GroupHelpers.add_expense(self.group1, self.user1)
        GroupHelpers.add_expense(self.group1, self.user1)
        GroupHelpers.add_expense(self.group1, self.user1)
        self.assertEqual(len(balances), 0)

    def test_balances_2_members_1_expense(self):
        GroupHelpers.add_expense(self.group2, self.user1)
        balances = BalanceCalculator.calculateBalancesAPI(self.group2)
        self.assertEqual(len(balances), 2)
        self.assertEqual(balances[self.user1.id][self.user2.id]["USD"], 50.0)
        self.assertEqual(balances[self.user2.id][self.user1.id]["USD"], -50.0)

    def test_balances_2_members_3_expenses(self):
        GroupHelpers.add_expense(self.group2, self.user1, amount="200")
        balances = BalanceCalculator.calculateBalancesAPI(self.group2)
        self.assertEqual(len(balances), 2)
        self.assertEqual(balances[self.user1.id][self.user2.id]["USD"], 100.0)
        self.assertEqual(balances[self.user2.id][self.user1.id]["USD"], -100.0)
        GroupHelpers.add_expense(self.group2, self.user1, amount="300")
        balances = BalanceCalculator.calculateBalancesAPI(self.group2)
        self.assertEqual(len(balances), 2)
        self.assertEqual(balances[self.user1.id][self.user2.id]["USD"], 250.0)
        self.assertEqual(balances[self.user2.id][self.user1.id]["USD"], -250.0)
        GroupHelpers.add_expense(self.group2, self.user1, amount="400")
        balances = BalanceCalculator.calculateBalancesAPI(self.group2)
        self.assertEqual(len(balances), 2)
        self.assertEqual(balances[self.user1.id][self.user2.id]["USD"], 450.0)
        self.assertEqual(balances[self.user2.id][self.user1.id]["USD"], -450.0)

    def test_balances_2_members_multiple_cuerrencies(self):
        GroupHelpers.add_expense(self.group2, self.user1, amount="400", currency="USD")
        GroupHelpers.add_expense(self.group2, self.user2, amount="200", currency="GBP")
        balances = BalanceCalculator.calculateBalancesAPI(self.group2)
        self.assertEqual(len(balances), 2)
        self.assertEqual(balances[self.user1.id][self.user2.id]["USD"], 200.0)
        self.assertEqual(balances[self.user2.id][self.user1.id]["GBP"], 100.0)
        self.assertEqual(balances[self.user2.id][self.user1.id]["USD"], -200.0)
        self.assertEqual(balances[self.user1.id][self.user2.id]["GBP"], -100.0)

    def test_balance_2_members_delete_expenses(self):
        expense1 = GroupHelpers.add_expense(self.group2, self.user1, amount="200")
        balances = BalanceCalculator.calculateBalancesAPI(self.group2)
        self.assertEqual(len(balances), 2)
        self.assertEqual(balances[self.user1.id][self.user2.id]["USD"], 100.0)
        self.assertEqual(balances[self.user2.id][self.user1.id]["USD"], -100.0)
        expense2 = GroupHelpers.add_expense(self.group2, self.user1, amount="300")
        balances = BalanceCalculator.calculateBalancesAPI(self.group2)
        self.assertEqual(len(balances), 2)
        self.assertEqual(balances[self.user1.id][self.user2.id]["USD"], 250.0)
        self.assertEqual(balances[self.user2.id][self.user1.id]["USD"], -250.0)
        GroupHelpers.delete_expense(expense1, self.user1)
        balances = BalanceCalculator.calculateBalancesAPI(self.group2)
        self.assertEqual(len(balances), 2)
        self.assertEqual(balances[self.user1.id][self.user2.id]["USD"], 150.0)
        self.assertEqual(balances[self.user2.id][self.user1.id]["USD"], -150.0)
        GroupHelpers.delete_expense(expense2, self.user1)
        balances = BalanceCalculator.calculateBalancesAPI(self.group2)
        self.assertEqual(len(balances), 0)


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
        balances = BalanceCalculator.calculateBalancesAPI(self.group1)
        self.assertEqual(len(balances), 3)
        self.assertEqual(balances[self.user1.id][self.user2.id]["USD"], 100.0)
        self.assertEqual(balances[self.user2.id][self.user1.id]["USD"], -100.0)
        self.assertEqual(balances[self.user1.id][self.user3.id]["USD"], 100.0)
        self.assertEqual(balances[self.user3.id][self.user1.id]["USD"], -100.0)

    def test_balances_3_members_3_expenses_1_owner(self):
        GroupHelpers.add_expense(self.group1, self.user1, amount="300", currency="USD")
        balances = BalanceCalculator.calculateBalancesAPI(self.group1)
        self.assertEqual(len(balances), 3)
        self.assertEqual(balances[self.user1.id][self.user2.id]["USD"], 100.0)
        self.assertEqual(balances[self.user2.id][self.user1.id]["USD"], -100.0)
        self.assertEqual(balances[self.user1.id][self.user3.id]["USD"], 100.0)
        self.assertEqual(balances[self.user3.id][self.user1.id]["USD"], -100.0)
        GroupHelpers.add_expense(self.group1, self.user1, amount="600", currency="USD")
        balances = BalanceCalculator.calculateBalancesAPI(self.group1)
        self.assertEqual(len(balances), 3)
        self.assertEqual(balances[self.user1.id][self.user2.id]["USD"], 300.0)
        self.assertEqual(balances[self.user2.id][self.user1.id]["USD"], -300.0)
        self.assertEqual(balances[self.user1.id][self.user3.id]["USD"], 300.0)
        self.assertEqual(balances[self.user3.id][self.user1.id]["USD"], -300.0)
        GroupHelpers.add_expense(self.group1, self.user1, amount="900", currency="USD")
        balances = BalanceCalculator.calculateBalancesAPI(self.group1)
        self.assertEqual(len(balances), 3)
        self.assertEqual(balances[self.user1.id][self.user2.id]["USD"], 600.0)
        self.assertEqual(balances[self.user2.id][self.user1.id]["USD"], -600.0)
        self.assertEqual(balances[self.user1.id][self.user3.id]["USD"], 600.0)
        self.assertEqual(balances[self.user3.id][self.user1.id]["USD"], -600.0)

    def test_balances_3_members_3_expenses_different_currencies(self):
        GroupHelpers.add_expense(self.group1, self.user1, amount="300", currency="USD")
        GroupHelpers.add_expense(self.group1, self.user2, amount="600", currency="GBP")
        GroupHelpers.add_expense(self.group1, self.user3, amount="900", currency="EUR")
        balances = BalanceCalculator.calculateBalancesAPI(self.group1)
        self.assertEqual(len(balances), 3)
        self.assertEqual(balances[self.user1.id][self.user2.id]["USD"], 100.0)
        self.assertEqual(balances[self.user2.id][self.user1.id]["USD"], -100.0)
        self.assertEqual(balances[self.user1.id][self.user3.id]["USD"], 100.0)
        self.assertEqual(balances[self.user3.id][self.user1.id]["USD"], -100.0)
        self.assertEqual(balances[self.user2.id][self.user3.id]["GBP"], 200.0)
        self.assertEqual(balances[self.user3.id][self.user2.id]["GBP"], -200.0)
        self.assertEqual(balances[self.user2.id][self.user1.id]["GBP"], 200.0)
        self.assertEqual(balances[self.user1.id][self.user2.id]["GBP"], -200.0)
        self.assertEqual(balances[self.user3.id][self.user1.id]["EUR"], 300.0)
        self.assertEqual(balances[self.user1.id][self.user3.id]["EUR"], -300.0)
        self.assertEqual(balances[self.user3.id][self.user2.id]["EUR"], 300.0)
        self.assertEqual(balances[self.user2.id][self.user3.id]["EUR"], -300.0)

    def test_balances_3_members_3_expenses_delete_expenses(self):
        expense1 = GroupHelpers.add_expense(self.group1, self.user1, amount="300", currency="USD")
        balances = BalanceCalculator.calculateBalancesAPI(self.group1)
        self.assertEqual(len(balances), 3)
        self.assertEqual(balances[self.user1.id][self.user2.id]["USD"], 100.0)
        self.assertEqual(balances[self.user2.id][self.user1.id]["USD"], -100.0)
        self.assertEqual(balances[self.user1.id][self.user3.id]["USD"], 100.0)
        self.assertEqual(balances[self.user3.id][self.user1.id]["USD"], -100.0)
        expense2 = GroupHelpers.add_expense(self.group1, self.user1, amount="600", currency="USD")
        balances = BalanceCalculator.calculateBalancesAPI(self.group1)
        self.assertEqual(len(balances), 3)
        self.assertEqual(balances[self.user1.id][self.user2.id]["USD"], 300.0)
        self.assertEqual(balances[self.user2.id][self.user1.id]["USD"], -300.0)
        self.assertEqual(balances[self.user1.id][self.user3.id]["USD"], 300.0)
        self.assertEqual(balances[self.user3.id][self.user1.id]["USD"], -300.0)
        expense3 = GroupHelpers.add_expense(self.group1, self.user1, amount="900", currency="USD")
        balances = BalanceCalculator.calculateBalancesAPI(self.group1)
        self.assertEqual(len(balances), 3)
        self.assertEqual(balances[self.user1.id][self.user2.id]["USD"], 600.0)
        self.assertEqual(balances[self.user2.id][self.user1.id]["USD"], -600.0)
        self.assertEqual(balances[self.user1.id][self.user3.id]["USD"], 600.0)
        self.assertEqual(balances[self.user3.id][self.user1.id]["USD"], -600.0)
        GroupHelpers.delete_expense(expense1, self.user1)
        balances = BalanceCalculator.calculateBalancesAPI(self.group1)
        self.assertEqual(len(balances), 3)
        self.assertEqual(balances[self.user1.id][self.user2.id]["USD"], 500.0)
        self.assertEqual(balances[self.user2.id][self.user1.id]["USD"], -500.0)
        self.assertEqual(balances[self.user1.id][self.user3.id]["USD"], 500.0)
        self.assertEqual(balances[self.user3.id][self.user1.id]["USD"], -500.0)
        GroupHelpers.delete_expense(expense2, self.user1)
        balances = BalanceCalculator.calculateBalancesAPI(self.group1)
        self.assertEqual(len(balances), 3)
        self.assertEqual(balances[self.user1.id][self.user2.id]["USD"], 300.0)
        self.assertEqual(balances[self.user2.id][self.user1.id]["USD"], -300.0)
        self.assertEqual(balances[self.user1.id][self.user3.id]["USD"], 300.0)
        self.assertEqual(balances[self.user3.id][self.user1.id]["USD"], -300.0)
        GroupHelpers.delete_expense(expense3, self.user1)
        balances = BalanceCalculator.calculateBalancesAPI(self.group1)
        self.assertEqual(len(balances), 0)


class GroupOwing2UsersTests(TestCase):
    def setUp(self):
        self.user1 = UserHelpers.create_user()
        self.user2 = UserHelpers.create_user()
        self.group1 = GroupHelpers.create_group(creator=self.user1)
        GroupHelpers.add_user_to_group(self.group1, self.user2)

    def test_owing_1_expense(self):
        GroupHelpers.add_expense(self.group1, self.user1, amount="100", currency="USD")
        user1_owes = BalanceCalculator.calculateUserOwes(self.group1.id, self.user1.id, True)
        user2_owes = BalanceCalculator.calculateUserOwes(self.group1.id, self.user2.id, True)
        user1_is_owed = BalanceCalculator.calculateUserIsOwed(self.group1.id, self.user1.id, True)
        user2_is_owed = BalanceCalculator.calculateUserIsOwed(self.group1.id, self.user2.id, True)
        self.assertEqual(user1_owes, ("USD", -50))
        self.assertEqual(user2_owes, ("USD", 50))
        self.assertEqual(user1_is_owed, ("USD", 50))
        self.assertEqual(user2_is_owed, ("USD", -50))

        user1_owes_explicit = BalanceCalculator.calculateUserOwes(
            self.group1.id, self.user1.id, False
        )
        user2_owes_explicit = BalanceCalculator.calculateUserOwes(
            self.group1.id, self.user2.id, False
        )
        user1_is_owed_explicit = BalanceCalculator.calculateUserIsOwed(
            self.group1.id, self.user1.id, False
        )
        user2_is_owed_explicit = BalanceCalculator.calculateUserIsOwed(
            self.group1.id, self.user2.id, False
        )
        self.assertEqual(user1_owes_explicit, ("XYZ", 0))
        self.assertEqual(user2_owes_explicit, ("USD", 50))
        self.assertEqual(user1_is_owed_explicit, ("USD", 50))
        self.assertEqual(user2_is_owed_explicit, ("XYZ", 0))

    def test_owing_1_direction_1_currency(self):
        GroupHelpers.add_expense(self.group1, self.user1, amount="100", currency="USD")
        GroupHelpers.add_expense(self.group1, self.user1, amount="200", currency="USD")
        GroupHelpers.add_expense(self.group1, self.user1, amount="300", currency="USD")
        user1_owes = BalanceCalculator.calculateUserOwes(self.group1.id, self.user1.id, True)
        user2_owes = BalanceCalculator.calculateUserOwes(self.group1.id, self.user2.id, True)
        user1_is_owed = BalanceCalculator.calculateUserIsOwed(self.group1.id, self.user1.id, True)
        user2_is_owed = BalanceCalculator.calculateUserIsOwed(self.group1.id, self.user2.id, True)
        self.assertEqual(user1_owes, ("USD", -300))
        self.assertEqual(user2_owes, ("USD", 300))
        self.assertEqual(user1_is_owed, ("USD", 300))
        self.assertEqual(user2_is_owed, ("USD", -300))

        user1_owes_explicit = BalanceCalculator.calculateUserOwes(
            self.group1.id, self.user1.id, False
        )
        user2_owes_explicit = BalanceCalculator.calculateUserOwes(
            self.group1.id, self.user2.id, False
        )
        user1_is_owed_explicit = BalanceCalculator.calculateUserIsOwed(
            self.group1.id, self.user1.id, False
        )
        user2_is_owed_explicit = BalanceCalculator.calculateUserIsOwed(
            self.group1.id, self.user2.id, False
        )
        self.assertEqual(user1_owes_explicit, ("XYZ", 0))
        self.assertEqual(user2_owes_explicit, ("USD", 300))
        self.assertEqual(user1_is_owed_explicit, ("USD", 300))
        self.assertEqual(user2_is_owed_explicit, ("XYZ", 0))

    def test_owing_1_direction_3_currency(self):
        GroupHelpers.add_expense(self.group1, self.user1, amount="100", currency="USD")
        GroupHelpers.add_expense(self.group1, self.user1, amount="200", currency="EUR")
        GroupHelpers.add_expense(self.group1, self.user1, amount="300", currency="GBP")
        user1_owes = BalanceCalculator.calculateUserOwes(self.group1.id, self.user1.id, True)
        user2_owes = BalanceCalculator.calculateUserOwes(self.group1.id, self.user2.id, True)
        user1_is_owed = BalanceCalculator.calculateUserIsOwed(self.group1.id, self.user1.id, True)
        user2_is_owed = BalanceCalculator.calculateUserIsOwed(self.group1.id, self.user2.id, True)
        self.assertEqual(user1_owes, ("GBP", -150))
        self.assertEqual(user2_owes, ("GBP", 150))
        self.assertEqual(user1_is_owed, ("GBP", 150))
        self.assertEqual(user2_is_owed, ("GBP", -150))

        user1_owes_explicit = BalanceCalculator.calculateUserOwes(
            self.group1.id, self.user1.id, False
        )
        user2_owes_explicit = BalanceCalculator.calculateUserOwes(
            self.group1.id, self.user2.id, False
        )
        user1_is_owed_explicit = BalanceCalculator.calculateUserIsOwed(
            self.group1.id, self.user1.id, False
        )
        user2_is_owed_explicit = BalanceCalculator.calculateUserIsOwed(
            self.group1.id, self.user2.id, False
        )
        self.assertEqual(user1_owes_explicit, ("XYZ", 0))
        self.assertEqual(user2_owes_explicit, ("GBP", 150))
        self.assertEqual(user1_is_owed_explicit, ("GBP", 150))
        self.assertEqual(user2_is_owed_explicit, ("XYZ", 0))

    def test_owing_2_directions_symmetrical(self):
        GroupHelpers.add_expense(self.group1, self.user1, amount="100", currency="USD")
        GroupHelpers.add_expense(self.group1, self.user2, amount="100", currency="USD")
        user1_owes = BalanceCalculator.calculateUserOwes(self.group1.id, self.user1.id, True)
        user2_owes = BalanceCalculator.calculateUserOwes(self.group1.id, self.user2.id, True)
        user1_is_owed = BalanceCalculator.calculateUserIsOwed(self.group1.id, self.user1.id, True)
        user2_is_owed = BalanceCalculator.calculateUserIsOwed(self.group1.id, self.user2.id, True)
        self.assertEqual(user1_owes, ("USD", 0))
        self.assertEqual(user2_owes, ("USD", 0))
        self.assertEqual(user1_is_owed, ("USD", 0))
        self.assertEqual(user2_is_owed, ("USD", 0))

        user1_owes_explicit = BalanceCalculator.calculateUserOwes(
            self.group1.id, self.user1.id, False
        )
        user2_owes_explicit = BalanceCalculator.calculateUserOwes(
            self.group1.id, self.user2.id, False
        )
        user1_is_owed_explicit = BalanceCalculator.calculateUserIsOwed(
            self.group1.id, self.user1.id, False
        )
        user2_is_owed_explicit = BalanceCalculator.calculateUserIsOwed(
            self.group1.id, self.user2.id, False
        )
        self.assertEqual(user1_owes_explicit, ("XYZ", 0))
        self.assertEqual(user2_owes_explicit, ("XYZ", 0))
        self.assertEqual(user1_is_owed_explicit, ("XYZ", 0))
        self.assertEqual(user2_is_owed_explicit, ("XYZ", 0))

    def test_owing_2_directions_multiple_expenses(self):
        GroupHelpers.add_expense(self.group1, self.user1, amount="100", currency="USD")
        GroupHelpers.add_expense(self.group1, self.user2, amount="200", currency="USD")
        GroupHelpers.add_expense(self.group1, self.user1, amount="300", currency="USD")
        GroupHelpers.add_expense(self.group1, self.user2, amount="200", currency="USD")
        GroupHelpers.add_expense(self.group1, self.user2, amount="100", currency="USD")
        user1_owes = BalanceCalculator.calculateUserOwes(self.group1.id, self.user1.id, True)
        user2_owes = BalanceCalculator.calculateUserOwes(self.group1.id, self.user2.id, True)
        user1_is_owed = BalanceCalculator.calculateUserIsOwed(self.group1.id, self.user1.id, True)
        user2_is_owed = BalanceCalculator.calculateUserIsOwed(self.group1.id, self.user2.id, True)
        self.assertEqual(user1_owes, ("USD", 50))
        self.assertEqual(user2_owes, ("USD", -50))
        self.assertEqual(user1_is_owed, ("USD", -50))
        self.assertEqual(user2_is_owed, ("USD", 50))

        user1_owes_explicit = BalanceCalculator.calculateUserOwes(
            self.group1.id, self.user1.id, False
        )
        user2_owes_explicit = BalanceCalculator.calculateUserOwes(
            self.group1.id, self.user2.id, False
        )
        user1_is_owed_explicit = BalanceCalculator.calculateUserIsOwed(
            self.group1.id, self.user1.id, False
        )
        user2_is_owed_explicit = BalanceCalculator.calculateUserIsOwed(
            self.group1.id, self.user2.id, False
        )
        self.assertEqual(user1_owes_explicit, ("USD", 50))
        self.assertEqual(user2_owes_explicit, ("XYZ", 0))
        self.assertEqual(user1_is_owed_explicit, ("XYZ", 0))
        self.assertEqual(user2_is_owed_explicit, ("USD", 50))


class GroupOwingManyUsersTests(TestCase):
    def setUp(self):
        self.user1 = UserHelpers.create_user()
        self.user2 = UserHelpers.create_user()
        self.user3 = UserHelpers.create_user()
        self.group1 = GroupHelpers.create_group(creator=self.user1)
        GroupHelpers.add_user_to_group(self.group1, self.user2)
        GroupHelpers.add_user_to_group(self.group1, self.user3)

    """
        After user 1 expense : user2 -> user1 = 100 , user3 -> user1 = 100
        After user 2 expense : user2 <- user1 = 100 , user3 -> user1 = 100, user3 -> user2 = 200
        After user 3 expense : user2 <- user1 = 100 , user3 <- user1 = 200, user3 <- user2 = 100
    """

    def test_owing_1_directions_3_users_1_expense_per_user(self):
        GroupHelpers.add_expense(self.group1, self.user1, amount="300", currency="USD")
        GroupHelpers.add_expense(self.group1, self.user2, amount="600", currency="USD")
        GroupHelpers.add_expense(self.group1, self.user3, amount="900", currency="USD")
        user1_owes = BalanceCalculator.calculateUserOwes(self.group1.id, self.user1.id, True)
        user2_owes = BalanceCalculator.calculateUserOwes(self.group1.id, self.user2.id, True)
        user3_owes = BalanceCalculator.calculateUserOwes(self.group1.id, self.user3.id, True)
        user1_is_owed = BalanceCalculator.calculateUserIsOwed(self.group1.id, self.user1.id, True)
        user2_is_owed = BalanceCalculator.calculateUserIsOwed(self.group1.id, self.user2.id, True)
        user3_is_owed = BalanceCalculator.calculateUserIsOwed(self.group1.id, self.user3.id, True)
        self.assertEqual(user1_owes, ("USD", 300))
        self.assertEqual(user2_owes, ("USD", 0))
        self.assertEqual(user3_owes, ("USD", -300))
        self.assertEqual(user1_is_owed, ("USD", -300))
        self.assertEqual(user2_is_owed, ("USD", 0))
        self.assertEqual(user3_is_owed, ("USD", 300))

        user1_owes_explicit = BalanceCalculator.calculateUserOwes(
            self.group1.id, self.user1.id, False
        )
        user2_owes_explicit = BalanceCalculator.calculateUserOwes(
            self.group1.id, self.user2.id, False
        )
        user3_owes_explicit = BalanceCalculator.calculateUserOwes(
            self.group1.id, self.user3.id, False
        )
        user1_is_owed_explicit = BalanceCalculator.calculateUserIsOwed(
            self.group1.id, self.user1.id, False
        )
        user2_is_owed_explicit = BalanceCalculator.calculateUserIsOwed(
            self.group1.id, self.user2.id, False
        )
        user3_is_owed_explicit = BalanceCalculator.calculateUserIsOwed(
            self.group1.id, self.user3.id, False
        )
        self.assertEqual(user1_owes_explicit, ("USD", 300))
        self.assertEqual(user2_owes_explicit, ("USD", 100))
        self.assertEqual(user3_owes_explicit, ("XYZ", 0))
        self.assertEqual(user1_is_owed_explicit, ("XYZ", 0))
        self.assertEqual(user2_is_owed_explicit, ("USD", 100))
        self.assertEqual(user3_is_owed_explicit, ("USD", 300))

    """
        After user 1 expense (25 each)
        u1<-u2 = 25, u1<-u3 = 25, u1<-u4 = 25, u2->u3 = 0, u2->u4 = 0, u3->u4 = 0
        After user 2 expense (50 each)
        u1->u2 = 25, u1<-u3 = 25, u1<-u4 = 25, u2<-u3 = 50, u2<-u4 = 50, u3->u4 = 0
        After user 3 expense (75 each)
        u1->u2 = 25, u1->u3 = 50, u1<-u4 = 25, u2->u3 = 25, u2<-u4 = 50, u3<-u4 = 75
        After user 4 expense (100 each)
        u1->u2 = 25, u1->u3 = 50, u1->u4 = 75, u2->u3 = 25, u2->u4 = 50, u3->u4 = 25
    """

    def test_owing_1_direction_4_users_1_expense_per_user(self):

        user4 = UserHelpers.create_user()
        GroupHelpers.add_user_to_group(self.group1, user4)

        GroupHelpers.add_expense(self.group1, self.user1, amount="100", currency="USD")
        GroupHelpers.add_expense(self.group1, self.user2, amount="200", currency="USD")
        GroupHelpers.add_expense(self.group1, self.user3, amount="300", currency="USD")
        GroupHelpers.add_expense(self.group1, user4, amount="400", currency="USD")
        user1_owes = BalanceCalculator.calculateUserOwes(self.group1.id, self.user1.id, True)
        user2_owes = BalanceCalculator.calculateUserOwes(self.group1.id, self.user2.id, True)
        user3_owes = BalanceCalculator.calculateUserOwes(self.group1.id, self.user3.id, True)
        user4_owes = BalanceCalculator.calculateUserOwes(self.group1.id, user4.id, True)
        user1_is_owed = BalanceCalculator.calculateUserIsOwed(self.group1.id, self.user1.id, True)
        user2_is_owed = BalanceCalculator.calculateUserIsOwed(self.group1.id, self.user2.id, True)
        user3_is_owed = BalanceCalculator.calculateUserIsOwed(self.group1.id, self.user3.id, True)
        user4_is_owed = BalanceCalculator.calculateUserIsOwed(self.group1.id, user4.id, True)
        self.assertEqual(user1_owes, ("USD", 150))
        self.assertEqual(user2_owes, ("USD", 50))
        self.assertEqual(user3_owes, ("USD", -50))
        self.assertEqual(user4_owes, ("USD", -150))
        self.assertEqual(user1_is_owed, ("USD", -150))
        self.assertEqual(user2_is_owed, ("USD", -50))
        self.assertEqual(user3_is_owed, ("USD", 50))
        self.assertEqual(user4_is_owed, ("USD", 150))

        user1_owes_explicit = BalanceCalculator.calculateUserOwes(
            self.group1.id, self.user1.id, False
        )
        user2_owes_explicit = BalanceCalculator.calculateUserOwes(
            self.group1.id, self.user2.id, False
        )
        user3_owes_explicit = BalanceCalculator.calculateUserOwes(
            self.group1.id, self.user3.id, False
        )
        user4_owes_explicit = BalanceCalculator.calculateUserOwes(self.group1.id, user4.id, False)
        user1_is_owed_explicit = BalanceCalculator.calculateUserIsOwed(
            self.group1.id, self.user1.id, False
        )
        user2_is_owed_explicit = BalanceCalculator.calculateUserIsOwed(
            self.group1.id, self.user2.id, False
        )
        user3_is_owed_explicit = BalanceCalculator.calculateUserIsOwed(
            self.group1.id, self.user3.id, False
        )
        user4_is_owed_explicit = BalanceCalculator.calculateUserIsOwed(
            self.group1.id, user4.id, False
        )
        self.assertEqual(user1_owes_explicit, ("USD", 150))
        self.assertEqual(user2_owes_explicit, ("USD", 75))
        self.assertEqual(user3_owes_explicit, ("USD", 25))
        self.assertEqual(user4_owes_explicit, ("XYZ", 0))
        self.assertEqual(user1_is_owed_explicit, ("XYZ", 0))
        self.assertEqual(user2_is_owed_explicit, ("USD", 25))
        self.assertEqual(user3_is_owed_explicit, ("USD", 75))
        self.assertEqual(user4_is_owed_explicit, ("USD", 150))
