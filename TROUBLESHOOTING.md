# Troubleshooting Guide

## Current Status Check

✅ **Backend is running** on port 8000  
✅ **Frontend is running** on port 3000  
✅ **Both services are responding correctly**

---

## Common Issues & Solutions

### 1. Can't Access Web App in Browser

**Problem:** Browser shows error or blank page

**Solutions:**
- Open browser and go to: **http://localhost:3000**
- If that doesn't work, try: **http://127.0.0.1:3000**
- Clear browser cache: `Cmd+Shift+R` (Mac) or `Ctrl+Shift+R` (Windows)
- Check browser console for errors: Press `F12` → Console tab

### 2. Login Not Working

**Problem:** "Invalid credentials" error

**Solutions:**
- Make sure you're using:
  - Username: `admin`
  - Password: `admin123`
- Check if backend is running: http://localhost:8000/admin
- Try logging in at admin panel first: http://localhost:8000/admin

### 3. CORS Errors in Browser Console

**Problem:** "CORS policy" errors

**Solutions:**
- Make sure backend is running on port 8000
- Check backend terminal for errors
- Restart backend:
  ```bash
  cd /Users/samiksha/FOSSEE/backend
  source venv/bin/activate
  python manage.py runserver
  ```

### 4. Frontend Shows "Cannot Connect" or "Network Error"

**Problem:** Frontend can't reach backend

**Solutions:**
- Verify backend is running: http://localhost:8000/api/history/
- Check if ports are correct:
  - Backend: 8000
  - Frontend: 3000
- Restart both services

### 5. Desktop App Won't Start

**Problem:** Desktop window doesn't open or crashes

**Solutions:**
```bash
cd /Users/samiksha/FOSSEE/desktop
source venv/bin/activate
python main.py
```

**If PyQt5 errors:**
```bash
# Reinstall PyQt5
pip install --upgrade PyQt5
```

### 6. File Upload Not Working

**Problem:** CSV upload fails

**Solutions:**
- Make sure file has correct columns:
  - Equipment Name
  - Type
  - Flowrate
  - Pressure
  - Temperature
- Use the sample file: `/Users/samiksha/FOSSEE/sample_equipment_data.csv`
- Check backend terminal for error messages

---

## Quick Restart Commands

### Restart Backend:
```bash
# Stop current backend (Ctrl+C in terminal)
cd /Users/samiksha/FOSSEE/backend
source venv/bin/activate
python manage.py runserver
```

### Restart Frontend:
```bash
# Stop current frontend (Ctrl+C in terminal)
cd /Users/samiksha/FOSSEE/frontend
npm start
```

### Restart Everything:
1. Stop all terminals (Ctrl+C in each)
2. Start Terminal 1 (Backend):
   ```bash
   cd /Users/samiksha/FOSSEE/backend
   source venv/bin/activate
   python manage.py runserver
   ```
3. Start Terminal 2 (Frontend):
   ```bash
   cd /Users/samiksha/FOSSEE/frontend
   npm start
   ```

---

## Verify Everything is Working

1. **Check Backend:**
   - Open: http://localhost:8000/admin
   - Login with admin/admin123
   - Should see Django admin panel

2. **Check Frontend:**
   - Open: http://localhost:3000
   - Should see login page
   - Login with admin/admin123

3. **Test Upload:**
   - Upload `sample_equipment_data.csv`
   - Should see charts and data

---

## Still Not Working?

1. **Check terminal outputs** for error messages
2. **Check browser console** (F12 → Console) for JavaScript errors
3. **Verify all dependencies are installed:**
   ```bash
   # Backend
   cd /Users/samiksha/FOSSEE/backend
   source venv/bin/activate
   pip list | grep -i django
   
   # Frontend
   cd /Users/samiksha/FOSSEE/frontend
   npm list react
   ```

4. **Check file permissions:**
   ```bash
   ls -la /Users/samiksha/FOSSEE/backend/venv
   ls -la /Users/samiksha/FOSSEE/frontend/node_modules
   ```
