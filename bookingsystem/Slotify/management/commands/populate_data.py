from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from Slotify.models import Service, Provider, Slot
from datetime import datetime, timedelta, time
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate database with sample booking data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create services
        services_data = [
            {'name': 'Haircut', 'description': 'Professional haircut and styling', 'duration': timedelta(minutes=45)},
            {'name': 'Massage', 'description': 'Relaxing therapeutic massage', 'duration': timedelta(minutes=60)},
            {'name': 'Dental Cleaning', 'description': 'Professional dental cleaning', 'duration': timedelta(minutes=30)},
            {'name': 'Personal Training', 'description': 'One-on-one fitness training session', 'duration': timedelta(minutes=60)},
        ]
        
        for service_data in services_data:
            service, created = Service.objects.get_or_create(**service_data)
            if created:
                self.stdout.write(f'Created service: {service.name}')

        # Create provider users
        provider_users = []
        for i, name in enumerate(['alice', 'bob', 'carol'], 1):
            user, created = User.objects.get_or_create(
                username=name,
                defaults={
                    'first_name': name.capitalize(),
                    'email': f'{name}@example.com',
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                self.stdout.write(f'Created user: {user.username}')
            provider_users.append(user)

        # Create providers
        providers = []
        for user in provider_users:
            provider, created = Provider.objects.get_or_create(user=user)
            if created:
                # Assign services to providers
                all_services = Service.objects.all()
                provider.services.set(all_services[:2])  # Each provider gets first 2 services
                self.stdout.write(f'Created provider: {provider}')
            providers.append(provider)

        # Create slots for the next 7 days
        start_date = timezone.now().date()
        time_slots = [
            time(9, 0), time(10, 0), time(11, 0), 
            time(14, 0), time(15, 0), time(16, 0)
        ]
        
        for day_offset in range(7):
            date = start_date + timedelta(days=day_offset)
            for provider in providers:
                for service in provider.services.all():
                    for slot_time in time_slots:
                        slot, created = Slot.objects.get_or_create(
                            provider=provider,
                            service=service,
                            date=date,
                            time=slot_time,
                            defaults={'available': True}
                        )
                        if created:
                            self.stdout.write(f'Created slot: {slot}')

        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))
