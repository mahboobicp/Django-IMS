from django.db import models

# Create your models here.
from django.db import models

class Plot(models.Model):
    plot_number = models.CharField(max_length=100)
    location = models.CharField(max_length=255, blank=True, null=True)
    plot_status = models.CharField(max_length=100, blank=True, null=True)
    land_type = models.CharField(max_length=100, blank=True, null=True)
    plot_area = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    coverd_area = models.DecimalField(max_digits=10, decimal_places=2,blank=True, null=True)
    cluped = models.BooleanField(default=False,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.plot_number
