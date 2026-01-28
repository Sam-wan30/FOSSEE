from django.contrib import admin
from .models import EquipmentDataset, EquipmentTypeDistribution


@admin.register(EquipmentDataset)
class EquipmentDatasetAdmin(admin.ModelAdmin):
    list_display = ['name', 'uploaded_at', 'total_count', 'avg_flowrate', 'avg_pressure', 'avg_temperature']
    list_filter = ['uploaded_at']
    readonly_fields = ['uploaded_at']


@admin.register(EquipmentTypeDistribution)
class EquipmentTypeDistributionAdmin(admin.ModelAdmin):
    list_display = ['dataset', 'equipment_type', 'count']
    list_filter = ['dataset', 'equipment_type']
