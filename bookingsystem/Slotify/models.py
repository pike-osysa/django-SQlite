from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta

# Service offered (e.g. haircut, training session)
class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.DurationField(default=timedelta(minutes=30))

    def __str__(self):
        return self.name

# A provider is someone offering bookings (e.g. stylist, doctor)
class Provider(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    services = models.ManyToManyField(Service)

    def __str__(self):
        return f"{self.user.username}"

# When a provider is available (for bookings)
class Availability(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.provider} - {self.date} {self.start_time}-{self.end_time}"

# A bookable slot for a provider and service
class Slot(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.provider} - {self.service} @ {self.date} {self.time} ({'Available' if self.available else 'Booked'})"

# A client booking a service with a provider
class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)  # 🔗 New: Link booking to a specific slot
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.client.username} → {self.service.name} with {self.provider.user.username} @ {self.date} {self.time}"
