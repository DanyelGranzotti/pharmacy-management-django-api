from rest_framework import viewsets
from ..models.user import User
from ..serializers.user import UserSerializer
from django.db.utils import IntegrityError
from rest_framework.response import Response
from rest_framework import status
from ..services.user_service import create_user, get_user, update_user, delete_user
from django.core.exceptions import ObjectDoesNotExist

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

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

    def retrieve(self, request, *args, **kwargs):
        try:
            user = get_user(kwargs['pk'])
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        except ObjectDoesNotExist as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response({'detail': 'Unexpected error.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        try:
            user = update_user(kwargs['pk'], request.data)
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        except ObjectDoesNotExist as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response({'detail': 'Unexpected error.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        try:
            delete_user(kwargs['pk'])
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist as e:
            return Response({'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response({'detail': 'Unexpected error.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
