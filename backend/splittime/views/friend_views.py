from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from ..models import GroupMembership
from ..services.balances import BalanceCalculator


class FriendsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        memberships = GroupMembership.objects.filter(member=user).select_related("group")
        friends_map = {}  # friend_id -> {user, groups, net}

        for membership in memberships:
            group = membership.group
            other_memberships = (
                GroupMembership.objects.filter(group=group)
                .exclude(member=user)
                .select_related("member")
            )

            if not other_memberships.exists():
                continue

            if group.minimize_balances_setting:
                transactions = BalanceCalculator.calculateMinimizedDebts(group)
            else:
                raw_balances = BalanceCalculator.calculateBalancesAPI(group)
                user_balances = raw_balances.get(user.id, {})

            for om in other_memberships:
                friend = om.member
                fid = friend.id

                if fid not in friends_map:
                    friends_map[fid] = {"user": friend, "groups": [], "net": {}}

                you_owe = []
                owed_to = []

                if group.minimize_balances_setting:
                    for t in transactions:
                        if t["from_user"] == fid and t["to_user"] == user.id:
                            owed_to.append({"currency": t["currency"], "amount": t["amount"]})
                            friends_map[fid]["net"][t["currency"]] = (
                                friends_map[fid]["net"].get(t["currency"], 0) + t["amount"]
                            )
                        elif t["from_user"] == user.id and t["to_user"] == fid:
                            you_owe.append({"currency": t["currency"], "amount": t["amount"]})
                            friends_map[fid]["net"][t["currency"]] = (
                                friends_map[fid]["net"].get(t["currency"], 0) - t["amount"]
                            )
                else:
                    friend_balance = user_balances.get(fid, {})
                    for currency, amount in friend_balance.items():
                        if abs(amount) < 0.005:
                            continue
                        if amount > 0:
                            owed_to.append({"currency": currency, "amount": round(amount, 2)})
                        else:
                            you_owe.append({"currency": currency, "amount": round(-amount, 2)})
                        friends_map[fid]["net"][currency] = (
                            friends_map[fid]["net"].get(currency, 0) + amount
                        )

                friends_map[fid]["groups"].append(
                    {
                        "id": group.id,
                        "name": group.name,
                        "you_owe": you_owe,
                        "owed_to": owed_to,
                    }
                )

        result = []
        for data in friends_map.values():
            net = [
                {"currency": c, "amount": round(a, 2)}
                for c, a in data["net"].items()
                if abs(a) >= 0.005
            ]
            result.append(
                {
                    "id": data["user"].id,
                    "username": data["user"].username,
                    "email": data["user"].email,
                    "net": net,
                    "groups": data["groups"],
                }
            )

        return Response(result, status=status.HTTP_200_OK)
