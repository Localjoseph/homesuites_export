from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Amenity(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Amenities"


class Property(models.Model):
    PROPERTY_TYPES = [
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('villa', 'Villa'),
        ('cabin', 'Cabin'),
        ('condo', 'Condominium'),
    ]
    
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    title = models.CharField(max_length=200)
    description = models.TextField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.DecimalField(max_digits=3, decimal_places=1)
    accommodates = models.PositiveIntegerField(help_text="Maximum number of guests")
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    amenities = models.ManyToManyField(Amenity, related_name='properties', blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('property-detail', kwargs={'pk': self.pk})
    
    @property
    def main_image(self):
        first_image = self.images.first()
        if first_image:
            return first_image.image.url
        return None
    
    class Meta:
        verbose_name_plural = "Properties"


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_images')
    caption = models.CharField(max_length=100, blank=True)
    is_main = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Image for {self.property.title}"
