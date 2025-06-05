from django.urls import path
from . import views

urlpatterns = [
    path('', views.PropertyListView.as_view(), name='property-list'),
    path('<int:pk>/', views.PropertyDetailView.as_view(), name='property-detail'),
    path('new/', views.PropertyCreateView.as_view(), name='property-create'),
    path('<int:pk>/update/', views.PropertyUpdateView.as_view(), name='property-update'),
    path('<int:pk>/delete/', views.PropertyDeleteView.as_view(), name='property-delete'),
    path('search/', views.property_search, name='property-search'),
    path('my-properties/', views.UserPropertyListView.as_view(), name='user-properties'),
]
