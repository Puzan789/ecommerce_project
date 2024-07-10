from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from product.models import Product, Order, OrderItem


class AuthTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.product = Product.objects.create(name='Test Product', price=100)

    

    def test_signup_view(self):
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        })
        (User.objects.filter(username='newuser').exists())

    def test_login_and_access_cart(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('cart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart.html')

    def test_add_to_cart(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('add_to_cart', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)
        order = Order.objects.get(user=self.user, completed=False)
        self.assertTrue(OrderItem.objects.filter(order=order, product=self.product).exists())

    def test_remove_from_cart(self):
        self.client.login(username='testuser', password='testpassword')
        order = Order.objects.create(user=self.user, completed=False)
        order_item = OrderItem.objects.create(order=order, product=self.product, quantity=1, price=self.product.price)
        response = self.client.get(reverse('remove_from_cart', args=[order_item.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(OrderItem.objects.filter(id=order_item.id).exists())

    def test_update_quantity(self):
        self.client.login(username='testuser', password='testpassword')
        order = Order.objects.create(user=self.user, completed=False)
        order_item = OrderItem.objects.create(order=order, product=self.product, quantity=1, price=self.product.price)
        response = self.client.post(reverse('update_quantity', args=[order_item.id]), {'action': 'increase'})
        order_item.refresh_from_db()
        self.assertEqual(order_item.quantity, 2)

    def test_checkout(self):
        self.client.login(username='testuser', password='testpassword')
        order = Order.objects.create(user=self.user, completed=False)
        OrderItem.objects.create(order=order, product=self.product, quantity=1, price=self.product.price)
        response = self.client.post(reverse('checkout'))
        self.assertEqual(response.status_code, 302)
        order.refresh_from_db()
        self.assertTrue(order.completed)
        self.assertFalse(OrderItem.objects.filter(order=order).exists())

    def test_success_view(self):
        response = self.client.get(reverse('success'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'success.html')
