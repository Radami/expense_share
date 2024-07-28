import datetime

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import UniqueConstraint
from django.utils import timezone

PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]
INTEGER_VALIDATOR = [MinValueValidator(0)]


class Group(models.Model):
    creator = models.ForeignKey(
        "auth.User", related_name="user_location", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    creation_date = models.DateTimeField("creation date")

    def __str__(self):
        return self.name

    def was_created_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=365) <= self.creation_date <= now

    def has_member(self, user):
        return user in [gm.member for gm in GroupMembership.objects.filter(group=self)]


class GroupMembership(models.Model):
    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["group", "member"], name="group_membership_uniqueness"
            )
        ]

    group = models.ForeignKey(
        Group, related_name="membership_group", on_delete=models.CASCADE
    )
    member = models.ForeignKey(
        "auth.User", related_name="membership_member", on_delete=models.DO_NOTHING
    )

    def __str__(self):
        return self.group.name + "-" + self.member.username


class Expense(models.Model):
    name = models.CharField(max_length=20)
    currency = models.CharField(max_length=3)
    amount = models.FloatField(max_length=9)
    group = models.ForeignKey(
        Group, related_name="expense_group", on_delete=models.CASCADE
    )
    creation_date = models.DateTimeField("creation_date")
    payee = models.ForeignKey(
        "auth.User", related_name="payee", on_delete=models.DO_NOTHING
    )

    def __str__(self):
        return self.name + " for " + str(self.amount) + " " + self.currency


class Debt(models.Model):
    class Meta:
        constraints = [
            UniqueConstraint(
                fields=[
                    "from_user",
                    "to_user",
                    "expense",
                ],
                name="one_debt_per_expense",
            )
        ]

    from_user = models.ForeignKey(
        "auth.User", related_name="from_user", on_delete=models.DO_NOTHING
    )
    to_user = models.ForeignKey(
        "auth.User", related_name="to_user", on_delete=models.DO_NOTHING
    )
    expense = models.ForeignKey(
        Expense, related_name="expense", on_delete=models.CASCADE
    )
    shares = models.IntegerField(validators=INTEGER_VALIDATOR)

    def __str__(self):
        relationship = self.from_user.username + " to " + self.to_user.username
        amount = (
            str(self.shares) + " of " + str(self.expense.amount) + self.expense.currency
        )
        return relationship + "=" + amount

    def __eq__(self, other):
        return (
            self.from_user.id == other.from_user.id
            and self.to_user.id == other.to_user.id
            and self.expense.id == other.expense.id
            and self.shares == other.shares
        )

    def __hash__(self):
        return super().__hash__()
