from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Property, Amenity

class PropertyTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testowner',
            email='owner@example.com',
            password='testpassword123'
        )
        
        self.property = Property.objects.create(
            owner=self.user,
            title='Test Property',
            description='A property for testing',
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
        
        self.amenity = Amenity.objects.create(name='WiFi')
        self.property.amenities.add(self.amenity)

    def test_property_creation(self):
        """Test that a property can be created"""
        self.assertEqual(self.property.title, 'Test Property')
        self.assertEqual(self.property.owner, self.user)
        
    def test_property_list_view(self):
        """Test the property list view"""
        response = self.client.get(reverse('property-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Property')
        
    def test_property_detail_view(self):
        """Test the property detail view"""
        response = self.client.get(reverse('property-detail', args=[self.property.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Property')
        self.assertContains(response, 'WiFi')
