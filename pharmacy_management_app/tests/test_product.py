from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from io import StringIO
import csv
from ..models.product import Product

User = get_user_model()

class ProductCSVUploadTest(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(email='admin@example.com', password='adminpassword', name='Admin User')
        self.token = RefreshToken.for_user(self.admin_user).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_upload_products_csv(self):
        url = reverse('upload-products')
        csv_file = StringIO()
        writer = csv.writer(csv_file)
        writer.writerow(['name', 'description', 'cost_price', 'profit_margin', 'quantity'])
        writer.writerow(['Aspirin', 'Pain reliever', '5.99', '0.20', '100'])
        writer.writerow(['Ibuprofen', 'Anti-inflammatory', '7.49', '0.25', '200'])
        csv_file.seek(0)
        response = self.client.post(url, {'file': csv_file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['detail'], 'Products uploaded successfully.')

    def test_upload_products_csv_no_file(self):
        url = reverse('upload-products')
        response = self.client.post(url, {}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'No file provided.')

    def test_upload_products_csv_invalid_data(self):
        url = reverse('upload-products')
        csv_file = StringIO()
        writer = csv.writer(csv_file)
        writer.writerow(['name', 'description', 'cost_price', 'profit_margin', 'quantity'])
        writer.writerow(['Aspirin', 'Pain reliever', 'invalid_price', '0.20', '100'])
        csv_file.seek(0)
        response = self.client.post(url, {'file': csv_file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class ProductCRUDTest(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(email='admin@example.com', password='adminpassword', name='Admin User')
        self.token = RefreshToken.for_user(self.admin_user).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.product_data = {
            'name': 'Test Product',
            'description': 'Test Description',
            'cost_price': 10.00,
            'profit_margin': 0.2,
            'quantity': 100
        }

    def test_create_product(self):
        url = reverse('product-list')
        response = self.client.post(url, self.product_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], self.product_data['name'])

    def test_get_product(self):
        product = Product.objects.create(**self.product_data)
        url = reverse('product-detail', args=[product.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.product_data['name'])

    def test_update_product(self):
        product = Product.objects.create(**self.product_data)
        url = reverse('product-detail', args=[product.id])
        updated_data = self.product_data.copy()
        updated_data['name'] = 'Updated Product'
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], updated_data['name'])

    def test_delete_product(self):
        product = Product.objects.create(**self.product_data)
        url = reverse('product-detail', args=[product.id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(id=product.id).exists())
