from rest_framework.response import Response
from django.http import FileResponse, JsonResponse
from rest_framework.decorators import api_view
from .models import Trip
from .serializers import TripSerializer

@api_view(['POST'])
def create_trip(request):
    serializer = TripSerializer(data=request.data)
    if serializer.is_valid():
        trip = serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=400)

@api_view(['GET'])
def trip_history(request):
    trips = Trip.objects.all().order_by('-created_at')
    serializer = TripSerializer(trips, many=True)
    return Response(serializer.data)

def download_trip_log(request, trip_id):
    """Serve the trip log PDF for download."""
    trip = Trip.objects.get(id=trip_id)
    file_path = trip.log_pdf.path
    return FileResponse(open(file_path, "rb"), content_type="application/pdf")