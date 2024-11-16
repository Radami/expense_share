from ..models import Expense, Debt


class BalanceCalculator:

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
