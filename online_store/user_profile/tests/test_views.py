from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse


class TestViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test', 'test@test.com', 'somepassword')
        self.client = Client()
        self.client.login(username='test', password='somepassword')

    def test_signup_returns_correct_template(self):
        # Arrange
        url = reverse('user_profile:signup')
        # Act
        response = self.client.get(url)
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login/signup.html')

    def test_logout_redirects_to_index(self):
        # Arrange
        url = reverse('user_profile:logout')
        expected_url_to_redirect_to = reverse('core:index')
        # Act
        response = self.client.get(url)
        # Assert
        self.assertRedirects(response, expected_url_to_redirect_to)

    def test_profile_returns_correct_template(self):
        # Arrange
        url = reverse('user_profile:profile')
        # Act
        response = self.client.get(url)
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_profile/profile.html')

    def test_change_password_returns_correct_template(self):
        # Arrange
        url = reverse('user_profile:change_password')
        # Act
        response = self.client.get(url)
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_profile/change_password.html')
