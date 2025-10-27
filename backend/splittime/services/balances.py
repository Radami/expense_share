from ..models import Expense, Debt, Group


class BalanceCalculator:
    """
    Balances is building the graph relationship constructed by taking users as nodes, and debts as
    directed edges.

    Each entry represents a debt from the from_user to the to_user in the respective currency and
    for the respective amount. The value can be positive if there is a debt or negative if there is
    a surplus.

    To check the balance between 2 users, both entries need to be checked and the one with the
    positive value will indicate the direction of the debt

    """

    def calculateBalancesAPI(group):
        balances = {}
        expenses = Expense.objects.filter(group=group).order_by("creation_date")
        for e in expenses:
            debt_set = Debt.objects.filter(expense=e)
            for debt in debt_set:
                to_user = debt.to_user.id
                from_user = debt.from_user.id
                if to_user == from_user:
                    continue
                shares = sum([d.shares for d in debt_set])
                if to_user not in balances:
                    balances[to_user] = {}
                if from_user not in balances:
                    balances[from_user] = {}
                if debt.from_user.id not in balances[to_user]:
                    balances[to_user][from_user] = {}
                if debt.to_user.id not in balances[from_user]:
                    balances[from_user][to_user] = {}
                if e.currency not in balances[to_user][from_user]:
                    balances[to_user][from_user][e.currency] = 0
                if e.currency not in balances[from_user][to_user]:
                    balances[from_user][to_user][e.currency] = 0
                balances[to_user][from_user][e.currency] += debt.shares / shares * e.amount
                balances[from_user][to_user][e.currency] -= debt.shares / shares * e.amount
        return balances

    """
    calculateUserIsOwed returns the maximum absolute value and the currency that the user is owed.
    It uses Balances and calculates the maximum by setting the from_user to the current user and
    summing up every value, by currency

    If simplify is True, the balance will take add both positive and negative debts. If it is
    false, it will only add positive ones. For example, if a user owes 100 USD to user A and
    is owed 100 USD by user B, with simplify, the user is owed 0 but without, they owe 100.

    ("XYZ", 0) is the return value for the user not being owed anything
    """

    def calculateUserIsOwed(group_id: int, user_id: int, simplify: bool):
        group = Group.objects.get(id=group_id)
        balances = BalanceCalculator.calculateBalancesAPI(group)
        currencies = {}

        # TODO: Fix edge case where user is not in balances
        if user_id not in balances:
            return ("XYZ", 0)

        for from_user in balances[user_id]:
            for currency in balances[user_id][from_user]:
                if simplify is True:
                    if currency not in currencies:
                        currencies[currency] = 0
                    currencies[currency] = (
                        currencies[currency] + balances[user_id][from_user][currency]
                    )
                elif balances[user_id][from_user][currency] > 0:
                    if currency not in currencies:
                        currencies[currency] = 0
                    currencies[currency] = (
                        currencies[currency] + balances[user_id][from_user][currency]
                    )
        if len(currencies.items()) == 0:
            return ("XYZ", 0)

        has_positive = any(i[1] > 0 for i in currencies.items())
        has_negative = any(i[1] < 0 for i in currencies.items())

        if has_positive is True and has_negative is True:
            return max(currencies.items(), key=lambda item: item[1])
        else:
            return max(currencies.items(), key=lambda item: abs(item[1]))

    """
    calculateUserOwes returns the maximum absolute value and the currency that the user owes. It
    uses Balances to go through each individual user and sets the from_user as the current user.
    It then sums up everything by currency

    If simplify is True, the balance will take add both positive and negative debts. If it is
    false, it will only add positive ones. For example, if a user owes 100 USD to user A and
    is owed 100 USD by user B, with simplify, the user owes 0 but without, they owe 100.

    ("XYZ", 0) is the return value for the user not owing anything
    """

    def calculateUserOwes(group_id: int, user_id: int, simplify: bool):
        group = Group.objects.get(id=group_id)
        balances = BalanceCalculator.calculateBalancesAPI(group)
        currencies = {}

        for to_user in balances:
            if user_id not in balances[to_user]:
                continue
            for currency in balances[to_user][user_id]:
                if simplify is True:
                    if currency not in currencies:
                        currencies[currency] = 0
                    currencies[currency] = (
                        currencies[currency] + balances[to_user][user_id][currency]
                    )
                elif balances[to_user][user_id][currency] > 0:
                    if currency not in currencies:
                        currencies[currency] = 0
                    currencies[currency] = (
                        currencies[currency] + balances[to_user][user_id][currency]
                    )

        if len(currencies.items()) == 0:
            return ("XYZ", 0)

        has_positive = any(i[1] > 0 for i in currencies.items())
        has_negative = any(i[1] < 0 for i in currencies.items())

        if has_positive is True and has_negative is True:
            return max(currencies.items(), key=lambda item: item[1])
        else:
            return max(currencies.items(), key=lambda item: abs(item[1]))
