from rest_framework import serializers

from .models import Group


class GroupSerializer(serializers.ModelSerializer):

    creator = serializers.ReadOnlyField(source="creator.username")
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=100)
    creation_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Group
        fields = ["id", "creator", "name", "description", "creation_date"]
