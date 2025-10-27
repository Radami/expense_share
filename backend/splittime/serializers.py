from django.contrib.auth.models import User

from rest_framework import serializers

from .models import Group, GroupMembership, Expense
from .services.balances import BalanceCalculator


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email"]


class GroupSerializer(serializers.ModelSerializer):

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

    def get_user_is_owed(self, obj):
        pair = BalanceCalculator.calculateUserIsOwed(obj.id, self.context["request"].user.id, True)
        if pair[0] == "XYZ" or pair[1] < 0:
            return "Nothing"
        return str(pair[0]) + " " + str("{0:.2f}".format(pair[1]))

    def get_user_owes(self, obj):
        pair = BalanceCalculator.calculateUserOwes(obj.id, self.context["request"].user.id, True)
        if pair[0] == "XYZ" or pair[1] < 0:
            return "Nothing"
        return str(pair[0]) + " " + str("{0:.2f}".format(pair[1]))


class GroupDetailsSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=100)
    creation_date = serializers.DateTimeField(read_only=True)

    group_members = serializers.SerializerMethodField()
    expenses = serializers.SerializerMethodField()
    totals = serializers.SerializerMethodField()
    balances = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = [
            "id",
            "name",
            "description",
            "creation_date",
            "group_members",
            "expenses",
            "totals",
            "balances",
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
        expenses = Expense.objects.filter(group=obj).order_by("creation_date")
        return [
            {
                "id": e.id,
                "name": e.name,
                "amount": e.amount,
                "currency": e.currency,
                "payee": e.payee.username,
                "creation_date": e.creation_date,
            }
            for e in expenses
        ]

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
        return BalanceCalculator.calculateBalancesAPI(obj)


class ExpenseSerializer(serializers.ModelSerializer):

    payee = serializers.SerializerMethodField()

    class Meta:
        model = Expense
        fields = ["id", "name", "currency", "amount", "group", "creation_date", "payee"]

    def get_payee(self, obj):
        return obj.payee.username  # Return only the username
