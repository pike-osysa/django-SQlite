from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from Slotify.models import Service, Provider, Slot
from datetime import date, time, timedelta
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **options):
        # Create services
        services_data = [
            {'name': 'Haircut', 'description': 'Professional haircut and styling', 'duration': timedelta(minutes=30)},
            {'name': 'Medical Consultation', 'description': 'General medical check-up', 'duration': timedelta(minutes=45)},
            {'name': 'Massage Therapy', 'description': 'Relaxing full body massage', 'duration': timedelta(hours=1)},
            {'name': 'Tutoring Session', 'description': 'One-on-one academic tutoring', 'duration': timedelta(hours=1)},
        ]

        for service_data in services_data:
            service, created = Service.objects.get_or_create(
                name=service_data['name'],
                defaults=service_data
            )
            if created:
                self.stdout.write(f'Created service: {service.name}')

        # Create provider users
        provider_users_data = [
            {'username': 'john_barber', 'first_name': 'John', 'last_name': 'Smith', 'email': 'john@example.com'},
            {'username': 'dr_sarah', 'first_name': 'Sarah', 'last_name': 'Johnson', 'email': 'sarah@example.com'},
            {'username': 'mike_massage', 'first_name': 'Mike', 'last_name': 'Wilson', 'email': 'mike@example.com'},
            {'username': 'teacher_anna', 'first_name': 'Anna', 'last_name': 'Brown', 'email': 'anna@example.com'},
        ]

        providers = []
        for user_data in provider_users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'email': user_data['email'],
                }
            )
            if created:
                user.set_password('provider123')
                user.save()
                self.stdout.write(f'Created user: {user.username}')

            provider, created = Provider.objects.get_or_create(user=user)
            if created:
                self.stdout.write(f'Created provider: {provider}')
            providers.append(provider)

        # Assign services to providers
        services = Service.objects.all()
        providers[0].services.add(services[0])  # John - Haircut
        providers[1].services.add(services[1])  # Sarah - Medical
        providers[2].services.add(services[2])  # Mike - Massage
        providers[3].services.add(services[3])  # Anna - Tutoring

        # Create slots for the next 7 days
        today = timezone.now().date()
        for i in range(7):
            slot_date = today + timedelta(days=i)
            
            # Skip weekends for some services
            if slot_date.weekday() < 5:  # Monday to Friday
                # Create morning slots (9 AM to 12 PM)
                for hour in [9, 10, 11]:
                    for provider in providers:
                        for service in provider.services.all():
                            slot, created = Slot.objects.get_or_create(
                                provider=provider,
                                service=service,
                                date=slot_date,
                                time=time(hour, 0),
                                defaults={'available': True}
                            )
                            if created:
                                self.stdout.write(f'Created slot: {slot}')

                # Create afternoon slots (2 PM to 5 PM)
                for hour in [14, 15, 16, 17]:
                    for provider in providers:
                        for service in provider.services.all():
                            slot, created = Slot.objects.get_or_create(
                                provider=provider,
                                service=service,
                                date=slot_date,
                                time=time(hour, 0),
                                defaults={'available': True}
                            )
                            if created:
                                self.stdout.write(f'Created slot: {slot}')

        # Create a test user for booking
        test_user, created = User.objects.get_or_create(
            username='testuser',
            defaults={
                'first_name': 'Test',
                'last_name': 'User',
                'email': 'test@example.com',
            }
        )
        if created:
            test_user.set_password('testpass123')
            test_user.save()
            self.stdout.write('Created test user: testuser (password: testpass123)')

        self.stdout.write(self.style.SUCCESS('Successfully populated database with sample data!'))
