from unittest.mock import patch

from django.db import transaction
from django.test import TestCase

from splittime.exceptions import DuplicateEntryException
from splittime.models import GroupMembership
from splittime.services.groups import GroupService
from ..helpers import GroupHelpers, UserHelpers


class GroupServiceExceptionTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = UserHelpers.create_user(user_name="gs_exc_u1")
        cls.user2 = UserHelpers.create_user(user_name="gs_exc_u2")
        cls.group = GroupHelpers.create_group(creator=cls.user)

    def test_add_group_propagates_save_error(self):
        """If group.save() raises, the exception is re-raised"""
        group_data = {
            "name": "Fail Group",
            "description": "desc",
            "creation_date": None,
            "creator": self.user,
        }
        with patch("splittime.models.Group.save", side_effect=Exception("db error")):
            with self.assertRaises(Exception):
                GroupService.add_group(group_data)

    def test_delete_group_propagates_error(self):
        """If group.delete() raises, the exception is re-raised"""
        group = GroupHelpers.create_group(creator=self.user)
        with patch.object(group, "delete", side_effect=Exception("db error")):
            with self.assertRaises(Exception):
                GroupService.delete_group(group)

    @transaction.atomic
    def test_add_group_member_duplicate_raises_duplicate_exception(self):
        """Adding the same member twice raises DuplicateEntryException"""
        with transaction.atomic():
            with self.assertRaises(DuplicateEntryException):
                GroupService.add_group_member(self.group, self.user)

    def test_add_group_member_non_integrity_error_propagates(self):
        """Non-IntegrityError from gm.save() is re-raised as generic Exception"""
        with patch("splittime.models.GroupMembership.save", side_effect=Exception("unexpected")):
            with self.assertRaises(Exception):
                GroupService.add_group_member(self.group, self.user2)

    def test_delete_group_member_propagates_error(self):
        """If group_membership.delete() raises, the exception is re-raised"""
        gm = GroupMembership.objects.get(group=self.group, member=self.user)
        with patch.object(gm, "delete", side_effect=Exception("db error")):
            with self.assertRaises(Exception):
                GroupService.delete_group_member(gm)