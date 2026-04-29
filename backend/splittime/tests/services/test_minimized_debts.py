from django.test import TestCase

from ..helpers import GroupHelpers, UserHelpers
from splittime.services.balances import BalanceCalculator


def as_set(transactions):
    """Convert a transaction list to a set of tuples for order-independent comparison."""
    return {(t["from_user"], t["to_user"], t["currency"], t["amount"]) for t in transactions}


class MinimizedDebts2UsersTests(TestCase):
    """
    Two-member group: user1 (creator, auto-added) and user2.
    These tests cover the base cases: no debt, one-directional debt, and mutual
    cancellation, as well as multiple currencies being handled independently.
    """

    def setUp(self):
        self.user1 = UserHelpers.create_user()
        self.user2 = UserHelpers.create_user()
        self.group = GroupHelpers.create_group(creator=self.user1)
        GroupHelpers.add_user_to_group(self.group, self.user2)

    def test_no_expenses_returns_empty(self):
        # No expenses have been added, so there is nothing to settle.
        result = BalanceCalculator.calculateMinimizedDebts(self.group)
        self.assertEqual(result, [])

    def test_one_payer_one_transaction(self):
        # user1 pays $100, split equally between 2 members = $50 each.
        # Net: user1 = +$50 (creditor), user2 = -$50 (debtor).
        # Expected: 1 transaction — user2 pays user1 $50.
        GroupHelpers.add_expense(self.group, self.user1, amount=100, currency="USD")

        result = BalanceCalculator.calculateMinimizedDebts(self.group)

        self.assertEqual(len(result), 1)
        self.assertEqual(as_set(result), {
            (self.user2.id, self.user1.id, "USD", 50.0),
        })

    def test_equal_mutual_payments_cancel_to_zero(self):
        # user1 pays $100, user2 pays $100 — each half of the other's expense.
        # Net: user1 = +$50 - $50 = 0, user2 = -$50 + $50 = 0.
        # Expected: no transactions needed.
        GroupHelpers.add_expense(self.group, self.user1, amount=100, currency="USD")
        GroupHelpers.add_expense(self.group, self.user2, amount=100, currency="USD")

        result = BalanceCalculator.calculateMinimizedDebts(self.group)

        self.assertEqual(result, [])

    def test_unequal_mutual_payments_net_to_one_transaction(self):
        # user1 pays $200 (user2 owes $100), user2 pays $100 (user1 owes $50).
        # Net: user1 = +$100 - $50 = +$50, user2 = -$100 + $50 = -$50.
        # Expected: 1 transaction — user2 pays user1 the net difference of $50.
        GroupHelpers.add_expense(self.group, self.user1, amount=200, currency="USD")
        GroupHelpers.add_expense(self.group, self.user2, amount=100, currency="USD")

        result = BalanceCalculator.calculateMinimizedDebts(self.group)

        self.assertEqual(len(result), 1)
        self.assertEqual(as_set(result), {
            (self.user2.id, self.user1.id, "USD", 50.0),
        })

    def test_two_currencies_handled_independently(self):
        # user1 pays $100 USD: net USD user1 = +$50, user2 = -$50.
        # user2 pays £100 GBP: net GBP user1 = -£50, user2 = +£50.
        # Currencies cannot offset each other, so two separate transactions are needed.
        # Expected: user2 → user1 for USD, user1 → user2 for GBP.
        GroupHelpers.add_expense(self.group, self.user1, amount=100, currency="USD")
        GroupHelpers.add_expense(self.group, self.user2, amount=100, currency="GBP")

        result = BalanceCalculator.calculateMinimizedDebts(self.group)

        self.assertEqual(len(result), 2)
        self.assertEqual(as_set(result), {
            (self.user2.id, self.user1.id, "USD", 50.0),
            (self.user1.id, self.user2.id, "GBP", 50.0),
        })


