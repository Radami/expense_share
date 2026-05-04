from django.urls import reverse
from rest_framework.test import APITestCase

from ..helpers import GroupHelpers, UserHelpers


class FriendsAPIViewTests(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = UserHelpers.create_user(user_name="friends_u1")
        cls.user2 = UserHelpers.create_user(user_name="friends_u2")
        cls.user3 = UserHelpers.create_user(user_name="friends_u3")

    def _get_friend(self, data, user):
        return next((f for f in data if f["id"] == user.id), None)

    def test_not_logged_in(self):
        response = self.client.get(reverse("splittime:api_friends_view"))
        self.assertEqual(response.status_code, 401)

    def test_no_groups_returns_empty(self):
        UserHelpers.login_user(self.client, self.user1)
        response = self.client.get(reverse("splittime:api_friends_view"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_group_with_no_other_members_returns_empty(self):
        """Group where user is the only member is skipped — no friends returned"""
        UserHelpers.login_user(self.client, self.user1)
        GroupHelpers.create_group(creator=self.user1)
        response = self.client.get(reverse("splittime:api_friends_view"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_friend_with_no_expenses(self):
        """Shared group with no expenses: friend appears with empty net balance"""
        UserHelpers.login_user(self.client, self.user1)
        group = GroupHelpers.create_group(creator=self.user1)
        GroupHelpers.add_user_to_group(group, self.user2)

        response = self.client.get(reverse("splittime:api_friends_view"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        friend = self._get_friend(response.data, self.user2)
        self.assertIsNotNone(friend)
        self.assertEqual(len(friend["net"]), 0)
        self.assertEqual(len(friend["groups"]), 1)
        self.assertEqual(len(friend["groups"][0]["you_owe"]), 0)
        self.assertEqual(len(friend["groups"][0]["owed_to"]), 0)

    def test_friend_owes_me(self):
        """I paid: friend shows in owed_to with a positive net amount"""
        UserHelpers.login_user(self.client, self.user1)
        group = GroupHelpers.create_group(creator=self.user1)
        GroupHelpers.add_user_to_group(group, self.user2)
        GroupHelpers.add_expense(group, self.user1, amount=100.0, currency="USD")

        response = self.client.get(reverse("splittime:api_friends_view"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        friend = self._get_friend(response.data, self.user2)
        self.assertIsNotNone(friend)
        self.assertEqual(len(friend["net"]), 1)
        self.assertEqual(friend["net"][0]["currency"], "USD")
        self.assertAlmostEqual(friend["net"][0]["amount"], 50.0, places=2)
        self.assertEqual(len(friend["groups"]), 1)
        self.assertEqual(len(friend["groups"][0]["owed_to"]), 1)
        self.assertEqual(friend["groups"][0]["owed_to"][0]["currency"], "USD")
        self.assertAlmostEqual(friend["groups"][0]["owed_to"][0]["amount"], 50.0, places=2)
        self.assertEqual(len(friend["groups"][0]["you_owe"]), 0)

    def test_i_owe_friend(self):
        """Friend paid: friend shows in you_owe with a negative net amount"""
        UserHelpers.login_user(self.client, self.user1)
        group = GroupHelpers.create_group(creator=self.user1)
        GroupHelpers.add_user_to_group(group, self.user2)
        GroupHelpers.add_expense(group, self.user2, amount=100.0, currency="USD")

        response = self.client.get(reverse("splittime:api_friends_view"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        friend = self._get_friend(response.data, self.user2)
        self.assertIsNotNone(friend)
        self.assertEqual(len(friend["net"]), 1)
        self.assertEqual(friend["net"][0]["currency"], "USD")
        self.assertAlmostEqual(friend["net"][0]["amount"], -50.0, places=2)
        self.assertEqual(len(friend["groups"]), 1)
        self.assertEqual(len(friend["groups"][0]["you_owe"]), 1)
        self.assertEqual(friend["groups"][0]["you_owe"][0]["currency"], "USD")
        self.assertAlmostEqual(friend["groups"][0]["you_owe"][0]["amount"], 50.0, places=2)
        self.assertEqual(len(friend["groups"][0]["owed_to"]), 0)

    def test_minimized_balances_reduces_number_of_transactions(self):
        """
        With minimize_balances=True, intermediate debtors are bypassed.

        user2 pays 300 USD, user3 pays 600 USD in a 3-member group.
        Net: user1 = -300 (debtor), user2 = 0 (neutral), user3 = +300 (creditor).
        Minimized: user1 → user3 directly. user2 is eliminated.
        Non-minimized: user1 → user2, user1 → user3, user2 → user3 (three debts).
        """
        UserHelpers.login_user(self.client, self.user1)
        group = GroupHelpers.create_group(creator=self.user1)
        group.minimize_balances_setting = True
        group.save()
        GroupHelpers.add_user_to_group(group, self.user2)
        GroupHelpers.add_user_to_group(group, self.user3)
        GroupHelpers.add_expense(group, self.user2, amount=300.0, currency="USD")
        GroupHelpers.add_expense(group, self.user3, amount=600.0, currency="USD")

        response = self.client.get(reverse("splittime:api_friends_view"))
        self.assertEqual(response.status_code, 200)

        friend_u2 = self._get_friend(response.data, self.user2)
        friend_u3 = self._get_friend(response.data, self.user3)
        self.assertIsNotNone(friend_u2)
        self.assertIsNotNone(friend_u3)

        # user2 is balanced after minimization — no net debt with user1
        self.assertEqual(len(friend_u2["net"]), 0)
        self.assertEqual(len(friend_u2["groups"][0]["you_owe"]), 0)
        self.assertEqual(len(friend_u2["groups"][0]["owed_to"]), 0)

        # user3 receives the consolidated payment from user1
        self.assertEqual(len(friend_u3["net"]), 1)
        self.assertEqual(friend_u3["net"][0]["currency"], "USD")
        self.assertAlmostEqual(abs(friend_u3["net"][0]["amount"]), 300.0, places=1)
        self.assertEqual(len(friend_u3["groups"][0]["you_owe"]), 1)
        self.assertEqual(len(friend_u3["groups"][0]["owed_to"]), 0)

    def test_non_minimized_balances_shows_individual_debts(self):
        """
        With minimize_balances=False, each debt is shown per counterparty.

        Same amounts as the minimized test (user2 pays 300, user3 pays 600).
        Non-minimized: user1 owes user2 100 USD and user3 200 USD separately,
        and user2 also owes user3 100 USD (3 distinct debt relationships).
        """
        UserHelpers.login_user(self.client, self.user1)
        group = GroupHelpers.create_group(creator=self.user1)
        GroupHelpers.add_user_to_group(group, self.user2)
        GroupHelpers.add_user_to_group(group, self.user3)
        GroupHelpers.add_expense(group, self.user2, amount=300.0, currency="USD")
        GroupHelpers.add_expense(group, self.user3, amount=600.0, currency="USD")

        response = self.client.get(reverse("splittime:api_friends_view"))
        self.assertEqual(response.status_code, 200)

        friend_u2 = self._get_friend(response.data, self.user2)
        friend_u3 = self._get_friend(response.data, self.user3)
        self.assertIsNotNone(friend_u2)
        self.assertIsNotNone(friend_u3)

        # user1 owes user2 100 USD (300/3)
        self.assertEqual(len(friend_u2["net"]), 1)
        self.assertEqual(friend_u2["net"][0]["currency"], "USD")
        self.assertAlmostEqual(friend_u2["net"][0]["amount"], -100.0, places=1)
        self.assertEqual(len(friend_u2["groups"][0]["you_owe"]), 1)
        self.assertEqual(len(friend_u2["groups"][0]["owed_to"]), 0)

        # user1 owes user3 200 USD (600/3)
        self.assertEqual(len(friend_u3["net"]), 1)
        self.assertEqual(friend_u3["net"][0]["currency"], "USD")
        self.assertAlmostEqual(friend_u3["net"][0]["amount"], -200.0, places=1)
        self.assertEqual(len(friend_u3["groups"][0]["you_owe"]), 1)
        self.assertEqual(len(friend_u3["groups"][0]["owed_to"]), 0)