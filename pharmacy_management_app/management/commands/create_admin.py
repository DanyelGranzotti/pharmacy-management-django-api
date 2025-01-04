from django.core.management.base import BaseCommand
from django.conf import settings
from pharmacy_management_app.models.user import User

class Command(BaseCommand):
    help = 'Create an admin user from environment variables'

    def handle(self, *args, **kwargs):
        email = settings.ADMIN_EMAIL
        password = settings.ADMIN_PASSWORD
        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(email=email, password=password)
            self.stdout.write(self.style.SUCCESS('Admin user created successfully'))
        else:
            self.stdout.write(self.style.WARNING('Admin user already exists'))