class MinimizedDebts3UsersTests(TestCase):
    """
    Three-member group: user1 (creator), user2, user3.
    These tests cover chain collapse, full cancellation, net-zero user bypass,
    and multiple currencies.
    """

    def setUp(self):
        self.user1 = UserHelpers.create_user()
        self.user2 = UserHelpers.create_user()
        self.user3 = UserHelpers.create_user()
        self.group = GroupHelpers.create_group(creator=self.user1)
        GroupHelpers.add_user_to_group(self.group, self.user2)
        GroupHelpers.add_user_to_group(self.group, self.user3)

    def test_one_payer_two_debtors(self):
        # user1 pays $300, split 3 ways = $100 each.
        # Net: user1 = +$200 (creditor), user2 = -$100, user3 = -$100.
        # Expected: 2 transactions — each debtor pays user1 directly.
        GroupHelpers.add_expense(self.group, self.user1, amount=300, currency="USD")

        result = BalanceCalculator.calculateMinimizedDebts(self.group)

        self.assertEqual(len(result), 2)
        self.assertEqual(as_set(result), {
            (self.user2.id, self.user1.id, "USD", 100.0),
            (self.user3.id, self.user1.id, "USD", 100.0),
        })

    def test_all_equal_payers_cancel_to_zero(self):
        # Each user pays $300. Every user owes $100 per expense × 3 expenses = $300.
        # Each user is also owed $200 by the other two (from their own expense).
        # Net: user1 = user2 = user3 = +$200 - $100 - $100 = $0.
        # Expected: no transactions needed.
        GroupHelpers.add_expense(self.group, self.user1, amount=300, currency="USD")
        GroupHelpers.add_expense(self.group, self.user2, amount=300, currency="USD")
        GroupHelpers.add_expense(self.group, self.user3, amount=300, currency="USD")

        result = BalanceCalculator.calculateMinimizedDebts(self.group)

        self.assertEqual(result, [])

    def test_non_payer_settles_directly_with_both_creditors(self):
        # user1 and user2 each pay $300. user3 pays nothing.
        # From user1's expense: user3 owes user1 $100, and user2 owes user1 $100 (cancelled by expense 2).
        # From user2's expense: user3 owes user2 $100, and user1 owes user2 $100 (cancelled by expense 1).
        # Net: user1 = +$100, user2 = +$100, user3 = -$200.
        # Expected: user3 pays user1 $100 and user2 $100 directly — no chain.
        GroupHelpers.add_expense(self.group, self.user1, amount=300, currency="USD")
        GroupHelpers.add_expense(self.group, self.user2, amount=300, currency="USD")

        result = BalanceCalculator.calculateMinimizedDebts(self.group)

        self.assertEqual(len(result), 2)
        self.assertEqual(as_set(result), {
            (self.user3.id, self.user1.id, "USD", 100.0),
            (self.user3.id, self.user2.id, "USD", 100.0),
        })

    def test_net_zero_middleman_is_bypassed(self):
        # user1 pays $300, user2 pays $600, user3 pays $900 — each split 3 ways.
        # Raw debts would be: user1→user2 $100, user1→user3 $300, user2→user3 $100 (3 transactions).
        # Net positions: user1 = +$200 - $200 - $300 = -$300, user2 = -$100 + $400 - $300 = $0, user3 = -$100 - $200 + $600 = +$300.
        # user2 is a net-zero middleman and is bypassed entirely.
        # Expected: 1 transaction — user1 pays user3 $300 directly.
        GroupHelpers.add_expense(self.group, self.user1, amount=300, currency="USD")
        GroupHelpers.add_expense(self.group, self.user2, amount=600, currency="USD")
        GroupHelpers.add_expense(self.group, self.user3, amount=900, currency="USD")

        result = BalanceCalculator.calculateMinimizedDebts(self.group)

        self.assertEqual(len(result), 1)
        self.assertEqual(as_set(result), {
            (self.user1.id, self.user3.id, "USD", 300.0),
        })

    def test_sole_debtor_pays_both_creditors(self):
        # user2 and user3 each pay $300. user1 pays nothing.
        # Net: user1 = -$200 (owes $100 to each), user2 = +$100, user3 = +$100.
        # Expected: user1 pays user2 $100 and user3 $100 directly.
        GroupHelpers.add_expense(self.group, self.user2, amount=300, currency="USD")
        GroupHelpers.add_expense(self.group, self.user3, amount=300, currency="USD")

        result = BalanceCalculator.calculateMinimizedDebts(self.group)

        self.assertEqual(len(result), 2)
        self.assertEqual(as_set(result), {
            (self.user1.id, self.user2.id, "USD", 100.0),
            (self.user1.id, self.user3.id, "USD", 100.0),
        })

    def test_two_currencies_settled_independently(self):
        # user1 pays $300 USD: net USD user1 = +$200, user2 = -$100, user3 = -$100.
        # user3 pays £300 GBP: net GBP user3 = +£200, user1 = -£100, user2 = -£100.
        # The two currencies are settled with separate transactions and cannot cancel each other.
        # Expected: 4 transactions total — 2 USD (user2→user1, user3→user1), 2 GBP (user1→user3, user2→user3).
        GroupHelpers.add_expense(self.group, self.user1, amount=300, currency="USD")
        GroupHelpers.add_expense(self.group, self.user3, amount=300, currency="GBP")

        result = BalanceCalculator.calculateMinimizedDebts(self.group)

        self.assertEqual(len(result), 4)
        self.assertEqual(as_set(result), {
            (self.user2.id, self.user1.id, "USD", 100.0),
            (self.user3.id, self.user1.id, "USD", 100.0),
            (self.user1.id, self.user3.id, "GBP", 100.0),
            (self.user2.id, self.user3.id, "GBP", 100.0),
        })


