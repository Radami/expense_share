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

    class Meta:
        model = Group
        fields = ["id", "creator", "name", "description", "creation_date"]


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
            {"id": gm.member.id, "username": gm.member.username, "email": gm.member.email}
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
        return BalanceCalculator.calculateBalances(obj)
