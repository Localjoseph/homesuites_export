from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Property, PropertyImage
from .forms import PropertyForm, PropertyImageForm, PropertySearchForm
from bookings.models import Booking
from bookings.forms import BookingForm


class PropertyListView(ListView):
    model = Property
    template_name = 'properties/property_list.html'
    context_object_name = 'properties'
    paginate_by = 12
    
    def get_queryset(self):
        return Property.objects.filter(is_available=True).order_by('-created_at')


class UserPropertyListView(LoginRequiredMixin, ListView):
    model = Property
    template_name = 'properties/user_properties.html'
    context_object_name = 'properties'
    paginate_by = 12
    
    def get_queryset(self):
        return Property.objects.filter(owner=self.request.user).order_by('-created_at')


class PropertyDetailView(DetailView):
    model = Property
    template_name = 'properties/property_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['booking_form'] = BookingForm()
        
        # Check if the property has any bookings and if the user is the owner
        if self.request.user.is_authenticated and self.request.user == self.object.owner:
            context['bookings'] = Booking.objects.filter(property=self.object).order_by('check_in')
            
        return context


class PropertyCreateView(LoginRequiredMixin, CreateView):
    model = Property
    form_class = PropertyForm
    template_name = 'properties/property_create.html'
    
    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        
        # Handle multiple image uploads
        images = self.request.FILES.getlist('images')
        for image in images:
            PropertyImage.objects.create(property=self.object, image=image)
        
        messages.success(self.request, 'Property has been created successfully!')
        return response


class PropertyUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Property
    form_class = PropertyForm
    template_name = 'properties/property_update.html'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Handle multiple image uploads
        images = self.request.FILES.getlist('images')
        for image in images:
            PropertyImage.objects.create(property=self.object, image=image)
        
        messages.success(self.request, 'Property has been updated successfully!')
        return response
    
    def test_func(self):
        property = self.get_object()
        return self.request.user == property.owner


class PropertyDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Property
    template_name = 'properties/property_confirm_delete.html'
    success_url = reverse_lazy('user-properties')
    
    def test_func(self):
        property = self.get_object()
        return self.request.user == property.owner


def property_search(request):
    form = PropertySearchForm(request.GET or None)
    results = Property.objects.filter(is_available=True)
    
    if form.is_valid():
        location = form.cleaned_data.get('location')
        check_in = form.cleaned_data.get('check_in')
        check_out = form.cleaned_data.get('check_out')
        guests = form.cleaned_data.get('guests')
        min_price = form.cleaned_data.get('min_price')
        max_price = form.cleaned_data.get('max_price')
        property_type = form.cleaned_data.get('property_type')
        bedrooms = form.cleaned_data.get('bedrooms')
        
        if location:
            results = results.filter(
                Q(city__icontains=location) | Q(country__icontains=location)
            )
        
        if guests:
            results = results.filter(accommodates__gte=guests)
        
        if min_price:
            results = results.filter(price_per_night__gte=min_price)
        
        if max_price:
            results = results.filter(price_per_night__lte=max_price)
        
        if property_type:
            results = results.filter(property_type=property_type)
        
        if bedrooms:
            results = results.filter(bedrooms__gte=bedrooms)
        
        # Handle booking date filtering
        if check_in and check_out:
            # Exclude properties that are already booked for the selected dates
            booked_properties = Booking.objects.filter(
                Q(check_in__range=[check_in, check_out]) |
                Q(check_out__range=[check_in, check_out]) |
                (Q(check_in__lte=check_in) & Q(check_out__gte=check_out))
            ).values_list('property_id', flat=True)
            
            results = results.exclude(id__in=booked_properties)
    
    return render(request, 'properties/property_search.html', {
        'form': form,
        'results': results
    })
