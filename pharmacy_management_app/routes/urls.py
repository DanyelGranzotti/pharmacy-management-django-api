from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views.user import UserViewSet, RegisterView, LoginView
from ..views.bank_account import BankAccountViewSet
from ..views.product import ProductCSVUploadView
from rest_framework_simplejwt.views import TokenRefreshView
from ..views.transaction import PurchaseProductView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'bank-accounts', BankAccountViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('upload-products/', ProductCSVUploadView.as_view(), name='upload-products'),
    path('purchase-product/', PurchaseProductView.as_view(), name='purchase-product'),
]
