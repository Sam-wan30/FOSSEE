# 🚀 Deployment Guide

## 🌐 Web Application Deployment

### Option 1: Heroku (Recommended for Beginners)

#### Prerequisites
- Heroku account (free tier available)
- Heroku CLI installed
- Git repository initialized

#### Deployment Steps

1. **Install Heroku CLI**
```bash
# macOS
brew tap heroku/brew && brew install heroku

# Windows
# Download from https://devcenter.heroku.com/articles/heroku-cli
```

2. **Login to Heroku**
```bash
heroku login
```

3. **Create Heroku App**
```bash
heroku create chemical-equipment-visualizer
```

4. **Add Buildpacks**
```bash
heroku buildpacks:set heroku/python
heroku buildpacks:add --index 1 heroku/nodejs
```

5. **Configure Environment Variables**
```bash
heroku config:set DJANGO_SETTINGS_MODULE=chemical_equipment.settings.production
heroku config:set PYTHONPATH=/app/backend
```

6. **Create Procfile**
```bash
echo "web: cd backend && gunicorn chemical_equipment.wsgi:application --bind 0.0.0.0:$PORT" > Procfile
echo "release: cd backend && python manage.py migrate" >> Procfile
```

7. **Update Django Settings for Production**
```python
# backend/chemical_equipment/settings/production.py
from .base import *
import dj_database_url

DEBUG = False
ALLOWED_HOSTS = ['your-app-name.herokuapp.com']

# Database
DATABASES = {
    'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
}

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Security
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

8. **Deploy**
```bash
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

### Option 2: Vercel (React Frontend) + DigitalOcean (Backend)

#### Frontend Deployment (Vercel)

1. **Install Vercel CLI**
```bash
npm i -g vercel
```

2. **Build React App**
```bash
cd frontend
npm run build
```

3. **Deploy to Vercel**
```bash
vercel --prod
```

#### Backend Deployment (DigitalOcean)

1. **Create Droplet** (Ubuntu 20.04 recommended)
2. **Setup Server**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3-pip python3-venv nginx -y

# Clone repository
git clone https://github.com/yourusername/chemical-equipment-visualizer.git
cd chemical-equipment-visualizer
```

3. **Configure Gunicorn and Nginx**
```bash
# Install Gunicorn
pip install gunicorn

# Create systemd service
sudo nano /etc/systemd/system/chemical-equipment.service
```

```ini
[Unit]
Description=Chemical Equipment Django App
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/your/app/backend
ExecStart=/path/to/your/venv/bin/gunicorn chemical_equipment.wsgi:application --workers 3 --bind unix:/run/chemical-equipment.sock

[Install]
WantedBy=multi-user.target
```

4. **Configure Nginx**
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://unix:/run/chemical-equipment.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ {
        alias /path/to/your/app/backend/staticfiles/;
    }
}
```

### Option 3: Docker Deployment

#### Create Dockerfile for Backend
```dockerfile
# backend/Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "chemical_equipment.wsgi:application", "--bind", "0.0.0.0:8000"]
```

#### Create Dockerfile for Frontend
```dockerfile
# frontend/Dockerfile
FROM node:16-alpine as build

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

#### Create docker-compose.yml
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - DATABASE_URL=sqlite:///db.sqlite3
    volumes:
      - ./backend:/app
      - static_volume:/app/staticfiles

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend

volumes:
  static_volume:
```

#### Deploy with Docker
```bash
docker-compose up -d --build
```

## 🖱 Desktop Application Distribution

### Windows

1. **Install PyInstaller**
```bash
pip install pyinstaller
```

2. **Create Executable**
```bash
cd desktop
pyinstaller --onefile --windowed --icon=icon.ico --add-data="../sample_equipment_data.csv;." main.py
```

3. **Create Installer (Optional)**
- Use NSIS or Inno Setup for professional installer
- Include all dependencies and sample files

### macOS

1. **Create App Bundle**
```bash
cd desktop
pyinstaller --windowed --onefile --icon=icon.icns --add-data="../sample_equipment_data.csv:." main.py
```

2. **Create DMG**
```bash
# Create DMG installer
hdiutil create -volname "Chemical Equipment Visualizer" -srcfolder dist/ -ov -format UDZO chemical-equipment-visualizer.dmg
```

### Linux

1. **Create AppImage**
```bash
cd desktop
pyinstaller --onefile --windowed main.py
# Use AppImageTool for distribution
```

2. **Create .deb Package (Ubuntu/Debian)**
```bash
# Use fpm or dpkg-deb for creating packages
```

## 🔧 Environment Configuration

### Production Environment Variables

```bash
# Backend
DJANGO_SETTINGS_MODULE=chemical_equipment.settings.production
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@localhost/dbname

# Frontend
REACT_APP_API_URL=https://your-api-domain.com/api
REACT_APP_ENVIRONMENT=production
```

### Security Considerations

1. **HTTPS Setup**
   - Use SSL certificates (Let's Encrypt recommended)
   - Configure HSTS headers
   - Force HTTPS redirects

2. **Database Security**
   - Use environment variables for credentials
   - Regular backups
   - Connection pooling

3. **API Security**
   - Rate limiting
   - CORS configuration
   - Input validation

## 📊 Monitoring & Analytics

### Application Monitoring

1. **Error Tracking**
   - Sentry for error monitoring
   - Log aggregation with ELK stack

2. **Performance Monitoring**
   - New Relic or DataDog
   - Google Analytics for frontend

3. **Health Checks**
```python
# Add to Django views.py
@api_view(['GET'])
def health_check(request):
    return Response({'status': 'healthy'}, status=200)
```

## 🔄 CI/CD Pipeline

### GitHub Actions Example

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      - name: Run tests
        run: |
          cd backend
          python manage.py test

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Heroku
        uses: akhileshns/heroku-deploy@v3.12.12
        with:
          heroku_api_key: ${{secrets.HEROKU_API_KEY}}
          heroku_app_name: ${{secrets.HEROKU_APP_NAME}}
          heroku_email: ${{secrets.HEROKU_EMAIL}}
```

## 📋 Deployment Checklist

### Pre-Deployment
- [ ] All tests passing
- [ ] Environment variables configured
- [ ] Database migrations tested
- [ ] Static files collected
- [ ] Security headers configured
- [ ] Backup strategy in place

### Post-Deployment
- [ ] Application accessible via HTTPS
- [ ] All API endpoints responding
- [ ] File uploads working
- [ ] PDF generation functional
- [ ] Monitoring alerts configured
- [ ] Documentation updated

## 🆘 Troubleshooting

### Common Issues

1. **Static Files Not Loading**
   - Run `collectstatic` command
   - Check Nginx/Apache configuration
   - Verify file permissions

2. **Database Connection Errors**
   - Check DATABASE_URL format
   - Verify database server is running
   - Check firewall settings

3. **CORS Issues**
   - Configure CORS properly in Django settings
   - Add frontend domain to allowed origins

4. **Memory Issues**
   - Increase server RAM
   - Optimize database queries
   - Implement caching

### Performance Optimization

1. **Database Optimization**
   - Add database indexes
   - Use connection pooling
   - Implement query optimization

2. **Frontend Optimization**
   - Code splitting
   - Image optimization
   - CDN for static assets

3. **Backend Optimization**
   - Implement caching (Redis)
   - Use load balancer
   - Optimize Django settings
