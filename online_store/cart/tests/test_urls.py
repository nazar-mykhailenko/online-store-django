from django.test import SimpleTestCase
from django.test.client import resolve
from django.urls import reverse

from cart.views import cart, cart_add, cart_remove, cart_remove_completely

class TestUrls(SimpleTestCase):
    def test_cart_url_is_resolved(self):
        # Arrange
        url = reverse('cart:cart')
        # Act
        resolved = resolve(url)
        # Assert
        self.assertEqual(resolved.func, cart)

    def test_cart_add_url_is_resolved(self):
        # Arrange
        url = reverse('cart:cart-add', args=[1])
        # Act
        resolved = resolve(url)
        # Assert
        self.assertEqual(resolved.func, cart_add)

    def test_cart_remove_url_is_resolved(self):
        # Arrange
        url = reverse('cart:cart-remove', args=[1])
        # Act
        resolved = resolve(url)
        # Assert
        self.assertEqual(resolved.func, cart_remove)

    def test_cart_remove_all_url_is_resolved(self):
        # Arrange
        url = reverse('cart:cart-remove-all', args=[1])
        # Act
        resolved = resolve(url)
        # Assert
        self.assertEqual(resolved.func, cart_remove_completely)
