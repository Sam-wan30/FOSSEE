import csv
import io
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg, Count
from .models import EquipmentDataset, EquipmentTypeDistribution
from .serializers import EquipmentDatasetSerializer, DataSummarySerializer
import os
from datetime import datetime

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_csv_simple(request):
    """Upload CSV file using Python's csv module instead of pandas"""
    if 'file' not in request.FILES:
        return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    file = request.FILES['file']
    
    if not file.name.endswith('.csv'):
        return Response({'error': 'File must be a CSV'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Read CSV using Python's csv module
        csv_file = io.StringIO(file.read().decode('utf-8'))
        csv_reader = csv.DictReader(csv_file)
        
        # Process data
        equipment_data = []
        type_counts = {}
        total_flowrate = 0
        total_pressure = 0
        total_temperature = 0
        count = 0
        
        for row in csv_reader:
            try:
                # Extract data (assuming CSV has these columns)
                equipment_type = row.get('Equipment Type', row.get('equipment_type', 'Unknown'))
                flowrate = float(row.get('Flowrate', row.get('flowrate', 0)))
                pressure = float(row.get('Pressure', row.get('pressure', 0)))
                temperature = float(row.get('Temperature', row.get('temperature', 0)))
                
                equipment_data.append({
                    'equipment_type': equipment_type,
                    'flowrate': flowrate,
                    'pressure': pressure,
                    'temperature': temperature
                })
                
                # Count equipment types
                type_counts[equipment_type] = type_counts.get(equipment_type, 0) + 1
                
                # Sum for averages
                total_flowrate += flowrate
                total_pressure += pressure
                total_temperature += temperature
                count += 1
                
            except (ValueError, KeyError) as e:
                continue  # Skip invalid rows
        
        if count == 0:
            return Response({'error': 'No valid data found in CSV'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Save file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'{timestamp}_{file.name}'
        file_path = os.path.join('media', 'uploads', filename)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        
        # Create dataset record
        dataset = EquipmentDataset.objects.create(
            filename=filename,
            upload_date=datetime.now(),
            total_count=count,
            avg_flowrate=total_flowrate / count,
            avg_pressure=total_pressure / count,
            avg_temperature=total_temperature / count
        )
        
        # Create type distribution records
        for equipment_type, type_count in type_counts.items():
            EquipmentTypeDistribution.objects.create(
                dataset=dataset,
                equipment_type=equipment_type,
                count=type_count
            )
        
        # Prepare summary
        type_distribution = {k: v for k, v in type_counts.items()}
        
        # Return summary
        serializer = EquipmentDatasetSerializer(dataset)
        return Response({
            'message': 'File uploaded successfully',
            'dataset': serializer.data,
            'summary': {
                'total_count': count,
                'avg_flowrate': round(total_flowrate / count, 2),
                'avg_pressure': round(total_pressure / count, 2),
                'avg_temperature': round(total_temperature / count, 2),
                'equipment_type_distribution': type_distribution
            }
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({'error': f'Error processing file: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
