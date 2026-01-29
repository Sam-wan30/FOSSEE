# Complete Terminal Commands to Run the Project

Copy and paste these commands into **3 separate terminal windows**.

---

## TERMINAL 1: Django Backend

```bash
cd /Users/samiksha/FOSSEE/backend
source venv/bin/activate
python manage.py migrate
python manage.py runserver
```

**Expected output:**
```
Watching for file changes with StatReloader
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

**Keep this terminal running!**

---

## TERMINAL 2: React Web Frontend

```bash
cd /Users/samiksha/FOSSEE/frontend
npm install
npm start
```

**Expected output:**
```
Compiled successfully!

You can now view chemical-equipment-visualizer in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000
```

**Keep this terminal running!** The browser should open automatically.

---

## TERMINAL 3: PyQt5 Desktop Application

```bash
cd /Users/samiksha/FOSSEE/desktop
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

**Expected output:**
- A desktop window will open with the application GUI

**Keep this terminal running!**

---

## First Time Setup (If Not Done Already)

If you haven't set up the project yet, run these commands **once** before the above:

### Backend Setup (Terminal 1):
```bash
cd /Users/samiksha/FOSSEE/backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
# Optional: Create superuser for admin access
python manage.py createsuperuser
```

### Frontend Setup (Terminal 2):
```bash
cd /Users/samiksha/FOSSEE/frontend
npm install
```

### Desktop Setup (Terminal 3):
```bash
cd /Users/samiksha/FOSSEE/desktop
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Quick Reference

**Login Credentials:**
- Username: `admin`
- Password: `admin123`

**URLs:**
- Web App: http://localhost:3000
- Backend API: http://localhost:8000/api/
- Admin Panel: http://localhost:8000/admin/

**Sample Data:**
- File: `/Users/samiksha/FOSSEE/sample_equipment_data.csv`

---

## Stopping the Applications

Press `Ctrl+C` in each terminal to stop the respective service.

---

## Troubleshooting

### Backend won't start:
```bash
# Check if port 8000 is in use
lsof -ti:8000

# Kill process if needed
kill -9 $(lsof -ti:8000)

# Then restart
cd /Users/samiksha/FOSSEE/backend
source venv/bin/activate
python manage.py runserver
```

### Frontend won't start:
```bash
# Check if port 3000 is in use
lsof -ti:3000

# Kill process if needed
kill -9 $(lsof -ti:3000)

# Then restart
cd /Users/samiksha/FOSSEE/frontend
npm start
```

### Desktop app issues:
```bash
# Make sure backend is running first
# Then restart desktop app
cd /Users/samiksha/FOSSEE/desktop
source venv/bin/activate
python main.py
```
