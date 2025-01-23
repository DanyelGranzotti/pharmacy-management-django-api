from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from ..models.user import User
from ..serializers.user import UserSerializer, RegisterSerializer, LoginSerializer, TokenSerializer
from django.db.utils import IntegrityError
from ..services.user_service import create_user, get_user, update_user, delete_user
from django.core.exceptions import ObjectDoesNotExist
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from ..permissions import IsOwner
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

class UserPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'email']
    pagination_class = UserPagination

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsOwner]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    @swagger_auto_schema(
        operation_description="Create a new user",
        request_body=UserSerializer,
        responses={
            201: openapi.Response('User created successfully', UserSerializer),
            400: 'Bad Request',
            500: 'Unexpected error'
        }
    )
    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            user = create_user(data)
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'detail': 'Unexpected error.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Retrieve a user by ID",
        responses={
            200: openapi.Response('User retrieved successfully', UserSerializer),
            404: 'User not found',
            500: 'Unexpected error'
        }
    )
    def retrieve(self, request, *args, **kwargs):
        try:
            user = self.get_object()
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        except ObjectDoesNotExist as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response({'detail': 'Unexpected error.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Update a user by ID",
        request_body=UserSerializer,
        responses={
            200: openapi.Response('User updated successfully', UserSerializer),
            400: 'Bad Request',
            404: 'User not found',
            500: 'Unexpected error'
        }
    )
    def update(self, request, *args, **kwargs):
        try:
            user = self.get_object()
            serializer = self.get_serializer(user, data=request.data, partial=False)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({'detail': 'Unexpected error.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Partially update a user by ID",
        request_body=UserSerializer,
        responses={
            200: openapi.Response('User partially updated successfully', UserSerializer),
            400: 'Bad Request',
            404: 'User not found',
            500: 'Unexpected error'
        }
    )
    def partial_update(self, request, *args, **kwargs):
        try:
            user = self.get_object()
            serializer = self.get_serializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({'detail': 'Unexpected error.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Delete a user by ID",
        responses={
            204: 'User deleted successfully',
            404: 'User not found',
            500: 'Unexpected error'
        }
    )
    def destroy(self, request, *args, **kwargs):
        try:
            user = self.get_object()
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response({'detail': 'Unexpected error.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        operation_description="Retrieve a list of users",
        responses={200: UserSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class RegisterView(APIView):
    @swagger_auto_schema(
        operation_description="Register a new user",
        request_body=RegisterSerializer,
        responses={
            201: openapi.Response('User registered successfully', RegisterSerializer),
            400: 'Bad Request'
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    @swagger_auto_schema(
        operation_description="Login a user",
        request_body=LoginSerializer,
        responses={
            200: 'Login successful',
            401: 'Invalid credentials',
            400: 'Bad Request'
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            token_serializer = TokenSerializer({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
            return Response(token_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
