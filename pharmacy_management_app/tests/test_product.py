from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from io import StringIO
from ..models.product import Product
from ..models.suppliers import Suppliers

User = get_user_model()


class ProductCRUDTest(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(email='admin@example.com', password='adminpassword', name='Admin User')
        self.token = RefreshToken.for_user(self.admin_user).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.supplier = Suppliers.objects.create(name='Test Supplier', contact_info='test@example.com')
        self.product_data = {
            'name': 'Test Product',
            'description': 'Test Description',
            'cost_price': 10.00,
            'profit_margin': 0.2,
            'quantity': 100,
            'supplier': self.supplier.id
        }

    def test_get_product(self):
        product = Product.objects.create(
            name=self.product_data['name'],
            description=self.product_data['description'],
            cost_price=self.product_data['cost_price'],
            profit_margin=self.product_data['profit_margin'],
            quantity=self.product_data['quantity'],
            supplier=self.supplier
        )
        url = reverse('product-detail', args=[product.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product_data['name'])

    def test_update_product(self):
        product = Product.objects.create(
            name=self.product_data['name'],
            description=self.product_data['description'],
            cost_price=self.product_data['cost_price'],
            profit_margin=self.product_data['profit_margin'],
            quantity=self.product_data['quantity'],
            supplier=self.supplier
        )
        url = reverse('product-detail', args=[product.id])
        updated_data = self.product_data.copy()
        updated_data['name'] = 'Updated Product'
        updated_data['supplier'] = self.supplier.id
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], updated_data['name'])

    def test_delete_product(self):
        product = Product.objects.create(
            name=self.product_data['name'],
            description=self.product_data['description'],
            cost_price=self.product_data['cost_price'],
            profit_margin=self.product_data['profit_margin'],
            quantity=self.product_data['quantity'],
            supplier=self.supplier
        )
        url = reverse('product-detail', args=[product.id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(id=product.id).exists())
