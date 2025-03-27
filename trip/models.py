from django.db import models

class Trip(models.Model):
    # Current Location
    current_location_name = models.CharField(max_length=255)
    current_lat = models.FloatField()
    current_lng = models.FloatField()

    # Pickup Location
    pickup_location_name = models.CharField(max_length=255)
    pickup_lat = models.FloatField()
    pickup_lng = models.FloatField()

    # Dropoff Location
    dropoff_location_name = models.CharField(max_length=255)
    dropoff_lat = models.FloatField()
    dropoff_lng = models.FloatField()

    current_cycle_used = models.FloatField()
    route_data = models.JSONField(null=True, blank=True)

    # Log PDF File
    log_pdf = models.FileField(upload_to="logs/", blank=True, null=True)

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Trip {self.id}: {self.pickup_location_name} → {self.dropoff_location_name} in {self.current_cycle_used} hrs"
