from django.http import HttpResponse
from django.shortcuts import get_object_or_404,render

from .models import Group

def index(request):
    latest_group_list = Group.objects.order_by("-creation_date")[:5]
    context = {
        "latest_group_list": latest_group_list
    }
    return render(request, "splittime/index.html", context)

def group_details(request, group_id):
    group = get_object_or_404(Group, pk=group_id)
    context = {
        "group": group
    }
    return render(request, "splittime/group_details.html", context)

def expense_details(request, expense_id):
    return HttpResponse("You're looking at expense %s" % expense_id)

def add_expense(request):
    return HttpResponse("You are trying to add an expense")
    