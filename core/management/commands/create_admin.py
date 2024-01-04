from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Generates an admin account'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@demo.com', 'demo@123')
            self.stdout.write(self.style.SUCCESS('Admin account created successfully'))
        else:
            self.stdout.write(self.style.ERROR('Admin account already exists'))
