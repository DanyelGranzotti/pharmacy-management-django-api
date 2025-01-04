from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views.user import UserViewSet, RegisterView, LoginView
from ..views.bank_account import BankAccountViewSet
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'bank-accounts', BankAccountViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
