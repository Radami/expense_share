from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status


class CreateUsersTest(APITestCase):
    def setUp(self):
        # We want to go ahead and originally create a user.
        self.test_user = User.objects.create_user("testuser", "test@example.com", "testpassword")

        # URL for creating an account.
        self.create_url = reverse("account_create")

    def test_create_user(self):
        """
        Ensure we can create a new user and a valid token is created with it.
        """
        data = {"username": "foobar", "email": "foobar@example.com", "password": "somepassword"}

        response = self.client.post(self.create_url, data, format="json")

        # We want to make sure we have two users in the database..
        self.assertEqual(User.objects.count(), 2)
        # And that we're returning a 201 created code.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Additionally, we want to return the username and email upon successful creation.
        self.assertEqual(response.data["username"], data["username"])
        self.assertEqual(response.data["email"], data["email"])
        self.assertFalse("password" in response.data)

    def test_create_user_with_short_password(self):
        """
        Ensure user is not created for password lengths less than 8.
        """
        data = {"username": "foobar", "email": "foobarbaz@example.com", "password": "foo"}

        response = self.client.post(self.create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data["password"]), 1)

    def test_create_user_with_no_password(self):
        data = {"username": "foobar", "email": "foobarbaz@example.com", "password": ""}

        response = self.client.post(self.create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data["password"]), 1)

    def test_create_user_with_too_long_username(self):
        data = {"username": "foo" * 30, "email": "foobarbaz@example.com", "password": "foobar"}

        response = self.client.post(self.create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data["username"]), 1)

    def test_create_user_with_no_username(self):
        data = {"username": "", "email": "foobarbaz@example.com", "password": "foobar"}

        response = self.client.post(self.create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data["username"]), 1)

    def test_create_user_with_preexisting_username(self):
        data = {"username": "testuser", "email": "user@example.com", "password": "testuser"}

        response = self.client.post(self.create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data["username"]), 1)

    def test_create_user_with_preexisting_email(self):
        data = {"username": "testuser2", "email": "test@example.com", "password": "testuser"}

        response = self.client.post(self.create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data["email"]), 1)

    def test_create_user_with_invalid_email(self):
        data = {"username": "foobarbaz", "email": "testing", "passsword": "foobarbaz"}

        response = self.client.post(self.create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data["email"]), 1)

    def test_create_user_with_no_email(self):
        data = {"username": "foobar", "email": "", "password": "foobarbaz"}

        response = self.client.post(self.create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data["email"]), 1)


class LoginUsersTests(APITestCase):
    def setUp(self):
        # We want to go ahead and originally create a user.
        self.test_user = User.objects.create_user("testuser", "test@example.com", "testpassword")
        self.invalid_user = "invalid_user"
        self.invalid_pass = "invalid_pass"
        self.invalid_token = "abc"

        # URL set-up
        self.token_obtain_url = reverse("token_obtain")
        self.token_verify_url = reverse("token_verify")

    def test_get_token_on_login_user(self):
        resp = self.client.post(
            self.token_obtain_url,
            {"username": self.test_user.username, "password": "testpassword"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue("access" in resp.data)
        self.assertTrue("refresh" in resp.data)

    def test_verify_token_on_login_user(self):
        resp = self.client.post(
            self.token_obtain_url,
            {"username": self.test_user.username, "password": "testpassword"},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue("access" in resp.data)
        self.assertTrue("refresh" in resp.data)
        access_token = resp.data["access"]
        refresh_token = resp.data["refresh"]

        resp = self.client.post(
            self.token_verify_url,
            {"token": access_token},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        resp = self.client.post(
            self.token_verify_url,
            {"token": refresh_token},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_verify_token_invalid_token(self):
        resp = self.client.post(
            self.token_verify_url,
            {"token": self.invalid_token},
            format="json",
        )
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_verify_token_on_invalid_username(self):
        resp = self.client.post(
            self.token_obtain_url,
            {"username": self.invalid_user, "password": self.invalid_pass},
            format="json",
        )

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_verify_token_on_invalid_password(self):
        resp = self.client.post(
            self.token_obtain_url,
            {"username": self.test_user.username, "password": self.invalid_pass},
            format="json",
        )

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
