from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from core.models import Category, Item


class TestViews(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Cabinets')
        self.first_item = Item.objects.create(
            name='Cabinet with money',
            price=420,
            category=self.category,
            image=SimpleUploadedFile(name='cab-1.png', content='')
        )
        self.second_item = Item.objects.create(
            name='Cabinet without money',
            price=100,
            category=self.category,
            image=SimpleUploadedFile(name='cab-2.png', content='')
        )

    def test_index_returns_correct_template(self):
        # Arrange
        url = reverse('core:index')
        # Act
        response = self.client.get(url)
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/index.html')

    def test_index_returns_correct_data(self):
        # Arrange
        url = reverse('core:index')
        # Act
        response = self.client.get(url)
        # Assert
        self.assertSetEqual(response.context['items'], Item.objects.all())

    def test_details_returns_correct_template(self):
        # Arrange
        url = reverse('core:details', args=[self.first_item.id])
        # Act
        response = self.client.get(url)
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/details.html')

    def test_details_returns_correct_data(self):
        # Arrange
        url = reverse('core:details', args=[self.first_item.id])
        # Act
        response = self.client.get(url)
        # Assert
        self.assertEqual(response.context['item'], self.first_item)

    def test_details_redirects_to_index_when_item_does_not_exist(self):
        # Arrange
        url = reverse('core:details', args=[1000])
        expected_url = reverse('core:index')
        # Act
        response = self.client.get(url)
        # Assert
        self.assertRedirects(response, expected_url)
