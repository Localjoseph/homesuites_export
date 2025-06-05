from django.urls import path
from . import views

urlpatterns = [
    path('', views.BookingListView.as_view(), name='user-bookings'),
    path('hosting/', views.HostBookingListView.as_view(), name='host-bookings'),
    path('<int:pk>/', views.BookingDetailView.as_view(), name='booking-detail'),
    path('create/<int:property_id>/', views.create_booking, name='create-booking'),
    path('<int:pk>/cancel/', views.cancel_booking, name='cancel-booking'),
    path('<int:pk>/confirm/', views.confirm_booking, name='confirm-booking'),
]
