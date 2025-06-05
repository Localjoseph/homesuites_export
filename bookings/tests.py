from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from properties.models import Property
from .models import Booking
from datetime import date, timedelta

class BookingTestCase(TestCase):
    def setUp(self):
        # Create a test user (property owner)
        self.owner = User.objects.create_user(
            username='owner',
            email='owner@example.com',
            password='ownerpassword'
        )
        
        # Create a test user (guest)
        self.guest = User.objects.create_user(
            username='guest',
            email='guest@example.com',
            password='guestpassword'
        )
        
        # Create a test property
        self.property = Property.objects.create(
            owner=self.owner,
            title='Test Property',
            description='A property for testing bookings',
            address='123 Test Street',
            city='Testville',
            country='Testland',
            zip_code='12345',
            price_per_night=100.00,
            bedrooms=2,
            bathrooms=1.5,
            accommodates=4,
            property_type='apartment',
            is_available=True
        )
        
        # Create test booking
        tomorrow = date.today() + timedelta(days=1)
        next_week = date.today() + timedelta(days=7)
        
        self.booking = Booking.objects.create(
            guest=self.guest,
            property=self.property,
            check_in=tomorrow,
            check_out=next_week,
            guests=2,
            status='confirmed'
        )

    def test_booking_creation(self):
        """Test that a booking can be created"""
        self.assertEqual(self.booking.status, 'confirmed')
        self.assertEqual(self.booking.guests, 2)
        self.assertEqual(self.booking.property, self.property)
        
    def test_booking_total_price(self):
        """Test that the total price is calculated correctly"""
        expected_nights = (self.booking.check_out - self.booking.check_in).days
        expected_price = self.property.price_per_night * expected_nights
        self.assertEqual(self.booking.total_price, expected_price)
        
    def test_booking_list_view(self):
        """Test the booking list view requires login"""
        response = self.client.get(reverse('user-bookings'))
        self.assertNotEqual(response.status_code, 200)  # Should redirect to login
        
        # Login as guest and test again
        self.client.login(username='guest', password='guestpassword')
        response = self.client.get(reverse('user-bookings'))
        self.assertEqual(response.status_code, 200)
