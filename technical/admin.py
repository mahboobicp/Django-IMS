from django.contrib import admin

# Register your models here.
from .models import Plot

# Simple model registration
admin.site.register(Plot)