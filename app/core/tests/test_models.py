# Tests for models

from django.test import TestCase
from django.contrib.auth import get_user_model

class ModelTests(TestCase):
    # Test models
    def test_create_user_with_email_successful(self):
        # Test creating a user with an email is successful
        # Recommends using example.com domain name when creating tests because example.com is reserved to be specifically used for testing. Not risking sending emails to real person
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))