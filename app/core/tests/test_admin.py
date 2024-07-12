# Tests for Django admin modifications

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client

class AdminSiteTests(TestCase):
    # Tests for Django admin

    # run before every test
    def setUp(self):
        # Create user and client.
        self.client = Client()
        # we have one admin user
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password="testpass123",
        )
        self.client.force_login(self.admin_user)
        # we have one normal user
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='testpass123',
            name="Test User"
        )

    def test_users_list(self):
        # Test that users are listed on page
        # using reverse() to get the url of the page with the list of users
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        # checking that page contains the name and email of our test user
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        # Test the edit user page works
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        # Test the create user page works
        url = reverse('admin:core_user_add')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)