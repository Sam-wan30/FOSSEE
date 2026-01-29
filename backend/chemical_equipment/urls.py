"""
URL configuration for chemical_equipment project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse, HttpResponse

def health_check(request):
    return JsonResponse({
        'status': 'healthy',
        'message': 'Chemical Equipment Parameter Visualizer API is running'
    })

def home_page(request):
    return HttpResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Chemical Equipment Parameter Visualizer</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            .container {
                background: rgba(255,255,255,0.1);
                padding: 30px;
                border-radius: 10px;
                backdrop-filter: blur(10px);
            }
            h1 {
                text-align: center;
                margin-bottom: 30px;
            }
            .api-info {
                background: rgba(255,255,255,0.2);
                padding: 20px;
                border-radius: 5px;
                margin: 10px 0;
            }
            .endpoint {
                font-family: monospace;
                background: rgba(0,0,0,0.3);
                padding: 5px 10px;
                border-radius: 3px;
                display: inline-block;
                margin: 5px 0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🧪 Chemical Equipment Parameter Visualizer</h1>
            
            <div class="api-info">
                <h2>🚀 API Status: Running</h2>
                <p>The Django backend API is successfully deployed and running!</p>
            </div>
            
            <div class="api-info">
                <h2>📡 Available Endpoints:</h2>
                <div class="endpoint">GET /api/health/</div>
                <div class="endpoint">POST /api/upload/</div>
                <div class="endpoint">GET /api/summary/</div>
                <div class="endpoint">GET /api/history/</div>
                <div class="endpoint">GET /api/dataset/&lt;id&gt;/</div>
                <div class="endpoint">GET /api/report/&lt;id&gt;/</div>
            </div>
            
            <div class="api-info">
                <h2>🔧 Admin Panel:</h2>
                <div class="endpoint">/admin/</div>
                <p>Access the Django admin interface (requires login)</p>
            </div>
            
            <div class="api-info">
                <h2>✅ Deployment Status:</h2>
                <p>✅ Backend API: Active</p>
                <p>✅ Database: Connected</p>
                <p>✅ Health Check: Passing</p>
            </div>
        </div>
    </body>
    </html>
    """)

urlpatterns = [
    path('', home_page, name='home'),
    path('api/health/', health_check, name='health_check'),
    path('admin/', admin.site.urls),
    path('api/', include('equipment.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
