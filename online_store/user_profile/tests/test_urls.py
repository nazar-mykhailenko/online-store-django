from django.test import SimpleTestCase
from django.test.client import resolve
from django.urls import reverse

from user_profile.views import signup, log_out, profile, ChangePasswordView

class TestUrls(SimpleTestCase):
    def test_signup_url_is_resolved(self):
        # Arrange
        url = reverse('user_profile:signup')
        # Act
        resolved = resolve(url)
        # Assert
        self.assertEqual(resolved.func, signup)

    def test_logout_url_is_resolved(self):
        # Arrange
        url = reverse('user_profile:logout')
        # Act
        resolved = resolve(url)
        # Assert
        self.assertEqual(resolved.func, log_out)

    def test_profile_url_is_resolved(self):
        # Arrange
        url = reverse('user_profile:profile')
        # Act
        resolved = resolve(url)
        # Assert
        self.assertEqual(resolved.func, profile)

    def test_login_url_is_resolved(self):
        # Arrange
        url = reverse('user_profile:login')
        # Act
        resolved = resolve(url)
        # Assert
        self.assertEqual(resolved.func.view_class.__name__, 'LoginView')

    def test_change_password_url_is_resolved(self):
        # Arrange
        url = reverse('user_profile:change_password')
        # Act
        resolved = resolve(url)
        # Assert
        self.assertEqual(resolved.func.view_class, ChangePasswordView)
