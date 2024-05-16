from django.test import SimpleTestCase
from django.test.client import resolve
from django.urls import reverse

from payment.views import billing, complete_payment, payment_success


class TestUrls(SimpleTestCase):
    def test_payment_url_is_resolved(self):
        # Arrange
        url = reverse('payment:payment', args=['100'])
        # Act
        resolved = resolve(url)
        # Assert
        self.assertEqual(resolved.func, billing)

    def test_complete_payment_url_is_resolved(self):
        # Arrange
        url = reverse('payment:complete_payment')
        # Act
        resolved = resolve(url)
        # Assert
        self.assertEqual(resolved.func, complete_payment)

    def test_payment_success_url_is_resolved(self):
        # Arrange
        url = reverse('payment:payment_success')
        # Act
        resolved = resolve(url)
        # Assert
        self.assertEqual(resolved.func, payment_success)
