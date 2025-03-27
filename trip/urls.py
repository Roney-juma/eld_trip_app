from django.urls import path
from .views import create_trip, trip_history

urlpatterns = [
    path('trips/', create_trip, name='create-trip'),
    path('history/', trip_history, name='trip-history'),
]
