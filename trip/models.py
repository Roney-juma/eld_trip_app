from django.db import models
class Trip(models.Model):
    current_location = models.CharField(max_length=255)
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)
    current_cycle_used = models.FloatField()
    route_data = models.JSONField(null=True)
    log_pdf = models.FileField(upload_to="logs/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Trip {self.id}: {self.pickup_location} -> {self.dropoff_location} in {self.current_cycle_used} hrs"
