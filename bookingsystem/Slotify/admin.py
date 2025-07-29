from django.contrib import admin
from .models import Service, Provider, Availability, Booking

admin.site.register(Service)
admin.site.register(Provider)
admin.site.register(Availability)
admin.site.register(Booking)
