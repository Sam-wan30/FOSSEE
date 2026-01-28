# Quick Start Guide

## Prerequisites
- Python 3.8+
- Node.js 14+
- npm

## Quick Setup (Linux/macOS)

Run the setup script:
```bash
./setup.sh
```

## Quick Setup (Windows)

Run the setup script:
```cmd
setup.bat
```

## Manual Setup

### 1. Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser  # Create login credentials
python manage.py runserver
```

### 2. Web Frontend
```bash
cd frontend
npm install
npm start
```

### 3. Desktop App
```bash
cd desktop
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Testing

1. Use the provided `sample_equipment_data.csv` file
2. Login with the superuser credentials you created
3. Upload the CSV file
4. View charts, tables, and download PDF reports

## Default URLs

- Web App: http://localhost:3000
- API: http://localhost:8000
- Admin Panel: http://localhost:8000/admin

## Troubleshooting

- **Port conflicts**: Change ports in respective config files
- **CORS errors**: Ensure backend is running before frontend
- **Auth errors**: Use the superuser credentials from `createsuperuser`
