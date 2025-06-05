from django.contrib import admin
from .models import Booking

class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'guest', 'rental_property', 'check_in', 'check_out', 'status')
    list_filter = ('status', 'check_in', 'check_out')
    search_fields = ('guest__username', 'rental_property__title')
    readonly_fields = ('booking_date',)

admin.site.register(Booking, BookingAdmin)
