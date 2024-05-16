from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse
from cart.models import CartItem

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
        self.user = User.objects.create_user('test', 'test@test.com', 'somepassword')
        self.cart_item = CartItem.objects.create(
            user=self.user,
            product=self.first_item,
            quantity=2,
        )
        self.client = Client()
        self.client.login(username='test', password='somepassword')

    def test_cart_returns_correct_template(self):
        # Arrange
        url = reverse('cart:cart')
        # Act
        response = self.client.get(url)
        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/cart.html')

    def test_cart_returns_correct_data(self):
        # Arrange
        url = reverse('cart:cart')
        expected_total = self.cart_item.product.price * self.cart_item.quantity
        # Act
        response = self.client.get(url)
        # Assert
        self.assertEqual(response.context['cart_empty'], False)
        self.assertEqual(response.context['total'], expected_total)
        self.assertListEqual(list(response.context['cart_items']), [self.cart_item])

    def test_cart_add_redirects_to_cart_when_item_exists(self):
        # Arrange
        url = reverse('cart:cart-add', args=[self.first_item.id])
        expected_url_to_redirect_to = reverse('cart:cart')
        # Act
        response = self.client.get(url)
        # Assert
        self.assertRedirects(response, expected_url_to_redirect_to)

    def test_cart_add_adds_item_to_cart_when_it_is_not_in_cart(self):
        # Arrange
        url = reverse('cart:cart-add', args=[self.second_item.id])
        # Act
        self.client.get(url)
        # Assert
        self.assertEqual(CartItem.objects.count(), 2)

    def test_cart_add_increases_quantity_when_item_is_already_in_cart(self):
        # Arrange
        url = reverse('cart:cart-add', args=[self.first_item.id])
        # Act
        self.client.get(url)
        # Assert
        self.assertEqual(CartItem.objects.count(), 1)
        self.assertEqual(CartItem.objects.first().quantity, 3)

    def test_cart_add_redirects_to_cart_when_item_does_not_exist(self):
        # Arrange
        url = reverse('cart:cart-add', args=[1000])
        expected_url_to_redirect_to = reverse('cart:cart')
        # Act
        response = self.client.get(url)
        # Assert
        self.assertRedirects(response, expected_url_to_redirect_to)

    def test_cart_add_does_not_add_item_when_item_does_not_exist(self):
        # Arrange
        url = reverse('cart:cart-add', args=[1000])
        # Act
        response = self.client.get(url)
        # Assert
        self.assertEqual(CartItem.objects.count(), 1)

    def test_cart_remove_redirects_to_cart_when_item_is_in_cart(self):
        # Arrange
        url = reverse('cart:cart-remove', args=[self.first_item.id])
        expected_url_to_redirect_to = reverse('cart:cart')
        # Act
        response = self.client.get(url)
        # Assert
        self.assertRedirects(response, expected_url_to_redirect_to)

    def test_cart_remove_decreases_quantity_when_item_quantity_is_greater_than_one(self):
        # Arrange
        url = reverse('cart:cart-remove', args=[self.first_item.id])
        # Act
        self.client.get(url)
        # Assert
        self.assertEqual(CartItem.objects.count(), 1)
        self.assertEqual(CartItem.objects.first().quantity, 1)

    def test_cart_remove_removes_item_when_quantity_is_one(self):
        # Arrange
        self.cart_item.quantity = 1
        self.cart_item.save()
        url = reverse('cart:cart-remove', args=[self.first_item.id])
        # Act
        self.client.get(url)
        # Assert
        self.assertEqual(CartItem.objects.count(), 0)

    def test_cart_remove_redirects_to_cart_when_item_is_not_in_cart(self):
        # Arrange
        url = reverse('cart:cart-remove', args=[self.second_item.id])
        expected_url_to_redirect_to = reverse('cart:cart')
        # Act
        response = self.client.get(url)
        # Assert
        self.assertRedirects(response, expected_url_to_redirect_to)

    def test_cart_remove_does_not_remove_item_when_item_is_not_in_cart(self):
        # Arrange
        url = reverse('cart:cart-remove', args=[self.second_item.id])
        # Act
        response = self.client.get(url)
        # Assert
        self.assertEqual(CartItem.objects.count(), 1)

    def test_cart_remove_completely_redirects_to_cart_when_item_is_in_cart(self):
        # Arrange
        url = reverse('cart:cart-remove-all', args=[self.first_item.id])
        expected_url_to_redirect_to = reverse('cart:cart')
        # Act
        response = self.client.get(url)
        # Assert
        self.assertRedirects(response, expected_url_to_redirect_to)

    def test_cart_remove_completely_removes_item_from_cart(self):
        # Arrange
        url = reverse('cart:cart-remove-all', args=[self.first_item.id])
        # Act
        self.client.get(url)
        # Assert
        self.assertEqual(CartItem.objects.count(), 0)

    def test_cart_remove_completely_redirects_to_cart_when_item_is_not_in_cart(self):
        # Arrange
        url = reverse('cart:cart-remove-all', args=[self.second_item.id])
        expected_url_to_redirect_to = reverse('cart:cart')
        # Act
        response = self.client.get(url)
        # Assert
        self.assertRedirects(response, expected_url_to_redirect_to)

    def test_cart_remove_completely_does_not_remove_item_when_item_is_not_in_cart(self):
        # Arrange
        url = reverse('cart:cart-remove-all', args=[self.second_item.id])
        # Act
        response = self.client.get(url)
        # Assert
        self.assertEqual(CartItem.objects.count(), 1)
