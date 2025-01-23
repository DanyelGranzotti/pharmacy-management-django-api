from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views.user import UserViewSet, RegisterView, LoginView
from ..views.bank_account import BankAccountViewSet
from ..views.product import ProductViewSet
from rest_framework_simplejwt.views import TokenRefreshView
from ..views.transaction import PurchaseProductView
from ..views.supplier import SupplierViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'bank-accounts', BankAccountViewSet)
router.register(r'products', ProductViewSet)
router.register(r'suppliers', SupplierViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('purchase-product/', PurchaseProductView.as_view(), name='purchase-product'),
]
