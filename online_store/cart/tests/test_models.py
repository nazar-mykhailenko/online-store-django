from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from cart.models import CartItem

from core.models import Category, Item


class TestModels(TestCase):
    def setUp(self) -> None:
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
        self.user = User.objects.create_user('test', 'test@test.com', 'somepassword')
        self.cart_item = CartItem.objects.create(
            user=self.user,
            product=self.first_item,
            quantity=2,
        )

    def test_cart_item_get_total_returns_correct_total(self):
        # Arrange
        expected_total = self.cart_item.product.price * self.cart_item.quantity
        # Act
        total = self.cart_item.get_total()
        # Assert
        self.assertEqual(total, expected_total)

