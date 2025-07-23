from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from ..models import Group, GroupMembership
from ..serializers import GroupSerializer, GroupDetailsSerializer, UserSerializer
from ..services.groups import GroupService
from ..services.balances import BalanceCalculator
from ..exceptions import DuplicateEntryException


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

        owes = {}
        is_owed = {}
        for group in latest_group_list:
            group_balance = BalanceCalculator.calculateBalancesAPI(group)
            for to_user in group_balance:
                if to_user == request.user.id:
                    # calculated all that request user is owed

                    for from_user in group_balance[to_user]:
                        for currency in group_balance[to_user][from_user]:
                            if currency not in is_owed:
                                is_owed[currency] = 0
                            is_owed[currency] = (
                                is_owed[currency] + group_balance[to_user][from_user][currency]
                            )
                else:
                    for from_user in group_balance[to_user]:
                        if to_user == request.user.id:
                            for currency in group_balance[to_user][from_user]:
                                if currency not in owes:
                                    owes[currency] = 0
                                owes[currency] = (
                                    owes[currency] + group_balance[to_user][from_user][currency]
                                )
                    # find if this user owes anything

        latest_group_list.sort(key=lambda x: x.creation_date, reverse=True)

        serializer = GroupSerializer(latest_group_list, many=True, context={"request": request})
        return Response(serializer.data)


class AddGroupView(APIView):
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def post(self, request):
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
            response_serializer = GroupSerializer(group, context={"request": request})
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
            group = Group.objects.get(pk=request.query_params.get("group_id"))
            if not group.has_member(request.user):
                return Response(
                    "You are not a member of this group.",
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            response_serializer = GroupDetailsSerializer(group)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response("Group not found", status=status.HTTP_404_NOT_FOUND)


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
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(status=status.HTTP_200_OK)


class AddGroupMemberAPIView(APIView):
    permission_classes = [IsAuthenticated]

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
        except DuplicateEntryException:
            return Response("User is already part of the group", status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response_serializer = UserSerializer(user)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
