from django.core.exceptions import PermissionDenied
from django.utils import timezone
from ..models import Expense, GroupMembership, Debt


class ExpenseService():

    def add_expense(expense_data):
        # Add an expense with the data from the POST request
        expense = Expense(name=expense_data["name"],
                          currency=expense_data["currency"],
                          amount=expense_data["amount"],
                          creation_date=timezone.now(),
                          group=expense_data["group"],
                          payee=expense_data["payee"])
        try:
            expense.save()
            # Add one debt relationship with each other member of the group
            members = GroupMembership.objects.filter(group=expense_data["group"])
            for group_member in members:
                debt = Debt()
                debt.from_user = group_member.member
                debt.to_user = expense.payee
                debt.expense = expense
                debt.shares = 1
                debt.save()
        except Exception as exception:
            print(exception)
            expense.delete()
            raise Exception
        return expense

    def delete_expense(expense, user):
        # Check if the user performing the delete is a member of the group,
        # otherwise error
        group = expense.group
        memberships = GroupMembership.objects.filter(group=group)
        found = [gm.member for gm in memberships if user == gm.member]
        if len(found) == 0:
            raise PermissionDenied()

        expense.delete()
