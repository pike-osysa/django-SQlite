from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Slot, Booking, Service, Provider
from .forms import BookingForm

def home(request):
    services = Service.objects.all()
    available_slots = Slot.objects.filter(available=True, date__gte=timezone.now().date())[:10]
    return render(request, 'Slotify/home.html', {
        'services': services,
        'available_slots': available_slots
    })

def services_list(request):
    services = Service.objects.all()
    return render(request, 'Slotify/services.html', {'services': services})

def service_slots(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    slots = Slot.objects.filter(
        service=service, 
        available=True, 
        date__gte=timezone.now().date()
    ).order_by('date', 'time')
    return render(request, 'Slotify/service_slots.html', {
        'service': service,
        'slots': slots
    })

@login_required
def book_slot(request, slot_id):
    slot = get_object_or_404(Slot, id=slot_id, available=True)
    
    if request.method == 'POST':
        booking = Booking.objects.create(
            client=request.user,
            provider=slot.provider,
            service=slot.service,
            date=slot.date,
            time=slot.time,
            slot=slot,
            status='confirmed'
        )
        slot.available = False
        slot.save()
        messages.success(request, 'Booking confirmed successfully!')
        return redirect('my_bookings')
    
    return render(request, 'Slotify/book_slot.html', {'slot': slot})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(client=request.user).order_by('-date', '-time')
    return render(request, 'Slotify/my_bookings.html', {'bookings': bookings})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, client=request.user)
    if booking.status != 'cancelled':
        booking.status = 'cancelled'
        booking.save()
        booking.slot.available = True
        booking.slot.save()
        messages.success(request, 'Booking cancelled successfully!')
    return redirect('my_bookings')