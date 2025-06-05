from django.db import models
from django.contrib.auth.models import User
from properties.models import Property
from django.urls import reverse
from decimal import Decimal
from datetime import datetime

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    guest = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    rental_property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='bookings')
    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.PositiveIntegerField()
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    special_requests = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.guest.username}'s booking at {self.rental_property.title}"
    
    def get_absolute_url(self):
        return reverse('booking-detail', kwargs={'pk': self.pk})
    
    def save(self, *args, **kwargs):
        # Calculate total price if not already set
        if not self.total_price:
            # Calculate number of nights
            delta = self.check_out - self.check_in
            nights = delta.days
            # Calculate total price
            self.total_price = self.rental_property.price_per_night * Decimal(nights)
        
        super().save(*args, **kwargs)
    
    @property
    def is_active(self):
        return self.status in ['pending', 'confirmed']
    
    @property
    def is_past(self):
        return datetime.now().date() > self.check_out