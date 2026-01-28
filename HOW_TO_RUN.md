# How to Run the Application

## Quick Start (3 Terminal Windows Required)

You need to run 3 components simultaneously in separate terminals.

---

## Terminal 1: Django Backend

```bash
# Navigate to backend directory
cd /Users/samiksha/FOSSEE/backend

# Create virtual environment (first time only)
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies (first time only)
pip install -r requirements.txt

# Run migrations (first time only)
python manage.py makemigrations
python manage.py migrate

# Create superuser (first time only - remember username/password!)
python manage.py createsuperuser

# Start the server
python manage.py runserver
```

✅ Backend will run at: **http://localhost:8000**

**Keep this terminal running!**

---

## Terminal 2: React Web Frontend

```bash
# Navigate to frontend directory
cd /Users/samiksha/FOSSEE/frontend

# Install dependencies (first time only)
npm install

# Start the React app
npm start
```

✅ Web app will open at: **http://localhost:3000**

**Keep this terminal running!**

---

## Terminal 3: PyQt5 Desktop Application

```bash
# Navigate to desktop directory
cd /Users/samiksha/FOSSEE/desktop

# Create virtual environment (first time only)
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies (first time only)
pip install -r requirements.txt

# Run the desktop app
python main.py
```

✅ Desktop application window will open

---

## First Time Setup Checklist

- [ ] Backend: Create venv, install dependencies, run migrations, create superuser
- [ ] Frontend: Install npm packages
- [ ] Desktop: Create venv, install dependencies

## Running Checklist (Every Time)

- [ ] Terminal 1: Backend server running (http://localhost:8000)
- [ ] Terminal 2: React app running (http://localhost:3000)
- [ ] Terminal 3: Desktop app running (GUI window)

---

## Testing the Application

1. **Web App**: 
   - Open http://localhost:3000 in browser
   - Login with superuser credentials
   - Upload `sample_equipment_data.csv` from project root
   - View charts and data

2. **Desktop App**:
   - Login with same superuser credentials
   - Click "Browse CSV File" and select `sample_equipment_data.csv`
   - Click "Upload File"
   - View charts and data

---

## Troubleshooting

### Backend won't start
- Make sure port 8000 is not in use
- Check if virtual environment is activated
- Verify all dependencies are installed: `pip list`

### Frontend won't start
- Make sure Node.js is installed: `node --version`
- Delete `node_modules` and run `npm install` again
- Check if port 3000 is available

### Desktop app won't start
- Make sure PyQt5 is installed: `pip show PyQt5`
- On macOS, you might need: `brew install pyqt5`
- Check if backend is running first

### Authentication errors
- Make sure you created a superuser: `python manage.py createsuperuser`
- Use the exact username/password you created
- Check backend is running on port 8000

---

## Sample Data

Use the provided file: `/Users/samiksha/FOSSEE/sample_equipment_data.csv`

This file contains 25 equipment records with the required columns:
- Equipment Name
- Type
- Flowrate
- Pressure
- Temperature
