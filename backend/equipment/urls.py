from django.urls import path
from . import views
from . import views_health

urlpatterns = [
    path('health/', views_health.health_check, name='health_check'),
    path('upload/', views.upload_csv, name='upload_csv'),
    path('summary/', views.get_summary, name='get_summary'),
    path('summary/<int:dataset_id>/', views.get_summary, name='get_summary_by_id'),
    path('history/', views.get_history, name='get_history'),
    path('dataset/<int:dataset_id>/', views.get_dataset_data, name='get_dataset_data'),
    path('report/<int:dataset_id>/', views.generate_pdf_report, name='generate_pdf_report'),
]
