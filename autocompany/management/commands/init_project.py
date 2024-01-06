from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Generates an admin account and run initial configs'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Running Migrations'))
        call_command('makemigrations')
        call_command('migrate')
        call_command('collectstatic', '--noinput')
        self.stdout.write(self.style.SUCCESS('Static files collected'))
        
        
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@demo.com', 'demo@123')
            self.stdout.write(self.style.SUCCESS('Admin account created successfully'))
        else:
            self.stdout.write(self.style.ERROR('Admin account already exists'))
            
