from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from io import StringIO
import csv

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
        writer.writerow(['name', 'description', 'price', 'quantity'])
        writer.writerow(['Aspirin', 'Pain reliever', '5.99', '100'])
        writer.writerow(['Ibuprofen', 'Anti-inflammatory', '7.49', '200'])
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
        writer.writerow(['name', 'description', 'price', 'quantity'])
        writer.writerow(['Aspirin', 'Pain reliever', 'invalid_price', '100'])
        csv_file.seek(0)
        response = self.client.post(url, {'file': csv_file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
