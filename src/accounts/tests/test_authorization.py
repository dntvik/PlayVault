import unittest
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import Client, TestCase
from django.urls import reverse


class TestAuthGamer(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            email="gamer@example.com", password="12345678", username="GamerUser", phone_number="+1234567890"
        )
        self.manager = get_user_model().objects.create_superuser(
            email="manager@example.com",
            password="12345678",
            username="ManagerUser",
            phone_number="+0987654321",
            is_staff=True,
        )

        def test_user_creation_with_duplicate_phone_number(self):
            with self.assertRaises(IntegrityError):
                get_user_model().objects.create_user(
                    email="another_gamer@example.com",
                    password="12345678",
                    username="AnotherGamer",
                    phone_number="+1234567890",
                )

    def test_user_login_wrong_email(self):
        user_login = self.client.login(email="wrong_email", password="12345678")
        self.assertFalse(user_login)

    def test_user_login_wrong_password(self):
        user_login = self.client.login(email="gamer@example.com", password="wrong_password")
        self.assertFalse(user_login)

    def test_user_access_admin_panel(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_manager_access_admin_panel(self):
        self.client.force_login(self.manager)
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    @unittest.skip("Index page will be implemented in week/spin 35")
    def test_user_access_index_page(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    @unittest.expectedFailure
    def test_manager_access_admin_panel_failure_expected(self):
        self.client.force_login(self.manager)
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, HTTPStatus.IM_A_TEAPOT)
