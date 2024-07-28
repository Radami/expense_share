from django.contrib import admin

from .models import Group, GroupMembership, Expense, Debt

# Register your models here.


class GroupMembershipInline(admin.TabularInline):
    model = GroupMembership
    extra = 3


class GroupAdmin(admin.ModelAdmin):
    fieldsets = [("Creation", {"fields": ["creator", "creation_date"]}),
                 ("Information", {"fields": ["name", "description"]})]
    # Display the option to add group members in the Group admin page
    inlines = [GroupMembershipInline]

    # Controls the fields being displayed in the admin index page
    list_display = ["name", "creation_date"]

    # Djanog creates a filter section based on this field
    list_filter = ["creation_date"]

    # Search box based on this field
    search_fields = ["name"]


admin.site.register(Group, GroupAdmin)
admin.site.register(Expense)
admin.site.register(Debt)
