from rest_framework import serializers
from .models import EquipmentDataset, EquipmentTypeDistribution


class EquipmentTypeDistributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EquipmentTypeDistribution
        fields = ['equipment_type', 'count']


class EquipmentDatasetSerializer(serializers.ModelSerializer):
    type_distributions = EquipmentTypeDistributionSerializer(many=True, read_only=True)
    
    class Meta:
        model = EquipmentDataset
        fields = ['id', 'name', 'uploaded_at', 'total_count', 'avg_flowrate', 
                 'avg_pressure', 'avg_temperature', 'type_distributions']


class DataSummarySerializer(serializers.Serializer):
    total_count = serializers.IntegerField()
    avg_flowrate = serializers.FloatField()
    avg_pressure = serializers.FloatField()
    avg_temperature = serializers.FloatField()
    equipment_type_distribution = serializers.DictField()
