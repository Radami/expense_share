from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from ..models import Group, Expense
from ..services.expenses import ExpenseService
from ..serializers import ExpenseSerializer


class AddExpenseAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        group = get_object_or_404(Group, pk=request.data["group_id"])
        payee = get_object_or_404(User, pk=request.data["payee"])

        if not group.has_member(request.user):
            return Response(
                "User does not have permission to delete members in this group",
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            # Add an expense with the data from the POST request
            expense = {
                "name": request.data["name"],
                "currency": request.data["currency"],
                "amount": request.data["amount"],
                "creation_date": timezone.now(),
                "group": group,
                "payee": payee,
            }
            saved_expense = ExpenseService.add_expense(expense)
        except Exception as exception:
            print("AddExpenseAPIViewExpection", exception)
            return Response(str(exception), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        response_serializer = ExpenseSerializer(saved_expense)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class DeleteExpenseAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        expense = get_object_or_404(Expense, pk=request.data["expense_id"])

        if not expense.group.has_member(request.user):
            return Response(
                "User does not have permission to delete expenses in this group",
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            ExpenseService.delete_expense(expense, request.user)
        except Exception as exception:
            print("DeleteExpenseException", exception)
            return Response(str(exception), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(status=status.HTTP_200_OK)
