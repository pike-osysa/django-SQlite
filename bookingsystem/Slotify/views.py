from django.shortcuts import render, redirect
from .models import Slot, Booking
from .forms import BookingForm
from django.contrib.auth.decorators import login_required

def home(request):
    slots = Slot.objects.filter(available=True)
    return render(request, 'Slotify/home.html', {'slots': slots})

def book_slot(request):
    # your booking logic
    return render(request, 'slotify/book_slot.html')

def business(request):
    return render(request, 'slotify/business.html')

def contact(request):
    if request.method == 'POST':
        # handle form submission (save or send email)
        pass
    return render(request, 'slotify/contact.html')

@login_required
def book_slot(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.save()
            # Mark slot as unavailable
            booking.slot.available = False
            booking.slot.save()
            return redirect('home')
    else:
        form = BookingForm()
    return render(request, 'Slotify/book_slot.html', {'form': form})
        