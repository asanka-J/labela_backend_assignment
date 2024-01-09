from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from .models import Cart

class CartAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', password='password')

    def test_guest_cart_creation(self):
        response = self.client.get('/api/cart/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_guest_cart_cart_id_format(self):
        response = self.client.get('/api/cart/')
        expected_prefix = 'G'
        cart_id = response.data.get('cart_id', '')
        self.assertTrue(expected_prefix,cart_id[0])

    def test_logged_in_user_cart_creation(self):
        self.client.force_login(self.user)
        response = self.client.get('/api/cart/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_logged_in_user_cart_creation(self):
        self.client.force_login(self.user)
        response = self.client.get('/api/cart/')
        expected_prefix = 'U'
        cart_id = response.data.get('cart_id', '')
        self.assertTrue(expected_prefix,cart_id[0])
        
    def test_logged_in_user_existing_cart(self):
        self.client.force_login(self.user)
        response = self.client.get('/api/cart/')
        cart_owner = response.data.get('user', '')
        self.assertEqual(self.user.id, cart_owner)

    def test_user_access_own_cart(self):
        self.client.force_login(self.user)
        cart = Cart.objects.create(user=self.user)
        response = self.client.get(f'/api/cart/?cart_id={cart.cart_id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_access_other_user_cart(self):
        other_user = User.objects.create(username='otheruser', password='password')
        self.client.force_login(other_user)
        cart = Cart.objects.create(user=self.user)
        response = self.client.get(f'/api/cart/?cart_id={cart.cart_id}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_guest_access_user_cart(self):
        cart = Cart.objects.create(user=self.user)
        response = self.client.get(f'/api/cart/?cart_id={cart.cart_id}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Guest trying to access another guest's cart should pass if it's not associated with a user
    def test_guest_access_other_guest_cart(self):
        cart = Cart.objects.create()
        response = self.client.get(f'/api/cart/?cart_id={cart.cart_id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # Assert success as it's not associated with a user

    # test requesting a cart with an invalid cart_id
    def test_invalid_cart_id(self):
        response = self.client.get('/api/cart/?cart_id=invalid_cart_id')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


