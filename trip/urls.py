from django.urls import path
from .views import TripListCreateView

urlpatterns = [
    path('/', TripListCreateView.as_view(), name='trip-list-create'),
]