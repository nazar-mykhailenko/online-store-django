from django.test import SimpleTestCase
from django.test.client import resolve
from django.urls import reverse

from core.views import index, details

class TestUrls(SimpleTestCase):
    def test_index_url_is_resolved(self):
        # Arrange
        url = reverse('core:index')
        # Act
        resolved = resolve(url)
        # Assert
        self.assertEqual(resolved.func, index)

    def test_details_url_is_resolved(self):
        # Arrange
        url = reverse('core:details', args=[1])
        # Act
        resolved = resolve(url)
        # Assert
        self.assertEqual(resolved.func, details)
