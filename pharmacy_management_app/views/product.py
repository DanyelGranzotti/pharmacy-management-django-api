import csv
import logging
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..models.product import Product
from ..serializers.product import ProductSerializer
from ..permissions import IsAdminUser

logger = logging.getLogger(__name__)

class ProductCSVUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated, IsAdminUser]

    @swagger_auto_schema(
        operation_description="Upload a CSV file with a list of products",
        manual_parameters=[
            openapi.Parameter(
                'file', openapi.IN_FORM, description="CSV file", type=openapi.TYPE_FILE, required=True
            )
        ],
        responses={
            201: openapi.Response('Products uploaded successfully'),
            400: 'Bad Request',
            500: 'Internal Server Error'
        }
    )
    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if not file:
            return Response({'detail': 'No file provided.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            decoded_file = file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            products = []
            for row in reader:
                logger.debug(f"Processing row: {row}")
                try:
                    if 'cost_price' in row:
                        row['cost_price'] = float(row['cost_price'])
                    if 'profit_margin' in row:
                        row['profit_margin'] = float(row['profit_margin'])
                except ValueError as e:
                    logger.error(f"Invalid data: {e}")
                    return Response({'detail': f"Invalid data: {e}"}, status=status.HTTP_400_BAD_REQUEST)
                
                serializer = ProductSerializer(data=row)
                if serializer.is_valid():
                    products.append(serializer.save())
                else:
                    logger.error(f"Invalid data: {serializer.errors}")
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({'detail': 'Products uploaded successfully.'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Error processing file: {e}")
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [IsAuthenticatedOrReadOnly]
        else:
            self.permission_classes = [IsAuthenticated, IsAdminUser]
        return super().get_permissions()

    @swagger_auto_schema(
        operation_description="Retrieve a list of products",
        responses={200: ProductSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new product",
        request_body=ProductSerializer,
        responses={201: ProductSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Retrieve a product by ID",
        responses={200: ProductSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a product by ID",
        request_body=ProductSerializer,
        responses={200: ProductSerializer}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update a product by ID",
        request_body=ProductSerializer,
        responses={200: ProductSerializer}
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a product by ID",
        responses={204: 'No Content'}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
