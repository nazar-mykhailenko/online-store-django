from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse


class TestViews(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test', 'test@test.com', 'somepassword')
        self.client = Client()
        self.client.login(username='test', password='somepassword')

    def test_payment_returns_correct_template(self):
        # Arrange
        url = reverse('payment:payment', args=['100'])
        # Act
        response = self.client.get(url)
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'payment/payment.html')

    def test_payment_success_returns_correct_template(self):
        # Arrange
        url = reverse('payment:payment_success')
        # Act
        response = self.client.get(url)
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'payment/payment_success.html')
