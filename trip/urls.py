from django.urls import path
from .views import create_trip, trip_history, download_trip_log

urlpatterns = [
    path('trips/', create_trip, name='create-trip'),
    path('history/', trip_history, name='trip-history'),
    path('download/<int:trip_id>/', download_trip_log, name='download-trip-log'),
]
