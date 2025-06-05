from django.contrib import admin
from .models import Property, PropertyImage, Amenity

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 3

class PropertyAdmin(admin.ModelAdmin):
    inlines = [PropertyImageInline]
    list_display = ('title', 'owner', 'price_per_night', 'address', 'is_available')
    list_filter = ('is_available', 'property_type')
    search_fields = ('title', 'description', 'address')

admin.site.register(Property, PropertyAdmin)
admin.site.register(Amenity)
