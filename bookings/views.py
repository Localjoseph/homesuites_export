from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.db.models import Q
from datetime import date
from .models import Booking
from .forms import BookingForm
from properties.models import Property

class BookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'bookings/booking_list.html'
    context_object_name = 'bookings'
    paginate_by = 10
    
    def get_queryset(self):
        return Booking.objects.filter(guest=self.request.user).order_by('-booking_date')


class HostBookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'bookings/host_booking_list.html'
    context_object_name = 'bookings'
    paginate_by = 10
    
    def get_queryset(self):
        # Get bookings for properties owned by the current user
        return Booking.objects.filter(rental_property__owner=self.request.user).order_by('-booking_date')


class BookingDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Booking
    template_name = 'bookings/booking_detail.html'
    
    def test_func(self):
        booking = self.get_object()
        # Allow access if user is the guest or the property owner
        return self.request.user == booking.guest or self.request.user == booking.rental_property.owner


@login_required
def create_booking(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    
    # Check if the property is available
    if not property.is_available:
        messages.error(request, 'This property is currently not available for booking.')
        return redirect('property-detail', pk=property_id)
    
    # Check if the user is trying to book their own property
    if request.user == property.owner:
        messages.error(request, 'You cannot book your own property.')
        return redirect('property-detail', pk=property_id)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            check_in = form.cleaned_data['check_in']
            check_out = form.cleaned_data['check_out']
            guests = form.cleaned_data['guests']
            
            # Check if there are any conflicting bookings
            conflicting_bookings = Booking.objects.filter(
                rental_property=property,
                status__in=['pending', 'confirmed'],
            ).filter(
                Q(check_in__range=[check_in, check_out]) |
                Q(check_out__range=[check_in, check_out]) |
                (Q(check_in__lte=check_in) & Q(check_out__gte=check_out))
            )
            
            if conflicting_bookings.exists():
                messages.error(request, 'The property is not available for the selected dates.')
                return render(request, 'bookings/booking_create.html', {
                    'form': form,
                    'property': property
                })
            
            # Check if the number of guests exceeds the property capacity
            if guests > property.accommodates:
                messages.error(request, f'This property can only accommodate {property.accommodates} guests.')
                return render(request, 'bookings/booking_create.html', {
                    'form': form,
                    'property': property
                })
            
            # Create the booking
            booking = form.save(commit=False)
            booking.guest = request.user
            booking.rental_property = property
            booking.save()
            
            messages.success(request, 'Your booking request has been submitted! The host will review your request.')
            return redirect('booking-detail', pk=booking.pk)
    else:
        # Pre-fill the form if check-in/check-out dates are in URL params
        initial = {}
        if request.GET.get('check_in'):
            initial['check_in'] = request.GET.get('check_in')
        if request.GET.get('check_out'):
            initial['check_out'] = request.GET.get('check_out')
        if request.GET.get('guests'):
            initial['guests'] = request.GET.get('guests')
        
        form = BookingForm(initial=initial)
    
    return render(request, 'bookings/booking_create.html', {
        'form': form,
        'property': property
    })


@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, id=pk)
    
    # Only allow cancellation if the user is the guest or the property owner
    if request.user != booking.guest and request.user != booking.rental_property.owner:
        messages.error(request, 'You do not have permission to cancel this booking.')
        return redirect('home')
    
    # Only allow cancellation if the booking is pending or confirmed
    if booking.status not in ['pending', 'confirmed']:
        messages.error(request, 'This booking cannot be cancelled.')
        return redirect('booking-detail', pk=booking.pk)
    
    # Check if check-in date has passed
    if booking.check_in < date.today():
        messages.error(request, 'Cannot cancel a booking after check-in date.')
        return redirect('booking-detail', pk=booking.pk)
    
    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        
        if request.user == booking.guest:
            messages.success(request, 'Your booking has been cancelled successfully.')
            return redirect('user-bookings')
        else:
            messages.success(request, 'The booking has been cancelled successfully.')
            return redirect('host-bookings')
    
    return render(request, 'bookings/booking_cancel.html', {'booking': booking})


@login_required
def confirm_booking(request, pk):
    booking = get_object_or_404(Booking, id=pk)
    
    # Only allow confirmation if the user is the property owner
    if request.user != booking.rental_property.owner:
        messages.error(request, 'Only the property owner can confirm bookings.')
        return redirect('home')
    
    # Only allow confirmation if the booking is pending
    if booking.status != 'pending':
        messages.error(request, 'This booking cannot be confirmed.')
        return redirect('booking-detail', pk=booking.pk)
    
    if request.method == 'POST':
        booking.status = 'confirmed'
        booking.save()
        messages.success(request, 'The booking has been confirmed successfully.')
        return redirect('host-bookings')
    
    return render(request, 'bookings/booking_confirm.html', {'booking': booking})
