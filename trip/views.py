from rest_framework.response import Response
from django.http import FileResponse, JsonResponse
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from .models import Trip
from .serializers import TripSerializer
from logs.generate_log import generate_eld_log
import os

# Ensure the media/logs directory exists
LOG_DIR = "media/logs"
os.makedirs(LOG_DIR, exist_ok=True)

@api_view(['POST'])
def create_trip(request):
    """Create a new trip and generate an ELD log PDF."""
    serializer = TripSerializer(data=request.data)
    
    if serializer.is_valid():
        trip = serializer.save()

        # ✅ Print trip details for debugging
        print(f"✅ Saved Trip {trip.id}: {trip.pickup_location_name} → {trip.dropoff_location_name}")

        # ✅ Prepare trip data for log generation
        trip_data = {
            "pickup_location": trip.pickup_location_name,
            "dropoff_location": trip.dropoff_location_name,
            "current_cycle_used": trip.current_cycle_used,
            "hours": [(i, "Driving") if i % 3 == 0 else (i, "Off Duty") for i in range(24)]
        }

        # ✅ Generate ELD Log PDF
        output_path = f"{LOG_DIR}/trip_{trip.id}.pdf"
        generate_eld_log(trip_data, output_path)
        print(f"✅ ELD Log Generated: {output_path}")

        # ✅ Assign PDF path to trip and save
        trip.log_pdf.name = output_path
        trip.save()

        # ✅ Return JSON response with absolute PDF URL
        return JsonResponse({
            "trip_id": trip.id,
            "pickup_location": trip.pickup_location_name,
            "dropoff_location": trip.dropoff_location_name,
            "log_pdf": request.build_absolute_uri(trip.log_pdf.url)
        })
    
    return Response(serializer.errors, status=400)


@api_view(['GET'])
def trip_history(request):
    """Retrieve all past trips ordered by latest."""
    trips = Trip.objects.all().order_by('-created_at')
    serializer = TripSerializer(trips, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def download_trip_log(request, trip_id):
    """Serve the trip log PDF for download."""
    trip = get_object_or_404(Trip, id=trip_id)

    if not trip.log_pdf:
        return JsonResponse({"error": "Log file not found for this trip"}, status=404)

    file_path = trip.log_pdf.path
    if not os.path.exists(file_path):
        return JsonResponse({"error": "Log file is missing from the server"}, status=404)

    return FileResponse(open(file_path, "rb"), content_type="application/pdf")
