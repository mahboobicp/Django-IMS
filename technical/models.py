

# Create your models here.
from django.db import models

class Plot(models.Model):
    plot_number = models.CharField(max_length=100, primary_key=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    plot_status = models.CharField(max_length=100, blank=True, null=True)
    land_type = models.CharField(max_length=100, blank=True, null=True)
    plot_area = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    coverd_area = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    cluped = models.BooleanField(default=False, blank=True, null=True)
    as_bifurcate = models.BooleanField(default=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    # Foreign Key to Zone
    zone = models.ForeignKey(
        'Zone',
        on_delete=models.SET_NULL,  # If a Zone is deleted, its related Plots will also be deleted
        related_name='plots',      # Allows reverse lookup like zone.plots.all()
        blank=True,
        null=True  # Zone can be optional
    )

    def __str__(self):
        return self.plot_number


class Zone(models.Model):
    zone_name = models.CharField(max_length=255, unique=True)  # Zone Name
    total_area = models.DecimalField(max_digits=10, decimal_places=2)  # Total Area
    industrial_area = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Industrial Area
    commercial_area = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Commercial Area
    infrastructure_area = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Infrastructure Area
    address = models.TextField(blank=True, null=True)  # Address
    year_of_development = models.IntegerField(blank=True, null=True)  # Year of Development
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.zone_name

