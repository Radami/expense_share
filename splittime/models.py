from django.db import models

# Create your models here.

class Group(models.Model):
    creator = models.ForeignKey('auth.User', related_name='user_location',
                                on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)

class GroupMembership(models.Model):
    group = models.ForeignKey(Group, related_name='location', on_delete=models.CASCADE)
    member = models.ForeignKey('auth.User', related_name='user_location', 
                               on_delete=models.CASCADE)