class MinimizedDebts4UsersTests(TestCase):
    """
    Four-member group: user1 (creator), user2, user3, user4.
    These tests cover multi-debtor scenarios, symmetric creditor/debtor pairs that
    settle independently, chain collapse, and a debtor making multiple payments.
    """

    def setUp(self):
        self.user1 = UserHelpers.create_user()
        self.user2 = UserHelpers.create_user()
        self.user3 = UserHelpers.create_user()
        self.user4 = UserHelpers.create_user()
        self.group = GroupHelpers.create_group(creator=self.user1)
        GroupHelpers.add_user_to_group(self.group, self.user2)
        GroupHelpers.add_user_to_group(self.group, self.user3)
        GroupHelpers.add_user_to_group(self.group, self.user4)

    def test_one_payer_three_debtors(self):
        # user4 pays $400, split 4 ways = $100 each.
        # Net: user4 = +$300 (creditor), user1 = user2 = user3 = -$100 (debtors).
        # Expected: 3 transactions — each debtor pays user4 $100.
        GroupHelpers.add_expense(self.group, self.user4, amount=400, currency="USD")

        result = BalanceCalculator.calculateMinimizedDebts(self.group)

        self.assertEqual(len(result), 3)
        self.assertEqual(as_set(result), {
            (self.user1.id, self.user4.id, "USD", 100.0),
            (self.user2.id, self.user4.id, "USD", 100.0),
            (self.user3.id, self.user4.id, "USD", 100.0),
        })

    def test_two_creditor_debtor_pairs_settle_independently(self):
        # user1 pays $200 and user4 pays $200 — the group has two symmetric payers.
        # From user1's expense: user2, user3, user4 each owe user1 $50.
        # From user4's expense: user1, user2, user3 each owe user4 $50.
        # Net: user1 = +$150 - $50 = +$100, user4 = +$150 - $50 = +$100,
        #      user2 = -$50 - $50 = -$100, user3 = -$50 - $50 = -$100.
        # The two creditor-debtor pairs can be matched directly with no cross-settling.
        # Expected: user2 → user1 $100, user3 → user4 $100.
        GroupHelpers.add_expense(self.group, self.user1, amount=200, currency="USD")
        GroupHelpers.add_expense(self.group, self.user4, amount=200, currency="USD")

        result = BalanceCalculator.calculateMinimizedDebts(self.group)

        self.assertEqual(len(result), 2)
        self.assertEqual(as_set(result), {
            (self.user2.id, self.user1.id, "USD", 100.0),
            (self.user3.id, self.user4.id, "USD", 100.0),
        })

    def test_chain_of_four_collapses_to_two_transactions(self):
        # Expenses increase by $400 per payer: user1=$400, user2=$800, user3=$1200, user4=$1600.
        # Each split 4 ways ($100, $200, $300, $400 per member respectively).
        # Net per user (sum of what they're owed minus what they owe across all expenses):
        #   user1 = +$300 - $200 - $300 - $400 = -$600 (biggest debtor)
        #   user2 = -$100 + $600 - $300 - $400 = -$200 (smaller debtor)
        #   user3 = -$100 - $200 + $900 - $400 = +$200 (smaller creditor)
        #   user4 = -$100 - $200 - $300 + $1200 = +$600 (biggest creditor)
        # The greedy match pairs the largest debtor with the largest creditor:
        # Expected: user1 → user4 $600, user2 → user3 $200 — 2 transactions instead of 12 raw debts.
        GroupHelpers.add_expense(self.group, self.user1, amount=400, currency="USD")
        GroupHelpers.add_expense(self.group, self.user2, amount=800, currency="USD")
        GroupHelpers.add_expense(self.group, self.user3, amount=1200, currency="USD")
        GroupHelpers.add_expense(self.group, self.user4, amount=1600, currency="USD")

        result = BalanceCalculator.calculateMinimizedDebts(self.group)

        self.assertEqual(len(result), 2)
        self.assertEqual(as_set(result), {
            (self.user1.id, self.user4.id, "USD", 600.0),
            (self.user2.id, self.user3.id, "USD", 200.0),
        })

    def test_debtor_makes_two_payments_when_no_single_creditor_can_absorb_full_debt(self):
        # user3 pays $400 (each member owes $100) and user4 pays $600 (each member owes $150).
        # Net:
        #   user1 = -$100 - $150 = -$250 (largest debtor)
        #   user2 = -$100 - $150 = -$250 (largest debtor, tied with user1)
        #   user3 = +$300 - $150 = +$150 (smaller creditor)
        #   user4 = -$100 + $450 = +$350 (larger creditor)
        # Neither creditor alone can absorb all of user1's or user2's debt.
        # Greedy matching: user4(+350) vs user1(-250) → user1→user4 $250. user4 has $100 left.
        #                  user3(+150) vs user2(-250) → user2→user3 $150. user2 has $100 left.
        #                  user4(+100) vs user2(-100) → user2→user4 $100. All settled.
        # user2 ends up making 2 separate payments (to user3 and user4).
        GroupHelpers.add_expense(self.group, self.user3, amount=400, currency="USD")
        GroupHelpers.add_expense(self.group, self.user4, amount=600, currency="USD")

        result = BalanceCalculator.calculateMinimizedDebts(self.group)

        self.assertEqual(len(result), 3)
        self.assertEqual(as_set(result), {
            (self.user1.id, self.user4.id, "USD", 250.0),
            (self.user2.id, self.user3.id, "USD", 150.0),
            (self.user2.id, self.user4.id, "USD", 100.0),
        })


