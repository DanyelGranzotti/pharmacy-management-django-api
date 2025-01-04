from django.apps import AppConfig

class PharmacyManagementDjangoApiConfig(AppConfig):
    name = 'pharmacy_management_django_api'

    def ready(self):
        from pharmacy_management_app.models.user import User
        User.objects.create_admin_from_env()
