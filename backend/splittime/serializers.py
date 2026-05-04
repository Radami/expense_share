from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Group, GroupMembership, Expense, Debt
from .services.balances import BalanceCalculator


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email"]


class UserBalanceMixin:
    """Computes and caches per-request balance data shared by group serializers."""

    def _get_balances(self, obj):
        if not hasattr(self, '_balances_cache'):
            self._balances_cache = BalanceCalculator.calculateBalancesAPI(obj)
        return self._balances_cache

    def get_user_is_owed(self, obj):
        pair = BalanceCalculator.calculateUserIsOwed(obj.id, self.context["request"].user.id, True, self._get_balances(obj))
        if pair[0] == "XYZ" or pair[1] < 0:
            return "Nothing"
        return str(pair[0]) + " " + str("{0:.2f}".format(pair[1]))

    def get_user_owes(self, obj):
        pair = BalanceCalculator.calculateUserOwes(obj.id, self.context["request"].user.id, True, self._get_balances(obj))
        if pair[0] == "XYZ" or pair[1] < 0:
            return "Nothing"
        return str(pair[0]) + " " + str("{0:.2f}".format(pair[1]))


class GroupSerializer(UserBalanceMixin, serializers.ModelSerializer):

    creator = serializers.ReadOnlyField(source="creator.username")
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=100)
    creation_date = serializers.DateTimeField(read_only=True)
    user_is_owed = serializers.SerializerMethodField()
    user_owes = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = [
            "id",
            "creator",
            "name",
            "description",
            "creation_date",
            "user_is_owed",
            "user_owes",
        ]


class GroupDetailsSerializer(UserBalanceMixin, serializers.Serializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=100)
    creation_date = serializers.DateTimeField(read_only=True)
    minimize_balances_setting = serializers.BooleanField(read_only=True)
    user_is_owed = serializers.SerializerMethodField()
    user_owes = serializers.SerializerMethodField()

    group_members = serializers.SerializerMethodField()
    expenses = serializers.SerializerMethodField()
    totals = serializers.SerializerMethodField()
    balances = serializers.SerializerMethodField()
    minimized_balances = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = [
            "id",
            "name",
            "description",
            "creation_date",
            "minimize_balances_setting",
            "user_is_owed",
            "user_owes",
            "group_members",
            "expenses",
            "totals",
            "balances",
            "minimized_balances",
        ]

    def get_group_members(self, obj):
        group_memberships = GroupMembership.objects.filter(group=obj)
        return [
            {
                "id": gm.member.id,
                "username": gm.member.username,
                "email": gm.member.email,
            }
            for gm in group_memberships
        ]

    def get_expenses(self, obj):
        user = self.context["request"].user
        expenses = Expense.objects.filter(group=obj).order_by("creation_date")
        result = []
        for e in expenses.reverse():
            debt_set = list(Debt.objects.filter(expense=e))
            total_shares = sum(d.shares for d in debt_set)
            if total_shares > 0:
                user_debts = [
                    d for d in debt_set if d.from_user_id == user.id and d.to_user_id != user.id
                ]
                you_owe = sum(d.shares / total_shares * e.amount for d in user_debts)
            else:
                you_owe = 0
            result.append(
                {
                    "id": e.id,
                    "name": e.name,
                    "amount": e.amount,
                    "currency": e.currency,
                    "payee": e.payee.username,
                    "creation_date": e.creation_date,
                    "you_owe": round(you_owe, 2),
                }
            )
        return result

    def get_totals(self, obj):
        expenses = Expense.objects.filter(group=obj)
        totals = {}
        for e in expenses:
            if e.currency not in totals:
                totals[e.currency] = e.amount
            else:
                totals[e.currency] += e.amount
        return totals

    def get_balances(self, obj):
        return self._get_balances(obj)

    def get_minimized_balances(self, obj):
        return BalanceCalculator.calculateMinimizedDebts(obj, self._get_balances(obj))


class ExpenseSerializer(serializers.ModelSerializer):

    payee = serializers.SerializerMethodField()

    class Meta:
        model = Expense
        fields = ["id", "name", "currency", "amount", "group", "creation_date", "payee"]

    def get_payee(self, obj):
        return obj.payee.username  # Return only the username
