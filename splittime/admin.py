from django.contrib import admin

from .models import Group, GroupMembership, Expense

# Register your models here.

admin.site.register(Group)
admin.site.register(GroupMembership)
admin.site.register(Expense)