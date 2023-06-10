from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from apps.accounts.models import Account


class RegisterTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.data = {
            "email": "user@example.com",
            "username": "user",
            "password": "test1234",
            "birthdate": "1990-01-01",
            "first_name": "John",
            "last_name": "Doe",
        }

    def test_register(self):
        # Send POST request to endpoint without reverse
        url = "/accounts/register/register/"
        response = self.client.post(url, self.data)

        # Assert response status code and success message
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["success"], True)

        # Check if user was created successfully
        self.assertTrue(
            Account.objects.filter(
                email=self.data["email"],
                username=self.data["username"],
                birthdate=self.data["birthdate"],
                first_name=self.data["first_name"],
                last_name=self.data["last_name"],
            ).exists()
        )


class LoginTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = Account.objects.create_user(
            email="user@example.com",
            username="user",
            password="test1234",
            birthdate="1990-01-01",
            first_name="John",
            last_name="Doe",
        )

    def test_login(self):
        # Send POST request to endpoint without reverse
        url = "/accounts/users/login/"
        data = {
            "email": self.user.email,
            "password": "test1234",
        }
        response = self.client.post(url, data)

        # Assert response status code and success message
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["success"], True)

        # Check if user was logged in successfully
        self.assertTrue(response.data["token"])


class NewPasswordTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = Account.objects.create_user(
            email="username@example.com",
            username="username",
            password="test1234",
            birthdate="1990-01-01",
            first_name="John",
            last_name="Doe",
        )

    def test_change_password_without_verification_code(self):
        self.client.force_authenticate(user=self.user)

        # Send POST request to endpoint without reverse
        url = "/accounts/users/new_password/"
        data = {
            "id_user": self.user.id,
            "old_password": "test1234",
            "new_password": "newtest1234",
        }
        response = self.client.post(url, data)

        # Assert response status code and success message
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["success"], True)

        # Check if password was changed successfully
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newtest1234"))
