from django.urls import reverse
from django.test import TestCase, Client

from .helpers import GroupHelpers, UserHelpers


class GroupMembershipViewTests(TestCase):

    def setUp(self):
        self.user1 = UserHelpers.create_user(user_name="user1") # creator
        self.user2 = UserHelpers.create_user(user_name="user2") # member
        self.user3 = UserHelpers.create_user(user_name="user3") # outsider
        self.group1 = GroupHelpers.create_group(creator=self.user1)

    def test_add_group_memmber_as_creator(self):
        self.assertEqual(self.client.login(username=self.user1.username, password="glassonion123"), True)

    def test_add_group_member_as_member(self):
        pass

    def test_add_group_member_as_outsider(self):
        pass