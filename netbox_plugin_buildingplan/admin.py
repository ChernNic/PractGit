from django.contrib import admin
from .models import BuildingPlan

@admin.register(BuildingPlan)
class BuildingPlanAdmin(admin.ModelAdmin):
    list_display = ['tenant', 'image']
