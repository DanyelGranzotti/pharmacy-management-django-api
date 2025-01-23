from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models.bank_account import BankAccount
from ..serializers.bank_account import BankAccountSerializer
from ..permissions import IsOwner
from ..services.bank_account_service import get_user_bank_accounts, create_bank_account
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

class BankAccountPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class BankAccountViewSet(viewsets.ModelViewSet):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['account_number', 'bank_name']
    pagination_class = BankAccountPagination

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return BankAccount.objects.none()
        if self.request.user.is_authenticated:
            return get_user_bank_accounts(self.request.user)
        return BankAccount.objects.none()

    def perform_create(self, serializer):
        create_bank_account(serializer, self.request.user)
