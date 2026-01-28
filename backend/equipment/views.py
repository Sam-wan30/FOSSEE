import os
import pandas as pd
from django.http import HttpResponse
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import EquipmentDataset, EquipmentTypeDistribution
from .serializers import EquipmentDatasetSerializer, DataSummarySerializer
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from datetime import datetime


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_csv(request):
    """Upload and process CSV file"""
    if 'file' not in request.FILES:
        return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    file = request.FILES['file']
    
    # Validate file extension
    if not file.name.endswith('.csv'):
        return Response({'error': 'File must be a CSV'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Read CSV file
        df = pd.read_csv(file)
        
        # Validate required columns
        required_columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return Response({
                'error': f'Missing required columns: {", ".join(missing_columns)}'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Calculate statistics
        total_count = len(df)
        avg_flowrate = df['Flowrate'].mean()
        avg_pressure = df['Pressure'].mean()
        avg_temperature = df['Temperature'].mean()
        
        # Calculate equipment type distribution
        type_distribution = df['Type'].value_counts().to_dict()
        
        # Save file to media directory
        media_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        os.makedirs(media_dir, exist_ok=True)
        
        file_path = os.path.join(media_dir, f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.name}")
        df.to_csv(file_path, index=False)
        
        # Create dataset record
        dataset = EquipmentDataset.objects.create(
            name=file.name,
            file_path=file_path,
            total_count=total_count,
            avg_flowrate=avg_flowrate,
            avg_pressure=avg_pressure,
            avg_temperature=avg_temperature
        )
        
        # Create type distribution records
        for eq_type, count in type_distribution.items():
            EquipmentTypeDistribution.objects.create(
                dataset=dataset,
                equipment_type=eq_type,
                count=count
            )
        
        # Keep only last 5 datasets
        datasets = EquipmentDataset.objects.all().order_by('-uploaded_at')
        if datasets.count() > 5:
            for old_dataset in datasets[5:]:
                # Delete associated file
                if os.path.exists(old_dataset.file_path):
                    os.remove(old_dataset.file_path)
                old_dataset.delete()
        
        # Return summary
        serializer = EquipmentDatasetSerializer(dataset)
        return Response({
            'message': 'File uploaded successfully',
            'dataset': serializer.data,
            'summary': {
                'total_count': total_count,
                'avg_flowrate': round(avg_flowrate, 2),
                'avg_pressure': round(avg_pressure, 2),
                'avg_temperature': round(avg_temperature, 2),
                'equipment_type_distribution': type_distribution
            }
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_summary(request, dataset_id=None):
    """Get summary statistics for a specific dataset or latest dataset"""
    if dataset_id:
        try:
            dataset = EquipmentDataset.objects.get(id=dataset_id)
        except EquipmentDataset.DoesNotExist:
            return Response({'error': 'Dataset not found'}, status=status.HTTP_404_NOT_FOUND)
    else:
        dataset = EquipmentDataset.objects.first()
        if not dataset:
            return Response({'error': 'No datasets available'}, status=status.HTTP_404_NOT_FOUND)
    
    # Get type distribution
    type_distributions = dataset.type_distributions.all()
    type_dist_dict = {dist.equipment_type: dist.count for dist in type_distributions}
    
    summary = {
        'total_count': dataset.total_count,
        'avg_flowrate': round(dataset.avg_flowrate, 2) if dataset.avg_flowrate else 0,
        'avg_pressure': round(dataset.avg_pressure, 2) if dataset.avg_pressure else 0,
        'avg_temperature': round(dataset.avg_temperature, 2) if dataset.avg_temperature else 0,
        'equipment_type_distribution': type_dist_dict
    }
    
    serializer = DataSummarySerializer(summary)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_history(request):
    """Get history of last 5 uploaded datasets"""
    datasets = EquipmentDataset.objects.all().order_by('-uploaded_at')[:5]
    serializer = EquipmentDatasetSerializer(datasets, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_dataset_data(request, dataset_id):
    """Get full data for a specific dataset"""
    try:
        dataset = EquipmentDataset.objects.get(id=dataset_id)
    except EquipmentDataset.DoesNotExist:
        return Response({'error': 'Dataset not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if not os.path.exists(dataset.file_path):
        return Response({'error': 'Dataset file not found'}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        df = pd.read_csv(dataset.file_path)
        data = df.to_dict('records')
        return Response({'data': data})
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_pdf_report(request, dataset_id):
    """Generate PDF report for a dataset"""
    try:
        dataset = EquipmentDataset.objects.get(id=dataset_id)
    except EquipmentDataset.DoesNotExist:
        return Response({'error': 'Dataset not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Create PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="equipment_report_{dataset_id}.pdf"'
    
    doc = SimpleDocTemplate(response, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Title
    title = Paragraph(f"Chemical Equipment Report - {dataset.name}", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 0.2*inch))
    
    # Summary information
    story.append(Paragraph(f"<b>Upload Date:</b> {dataset.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    story.append(Spacer(1, 0.1*inch))
    
    # Summary table
    summary_data = [
        ['Metric', 'Value'],
        ['Total Equipment Count', str(dataset.total_count)],
        ['Average Flowrate', f"{dataset.avg_flowrate:.2f}" if dataset.avg_flowrate else "N/A"],
        ['Average Pressure', f"{dataset.avg_pressure:.2f}" if dataset.avg_pressure else "N/A"],
        ['Average Temperature', f"{dataset.avg_temperature:.2f}" if dataset.avg_temperature else "N/A"],
    ]
    
    summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Equipment type distribution
    story.append(Paragraph("<b>Equipment Type Distribution</b>", styles['Heading2']))
    story.append(Spacer(1, 0.1*inch))
    
    type_distributions = dataset.type_distributions.all()
    if type_distributions:
        dist_data = [['Equipment Type', 'Count']]
        for dist in type_distributions:
            dist_data.append([dist.equipment_type, str(dist.count)])
        
        dist_table = Table(dist_data, colWidths=[3*inch, 2*inch])
        dist_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(dist_table)
    
    doc.build(story)
    return response
