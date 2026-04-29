import heapq

from ..models import Expense, Debt, Group


class BalanceCalculator:
    """
    Builds a balance graph where users are nodes and debts are directed edges.

    Structure: balances[creditor][debtor][currency] = amount
    - A positive amount means the creditor is owed that amount by the debtor.
    - Each edge has a corresponding negative mirror: balances[debtor][creditor][currency] = -amount.

    To find the net position of a user, sum all their outgoing edges across all counterparties.
    Positive sum = net creditor; negative sum = net debtor.
    """

    def calculateBalancesAPI(group):
        balances = {}
        expenses = Expense.objects.filter(group=group).order_by("creation_date")
        for expense in expenses:
            debt_set = Debt.objects.filter(expense=expense)
            total_shares = sum(d.shares for d in debt_set)
            for debt in debt_set:
                creditor = debt.to_user.id
                debtor = debt.from_user.id
                if creditor == debtor:
                    continue
                amount = debt.shares / total_shares * expense.amount

                if creditor not in balances:
                    balances[creditor] = {}
                if debtor not in balances:
                    balances[debtor] = {}
                if debtor not in balances[creditor]:
                    balances[creditor][debtor] = {}
                if creditor not in balances[debtor]:
                    balances[debtor][creditor] = {}
                if expense.currency not in balances[creditor][debtor]:
                    balances[creditor][debtor][expense.currency] = 0
                if expense.currency not in balances[debtor][creditor]:
                    balances[debtor][creditor][expense.currency] = 0

                balances[creditor][debtor][expense.currency] += amount
                balances[debtor][creditor][expense.currency] -= amount

        return balances

    def _computeGrossPositions(balances, user_id):
        """
        Returns (credits, debits) as {currency: amount} dicts for user_id.
        credits: gross amounts owed to user_id (positive outgoing edges).
        debits:  gross amounts user_id owes to others (negative outgoing edges, stored positive).
        Both are derived from the same single pass over balances[user_id].
        """
        credits = {}
        debits = {}
        for currencies in balances.get(user_id, {}).values():
            for currency, amount in currencies.items():
                if amount > 0:
                    credits[currency] = credits.get(currency, 0) + amount
                elif amount < 0:
                    debits[currency] = debits.get(currency, 0) - amount
        return credits, debits

    def _computeNetPositions(balances):
        """
        Returns {user_id: {currency: net_amount}} by summing all outgoing edges per user.
        Positive net = creditor (owed money); negative net = debtor (owes money).
        """
        net = {}
        for user_id, counterparties in balances.items():
            net[user_id] = {}
            for currencies in counterparties.values():
                for currency, amount in currencies.items():
                    net[user_id][currency] = net[user_id].get(currency, 0) + amount
        return net

    """
    calculateUserIsOwed returns the (currency, amount) pair representing the largest amount
    the user is owed across all counterparties.

    With simplify=True, positive and negative edges are summed together, so debts the user
    owes to others cancel against debts owed to them — giving a net position.
    With simplify=False, only positive edges are summed — the gross amount owed to the user,
    ignoring what they owe in return.

    Returns ("XYZ", 0) when the user is not owed anything.
    """

    def calculateUserIsOwed(group_id: int, user_id: int, simplify: bool):
        group = Group.objects.get(id=group_id)
        balances = BalanceCalculator.calculateBalancesAPI(group)
        currencies = {}

        # TODO: Fix edge case where user is not in balances
        if user_id not in balances:
            return ("XYZ", 0)

        if simplify is True:
            currencies = BalanceCalculator._computeNetPositions(balances).get(user_id, {})
        else:
            currencies, _ = BalanceCalculator._computeGrossPositions(balances, user_id)

        if len(currencies.items()) == 0:
            return ("XYZ", 0)

        has_positive = any(i[1] > 0 for i in currencies.items())
        has_negative = any(i[1] < 0 for i in currencies.items())

        if has_positive is True and has_negative is True:
            return max(currencies.items(), key=lambda item: item[1])
        else:
            return max(currencies.items(), key=lambda item: abs(item[1]))

    """
    calculateUserOwes returns the (currency, amount) pair representing the largest amount
    the user owes across all counterparties.

    With simplify=True, positive and negative edges cancel — giving the user's net debt position.
    With simplify=False, only edges where the user is the debtor are summed — the gross amount
    they owe, ignoring what others owe them in return.

    Returns ("XYZ", 0) when the user owes nothing.
    """

    def calculateUserOwes(group_id: int, user_id: int, simplify: bool):
        group = Group.objects.get(id=group_id)
        balances = BalanceCalculator.calculateBalancesAPI(group)
        currencies = {}

        if simplify is True:
            net = BalanceCalculator._computeNetPositions(balances)
            if user_id not in net:
                return ("XYZ", 0)
            # Outgoing edges give the creditor perspective; negate for the debtor perspective.
            currencies = {currency: -amount for currency, amount in net[user_id].items()}
        else:
            _, currencies = BalanceCalculator._computeGrossPositions(balances, user_id)

        if len(currencies.items()) == 0:
            return ("XYZ", 0)

        has_positive = any(i[1] > 0 for i in currencies.items())
        has_negative = any(i[1] < 0 for i in currencies.items())

        if has_positive is True and has_negative is True:
            return max(currencies.items(), key=lambda item: item[1])
        else:
            return max(currencies.items(), key=lambda item: abs(item[1]))

    """
    calculateMinimizedDebts returns the smallest possible list of payment transactions that
    fully settles all debts in the group.

    It works in two steps:
      1. Compute each user's net position per currency by summing all their edges in the balance
         graph. A positive net means the user is a creditor (owed money); negative means debtor.
      2. For each currency, greedily match the largest creditor with the largest debtor. Each
         match produces one transaction and eliminates at least one party. The remainder is pushed
         back and matched in the next round.

    Because it operates on net positions rather than individual edges, intermediate users whose
    debts cancel out are automatically bypassed — their net is zero, so they never appear in
    either heap and no transactions are generated for them.

    Returns a list of dicts: [{"from_user": int, "to_user": int, "currency": str, "amount": float}]
    """

    def calculateMinimizedDebts(group):
        balances = BalanceCalculator.calculateBalancesAPI(group)

        net = BalanceCalculator._computeNetPositions(balances)

        all_currencies = {c for user in net.values() for c in user}
        transactions = []

        for currency in all_currencies:
            # Max-heaps implemented via Python's min-heap with negated values.
            # Tiebreaking by user_id ensures deterministic output.
            creditors = []  # (-amount, user_id)
            debtors = []    # (amount, user_id)  —  amount is negative; most negative pops first

            for user_id, user_net in net.items():
                amount = user_net.get(currency, 0)
                if amount > 0.005:
                    heapq.heappush(creditors, (-amount, user_id))
                elif amount < -0.005:
                    heapq.heappush(debtors, (amount, user_id))

            while creditors and debtors:
                neg_credit, creditor = heapq.heappop(creditors)
                credit = -neg_credit
                neg_debt, debtor = heapq.heappop(debtors)
                debt = -neg_debt  # absolute value of what the debtor owes

                settled = min(credit, debt)
                transactions.append({
                    "from_user": debtor,
                    "to_user": creditor,
                    "currency": currency,
                    "amount": round(settled, 2),
                })

                remainder_credit = credit - settled
                remainder_debt = debt - settled
                if remainder_credit > 0.005:
                    heapq.heappush(creditors, (-remainder_credit, creditor))
                if remainder_debt > 0.005:
                    heapq.heappush(debtors, (-remainder_debt, debtor))

        return transactions
