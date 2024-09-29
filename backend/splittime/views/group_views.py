from typing import Any
from datetime import datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import (
    HttpResponseRedirect,
    HttpResponseServerError,
    HttpResponseForbidden,
    HttpResponseNotFound,
)
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from ..models import Group, GroupMembership, Expense
from ..serializers import GroupSerializer, GroupDetailsSerializer, UserSerializer
from ..services.balances import BalanceCalculator
from ..services.groups import GroupService
from ..exceptions import DuplicateEntryException


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = "splittime/index.html"
    context_object_name = "latest_group_list"

    def get_queryset(self):
        """Returns empy as everything is populated by get_context_data"""
        return []

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        creation_date = timezone.make_aware(
            datetime.now() - timedelta(days=365), timezone.get_current_timezone()
        )
        group_memberships = GroupMembership.objects.filter(member=self.request.user)
        # latest_group_list = Group.objects.filter(creator=self.request.user).filter(
        #   creation_date__gte=creation_date).order_by("-creation_date")[:5]
        latest_group_list = [
            gm.group for gm in group_memberships if gm.group.creation_date >= creation_date
        ]
        latest_group_list.sort(key=lambda x: x.creation_date, reverse=True)
        context = {"latest_group_list": latest_group_list}
        return context


class GroupDetailsView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    model = Group
    template_name = "splittime/group_details.html"

    def test_func(self):
        try:
            group = Group.objects.get(pk=self.kwargs["pk"])
        except ObjectDoesNotExist as e:
            return HttpResponseNotFound(e)
        return group.has_member(self.request.user)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super(GroupDetailsView, self).get_context_data(**kwargs)
        group = Group.objects.get(pk=self.kwargs["pk"])
        group_memberships = GroupMembership.objects.filter(group=group)

        expenses = Expense.objects.filter(group=group).order_by("creation_date")

        totals = {}
        for e in expenses:
            if e.currency not in totals:
                totals[e.currency] = e.amount
                continue
            totals[e.currency] += e.amount

        balances = BalanceCalculator.calculateBalances(group)

        context = {
            "group": group,
            "group_members": group_memberships,
            "expenses": expenses,
            "totals": totals,
            "balances": balances,
        }
        return context


@login_required
def add_group(request):
    if request.method == "POST":
        group_data = {
            "name": request.POST["group_name"],
            "description": request.POST["group_description"],
            "creator": request.user,
        }
        group = Group()
        try:
            group = GroupService.add_group(group_data)
        except Exception as e:
            return HttpResponseServerError(e)
        return HttpResponseRedirect(reverse("splittime:group_details", args=(group.id,)))
    return HttpResponseRedirect(
        reverse(
            "splittime:index",
        )
    )


@login_required
def delete_group(request, pk):
    if request.method == "POST":
        group = get_object_or_404(Group, pk=pk)

        if group.creator.id != request.user.id:
            return HttpResponseForbidden()

        try:
            GroupService.delete_group(group)
        except Exception as e:
            return HttpResponseServerError(e)
    return HttpResponseRedirect(reverse("splittime:index"))


@login_required
def add_group_member(request, group_id):
    user = get_object_or_404(User, email=request.POST["member_email"])
    group = get_object_or_404(Group, pk=group_id)

    if not group.has_member(request.user):
        return HttpResponseForbidden()
    try:
        GroupService.add_group_member(group, user)
    except Exception as e:
        if type(e) is DuplicateEntryException:
            # messages.add_message(request, messages.INFO, "Member already added")
            return HttpResponseRedirect(reverse("splittime:group_details", args=(group.id,)))
        return HttpResponseServerError(e)
    return HttpResponseRedirect(reverse("splittime:group_details", args=(group.id,)))


@login_required
def delete_group_member(request, group_id, user_id):
    user = get_object_or_404(User, pk=user_id)
    group = get_object_or_404(Group, pk=group_id)
    gm = get_object_or_404(GroupMembership, member=user, group=group)

    if not group.has_member(request.user):
        return HttpResponseForbidden()
    try:
        GroupService.delete_group_member(gm)
    except Exception as e:
        return HttpResponseServerError(e)

    return HttpResponseRedirect(reverse("splittime:group_details", args=(group.id,)))


# Django Rest Framework views
class GroupIndexView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        creation_date = timezone.make_aware(
            datetime.now() - timedelta(days=365), timezone.get_current_timezone()
        )

        group_memberships = GroupMembership.objects.filter(member=request.user)

        latest_group_list = [
            gm.group for gm in group_memberships if gm.group.creation_date >= creation_date
        ]

        latest_group_list.sort(key=lambda x: x.creation_date, reverse=True)

        serializer = GroupSerializer(latest_group_list, many=True)
        return Response(serializer.data)


# Django Rest Framework views
class AddGroupView(APIView):
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def post(self, request):
        print(request.data)
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            # Extract validated data from serializer
            validated_data = serializer.validated_data
            # Add the current user as the creator
            group_data = {
                "name": validated_data.get("name"),
                "description": validated_data.get("description"),
                "creator": request.user,
            }

            # Use the GroupService to add the group
            group = GroupService.add_group(group_data)

            # Serialize the created group to return as response
            response_serializer = GroupSerializer(group)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteGroupView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        id = request.data["id"]
        group = get_object_or_404(Group, pk=id)

        if group.creator.id != request.user.id:
            return Response(
                "User doesn not have permission to delete the group",
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            GroupService.delete_group(group)
        except Exception as e:
            return Response(e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=status.HTTP_200_OK)


class GroupDetailsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            group = Group.objects.get(pk=request.query_params.get("groupId"))
            if not group.has_member(request.user):
                raise Response(
                    "You are not a member of this group.", status=status.HTTP_401_UNAUTHORIZED
                )
            response_serializer = GroupDetailsSerializer(group)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            raise Response("Group not found", status=status.HTTP_404_NOT_FOUND)


class DeleteGroupMemberAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = get_object_or_404(User, pk=request.data["user_id"])
        group = get_object_or_404(Group, pk=request.data["group_id"])
        gm = get_object_or_404(GroupMembership, member=user, group=group)

        if not group.has_member(request.user):
            return Response(
                "User does not have permission to delete members in this group",
                status=status.HTTP_403_FORBIDDEN,
            )

        if user.id == request.user.id:
            return Response(
                "self removal is forbidden for now",
                status=status.HTTP_403_FORBIDDEN,
            )
        try:
            GroupService.delete_group_member(gm)
        except Exception as e:
            return Response(e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(status=status.HTTP_200_OK)


class AddGroupMemberAPIView(APIView):

    def post(self, request):
        user = get_object_or_404(User, email=request.data["member_email"])
        group = get_object_or_404(Group, pk=request.data["group_id"])

        if not group.has_member(request.user):
            return Response(
                "User does not have permission to delete members in this group",
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            GroupService.add_group_member(group, user)
        except Exception as e:
            return Response(e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response_serializer = UserSerializer(user)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
