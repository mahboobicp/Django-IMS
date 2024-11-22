from django.contrib import admin

# Register your models here.
from .models import Plot, Zone

# Simple model registration
admin.site.register(Plot)
admin.site.register(Zone)