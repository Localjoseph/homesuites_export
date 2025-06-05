from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Profile


class UserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )

    def test_profile_creation(self):
        """Test that a profile is created for a new user"""
        self.assertTrue(Profile.objects.filter(user=self.user).exists())

    def test_register_view(self):
        """Test the register view"""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        
    def test_profile_view(self):
        """Test that the profile view requires login"""
        response = self.client.get(reverse('profile'))
        self.assertNotEqual(response.status_code, 200)  # Should redirect to login
