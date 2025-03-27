from rest_framework.response import Response
from django.http import FileResponse, JsonResponse
from rest_framework.decorators import api_view
from .models import Trip
from .serializers import TripSerializer
from logs.generate_log import generate_eld_log 
import os

@api_view(['POST'])
def create_trip(request):
    serializer = TripSerializer(data=request.data)
    if serializer.is_valid():
        trip = serializer.save()
        # Generate ELD Log
        print("✅ Saved Trip:", trip.id, trip.pickup_location, trip.dropoff_location, trip.current_cycle_used)
        output_path = f"media/logs/trip_{trip.id}.pdf"
        trip_data = {
            "pickup_location": trip.pickup_location,
            "dropoff_location": trip.dropoff_location,
            "current_cycle_used": trip.current_cycle_used,
            "hours": [(i, "Driving") if i % 3 == 0 else (i, "Off Duty") for i in range(24)]
        }
        generate_eld_log(trip_data, output_path)
        print("✅ ELD Log Generated:", output_path)
        trip.log_pdf = output_path
        trip.save()

        # Return JSON response with absolute PDF URL
        return JsonResponse({
            "trip_id": trip.id,
            "log_pdf": request.build_absolute_uri(trip.log_pdf.url)
        })

    return Response(serializer.errors, status=400)

@api_view(['GET'])
def trip_history(request):
    trips = Trip.objects.all().order_by('-created_at')
    serializer = TripSerializer(trips, many=True)
    return Response(serializer.data)

def download_trip_log(request, trip_id):
    """Serve the trip log PDF for download."""
    trip = Trip.objects.get(id=trip_id)
    print(trip)
    file_path = trip.log_pdf.path
    return FileResponse(open(file_path, "rb"), content_type="application/pdf")