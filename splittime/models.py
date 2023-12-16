import datetime

from django.db import models
from django.utils import timezone
from django.db.models import UniqueConstraint

# Create your models here.

class Group(models.Model):
    creator = models.ForeignKey('auth.User', related_name='user_location',
                                on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    creation_date = models.DateTimeField("creation date")

    def __str__(self):
        return self.name
    
    def was_created_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=7) <= self.creation_date <= now

class GroupMembership(models.Model):

    class Meta:
        constraints = [
            UniqueConstraint(fields=['group', 'member'], name = 'group_membership_uniqueness')]
    
    group = models.ForeignKey(Group, related_name='membership_group', on_delete=models.CASCADE)
    member = models.ForeignKey('auth.User', related_name='membership_member', 
                               on_delete=models.CASCADE)
    
    def __str__(self):
        return self.group.name + "-" + self.member.username
    
class Expense(models.Model):
    name = models.CharField(max_length=20)
    currency = models.CharField(max_length=3)
    amount = models.FloatField(max_length=9)
    group = models.ForeignKey(Group, related_name='expense_group', on_delete=models.CASCADE)

    def __str__(self):
        return self.name + " for " + str(self.amount) + " " + self.currency

