from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models.bank_account import BankAccount
from ..serializers.bank_account import BankAccountSerializer
from ..permissions import IsOwner

class BankAccountViewSet(viewsets.ModelViewSet):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return BankAccount.objects.none()
        if self.request.user.is_authenticated:
            return self.queryset.filter(user=self.request.user)
        return BankAccount.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
