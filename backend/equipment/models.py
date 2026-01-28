from django.db import models
from django.utils import timezone


class EquipmentDataset(models.Model):
    """Model to store uploaded datasets (keeping last 5)"""
    name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(default=timezone.now)
    file_path = models.CharField(max_length=500)
    total_count = models.IntegerField(default=0)
    avg_flowrate = models.FloatField(null=True, blank=True)
    avg_pressure = models.FloatField(null=True, blank=True)
    avg_temperature = models.FloatField(null=True, blank=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.name} - {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"


class EquipmentTypeDistribution(models.Model):
    """Model to store equipment type distribution for each dataset"""
    dataset = models.ForeignKey(EquipmentDataset, on_delete=models.CASCADE, related_name='type_distributions')
    equipment_type = models.CharField(max_length=100)
    count = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.dataset.name} - {self.equipment_type}: {self.count}"
