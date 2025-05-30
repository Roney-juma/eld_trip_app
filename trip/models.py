from django.db import models

class Trip(models.Model):
    pickup_location_name = models.CharField(max_length=255)
    pickup_latitude = models.FloatField()
    pickup_longitude = models.FloatField()
    dropoff_location_name = models.CharField(max_length=255)
    dropoff_latitude = models.FloatField()
    dropoff_longitude = models.FloatField()
    current_cycle_used = models.FloatField()
    route_data = models.JSONField(null=True, blank=True)
    log_pdf = models.FileField(upload_to="logs/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Return all the trip details in the model
        return f"{self.pickup_location_name} to {self.dropoff_location_name}"
        
