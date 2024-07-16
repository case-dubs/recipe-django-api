# Tests for user API

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
# import logging
# Configure logging
# logging.basicConfig(level=logging.INFO)

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')

# **params argument gives us flexibility of providing a dictionary of any params we'd like
def create_user(**params):
    # Create and return a new user with whatever details we pass into parameters
    return get_user_model().objects.create_user(**params)

# Public tests - unathenticated requests / requests that don't require authication

class PublicUserApiTests(TestCase):
    # Test the public features of the user API

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        # Test creating a user is successful
        # Data we'll send to API post
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }

        # POST url we'll send registration data to
        res = self.client.post(CREATE_USER_URL, payload)

        # Testing that 201 created code is returned
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # Testing that object was created in database
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))

        # Make sure non-hashed password not sent back with user object
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        # Test error returned if user with email exists
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }

        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        # an error is returned if password less than 5 chars
        payload = {
            'email': 'test@example.com',
            'password': 'pw',
            'name': 'Test Name',
        }

        res = self.client.post(CREATE_USER_URL,payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        # Test generates token for valid credentials
        user_details = {
            'name': 'Test Name',
            'email': 'test@example.com',
            'password': 'test-user-password123',
        }
        create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': user_details['password'],
        }

        res = self.client.post(TOKEN_URL, payload)
        # checking that response includes a token
        self.assertIn('token', res.data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        # Test returns error if credentials invalid
        create_user(email='test@example.com', password='goodpass')
        payload = {'email': 'test@example.com', 'password': 'badpass'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        # Test posting a blank password return an error
        payload = {'email': 'test@example.com', 'password': ''}
        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)