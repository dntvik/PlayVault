from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase


class UserModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="test@example.com", password="testpassword123", username="TestUser", phone_number="+1234567890"
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, "test@example.com")
        self.assertTrue(self.user.check_password("testpassword123"))
        self.assertEqual(self.user.username, "TestUser")
        self.assertEqual(str(self.user), self.user.email)

    def test_superuser_creation(self):
        admin_user = get_user_model().objects.create_superuser(email="admin@example.com", password="adminpassword")
        self.assertEqual(admin_user.email, "admin@example.com")
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

    def test_get_short_name(self):
        self.assertEqual(self.user.get_short_name(), "TestUser")

    def test_registration_duration(self):
        duration = self.user.get_registration_duration()
        self.assertIn("Time on site", duration)

    def test_username_unique(self):
        with self.assertRaises(IntegrityError):
            get_user_model().objects.create_user(
                email="another@example.com",
                password="password",
                username="TestUser",
            )

    def test_phone_number_unique(self):
        with self.assertRaises(IntegrityError):
            get_user_model().objects.create_user(
                email="another@example.com", password="password", username="AnotherUser", phone_number="+1234567890"
            )