class MinimizedDebts5UsersTests(TestCase):
    """
    Five-member group: user1 (creator), user2, user3, user4, user5.
    These tests cover large debtee fan-out, full cancellation, multi-user chain
    collapse with bypassed middlemen, and a complex split between two creditors
    and three debtors.
    """

    def setUp(self):
        self.user1 = UserHelpers.create_user()
        self.user2 = UserHelpers.create_user()
        self.user3 = UserHelpers.create_user()
        self.user4 = UserHelpers.create_user()
        self.user5 = UserHelpers.create_user()
        self.group = GroupHelpers.create_group(creator=self.user1)
        GroupHelpers.add_user_to_group(self.group, self.user2)
        GroupHelpers.add_user_to_group(self.group, self.user3)
        GroupHelpers.add_user_to_group(self.group, self.user4)
        GroupHelpers.add_user_to_group(self.group, self.user5)

    def test_one_payer_four_debtors(self):
        # user5 pays $500, split 5 ways = $100 each.
        # Net: user5 = +$400, user1 = user2 = user3 = user4 = -$100.
        # Expected: 4 transactions — each debtor pays user5 $100.
        GroupHelpers.add_expense(self.group, self.user5, amount=500, currency="USD")

        result = BalanceCalculator.calculateMinimizedDebts(self.group)

        self.assertEqual(len(result), 4)
        self.assertEqual(as_set(result), {
            (self.user1.id, self.user5.id, "USD", 100.0),
            (self.user2.id, self.user5.id, "USD", 100.0),
            (self.user3.id, self.user5.id, "USD", 100.0),
            (self.user4.id, self.user5.id, "USD", 100.0),
        })

    def test_all_equal_payers_cancel_to_zero(self):
        # Each user pays $500. Each person's share of every expense is $100,
        # so each owes $400 total (across the other 4 expenses) and is owed
        # $400 total (the other 4 members' shares of their own expense).
        # Net: every user = +$400 - $400 = $0.
        # Expected: no transactions needed.
        GroupHelpers.add_expense(self.group, self.user1, amount=500, currency="USD")
        GroupHelpers.add_expense(self.group, self.user2, amount=500, currency="USD")
        GroupHelpers.add_expense(self.group, self.user3, amount=500, currency="USD")
        GroupHelpers.add_expense(self.group, self.user4, amount=500, currency="USD")
        GroupHelpers.add_expense(self.group, self.user5, amount=500, currency="USD")

        result = BalanceCalculator.calculateMinimizedDebts(self.group)

        self.assertEqual(result, [])

    def test_two_middlemen_bypassed_leaving_two_transactions(self):
        # Expenses increase by $500 per payer: user1=$500, user2=$1000, user3=$1500, user4=$2000, user5=$2500.
        # Each split 5 ways ($100, $200, $300, $400, $500 per member respectively).
        # Net per user:
        #   user1 = +$400 - $200 - $300 - $400 - $500 = -$1000 (biggest debtor)
        #   user2 = -$100 + $800 - $300 - $400 - $500 = -$500  (smaller debtor)
        #   user3 = -$100 - $200 + $1200 - $400 - $500 = $0    (net-zero, bypassed)
        #   user4 = -$100 - $200 - $300 + $1600 - $500 = +$500 (smaller creditor)
        #   user5 = -$100 - $200 - $300 - $400 + $2000 = +$1000(biggest creditor)
        # user3 nets to zero and generates no transactions.
        # Greedy: user5(+1000) vs user1(-1000) → user1→user5 $1000. Both settled.
        #         user4(+500) vs user2(-500)   → user2→user4 $500. Both settled.
        # Expected: 2 transactions, user3 completely absent.
        GroupHelpers.add_expense(self.group, self.user1, amount=500, currency="USD")
        GroupHelpers.add_expense(self.group, self.user2, amount=1000, currency="USD")
        GroupHelpers.add_expense(self.group, self.user3, amount=1500, currency="USD")
        GroupHelpers.add_expense(self.group, self.user4, amount=2000, currency="USD")
        GroupHelpers.add_expense(self.group, self.user5, amount=2500, currency="USD")

        result = BalanceCalculator.calculateMinimizedDebts(self.group)

        self.assertEqual(len(result), 2)
        self.assertEqual(as_set(result), {
            (self.user1.id, self.user5.id, "USD", 1000.0),
            (self.user2.id, self.user4.id, "USD", 500.0),
        })
        # Verify user3 is not involved in any transaction
        user3_txs = [t for t in result if self.user3.id in (t["from_user"], t["to_user"])]
        self.assertEqual(user3_txs, [])

    def test_two_creditors_three_debtors_four_transactions(self):
        # user4 pays $500 (each owes $100) and user5 pays $250 (each owes $50).
        # Net:
        #   user1 = -$100 - $50 = -$150 (debtor)
        #   user2 = -$100 - $50 = -$150 (debtor, tied with user1)
        #   user3 = -$100 - $50 = -$150 (debtor, tied with user1 and user2)
        #   user4 = +$400 - $50  = +$350 (larger creditor)
        #   user5 = -$100 + $200 = +$100 (smaller creditor)
        # Three debtors at -$150 each, two creditors at +$350 and +$100.
        # Greedy (debtors pop in user_id order due to tie):
        #   user4(+350) vs user1(-150) → user1→user4 $150.  user4 has $200 left.
        #   user4(+200) vs user2(-150) → user2→user4 $150.  user4 has $50 left.
        #   user5(+100) vs user3(-150) → user3→user5 $100.  user3 has $50 left.
        #   user4(+50)  vs user3(-50)  → user3→user4 $50.   All settled.
        # user3 makes two separate payments (to user5 then user4).
        GroupHelpers.add_expense(self.group, self.user4, amount=500, currency="USD")
        GroupHelpers.add_expense(self.group, self.user5, amount=250, currency="USD")

        result = BalanceCalculator.calculateMinimizedDebts(self.group)

        self.assertEqual(len(result), 4)
        self.assertEqual(as_set(result), {
            (self.user1.id, self.user4.id, "USD", 150.0),
            (self.user2.id, self.user4.id, "USD", 150.0),
            (self.user3.id, self.user5.id, "USD", 100.0),
            (self.user3.id, self.user4.id, "USD", 50.0),
        })
