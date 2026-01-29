# Chemical Equipment Parameter Visualizer

A comprehensive web and desktop application for visualizing and analyzing chemical equipment data from CSV files. Features a modern chemical-themed interface with automatic data analysis, interactive charts, and PDF reporting capabilities.

## 🚀 How to Start (Quick)

**Open 3 terminal windows and run:**

**Terminal 1 (Backend):**
```bash
cd /Users/samiksha/FOSSEE/backend && source venv/bin/activate && python manage.py migrate && python manage.py runserver
```

**Terminal 2 (Frontend):**
```bash
cd /Users/samiksha/FOSSEE/frontend && npm install && npm start
```

**Terminal 3 (Desktop):**
```bash
cd /Users/samiksha/FOSSEE/desktop && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python main.py
```

**Access URLs:**
- 🌐 Web App: http://localhost:3000
- 🔧 Backend API: http://localhost:8000/api/
- ⚙️ Admin Panel: http://localhost:8000/admin/

---

## 🚀 Live Demo

**Web Application**: [Deployed Live Demo on Replit](https://your-replit-url.replit.app) - Full-stack application with real CSV processing and data visualization

**Source Code**: [GitHub Repository](https://github.com/Sam-wan30/FOSSEE)

## 📺 Demo Video

[![Watch Demo Video](https://img.youtube.com/vi/your-video-id/0.jpg)](https://www.youtube.com/watch?v=your-video-id)

*Click the image above to watch a 2-3 minute demo video* *(Video Coming Soon)*

## ✨ Features

### 🎨 Modern Interface
- **Chemical-themed login page** with animated background elements
- **Glass-morphism design** with subtle green glow effects
- **Responsive layout** that works on all devices
- **Professional UI** with smooth transitions and hover effects

### 📊 Data Analysis & Visualization
- **Automatic CSV processing** with intelligent data parsing
- **Real-time statistics** (total count, averages, type distribution)
- **Interactive charts** using Chart.js:
  - Pie chart for equipment type distribution
  - Bar chart for average parameter values
- **Full data tables** with sortable columns
- **Upload history** tracking last 5 datasets

### 📄 Reporting & Export
- **PDF report generation** with comprehensive data summary
- **Downloadable reports** including charts and statistics
- **Data export** capabilities for further analysis

### 🔐 Security & Authentication
- **Secure login system** with username/password authentication
- **Session management** for both web and desktop applications
- **Protected API endpoints** with Django REST Framework

### 💻 Multi-Platform Support
- **Web application** (React + Django)
- **Desktop application** (PyQt5)
- **Cross-platform compatibility** (Windows, macOS, Linux)

## 🛠 Tech Stack

### 🖥 Backend
- **Django 4.2.7**: Web framework
- **Django REST Framework**: API development
- **Pandas**: CSV parsing and data analysis
- **SQLite**: Database for storing dataset metadata
- **ReportLab**: PDF report generation

### 🌐 Web Frontend
- **React 18.2.0**: UI framework
- **Chart.js**: Data visualization
- **Axios**: HTTP client
- **CSS3**: Modern styling with animations

### 🖱 Desktop Frontend
- **PyQt5**: Desktop GUI framework
- **Matplotlib**: Data visualization

## 📁 Project Structure

```
FOSSEE/
├── backend/                    # Django backend API
│   ├── chemical_equipment/     # Django project settings
│   ├── equipment/              # Main app with models, views, serializers
│   ├── manage.py              # Django management script
│   ├── requirements.txt      # Python dependencies
│   └── media/                  # Uploaded CSV files (auto-created)
├── frontend/                   # React web application
│   ├── public/                # Static assets
│   ├── src/
│   │   ├── App.js            # Main React component
│   │   ├── index.js          # React entry point
│   │   └── index.css         # Styling with chemical theme
│   └── package.json          # Node.js dependencies
├── desktop/                    # PyQt5 desktop application
│   ├── main.py               # Desktop app main file
│   └── requirements.txt      # Python dependencies
├── sample_equipment_data.csv  # Sample CSV file for testing
├── setup.sh                  # Linux/macOS setup script
├── setup.bat                 # Windows setup script
└── README.md                 # This file
```

## 🚀 Quick Start

### 🎬 One-Click Setup

**For Linux/macOS:**
```bash
chmod +x setup.sh
./setup.sh
```

**For Windows:**
```bash
setup.bat
```

### � Quick Terminal Commands (3 Windows)

#### **Terminal 1: Backend** 🐍
```bash
cd /Users/samiksha/FOSSEE/backend && source venv/bin/activate && python manage.py migrate && python manage.py runserver
```

#### **Terminal 2: Frontend** 🌐
```bash
cd /Users/samiksha/FOSSEE/frontend && npm install && npm start
```

#### **Terminal 3: Desktop** 🖥️
```bash
cd /Users/samiksha/FOSSEE/desktop && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python main.py
```

### �� Prerequisites

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **Node.js 14+ & npm** - [Download Node.js](https://nodejs.org/)
- **Git** - [Download Git](https://git-scm.com/downloads)

### 🖥️ Manual Setup (3 Terminals Required)

#### **Terminal 1: Backend Server** 🐍
```bash
# Navigate to backend directory
cd /Users/samiksha/FOSSEE/backend

# Activate virtual environment
source venv/bin/activate

# Setup database
python manage.py migrate

# Start Django server
python manage.py runserver
```
📍 **Backend API**: `http://localhost:8000/api/`
📍 **Admin Panel**: `http://localhost:8000/admin/`

#### **Terminal 2: Web Frontend** 🌐
```bash
# Navigate to frontend directory
cd /Users/samiksha/FOSSEE/frontend

# Install dependencies
npm install

# Start React development server
npm start
```
📍 **Web Frontend**: `http://localhost:3000`

#### **Terminal 3: Desktop Application** 🖥️
```bash
# Navigate to desktop directory
cd /Users/samiksha/FOSSEE/desktop

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start desktop application
python main.py
```
📍 **Desktop App**: Opens automatically

### 🚀 Quick Copy-Paste Commands

#### **Terminal 1 (Backend):**
```bash
cd /Users/samiksha/FOSSEE/backend && source venv/bin/activate && python manage.py migrate && python manage.py runserver
```

#### **Terminal 2 (Frontend):**
```bash
cd /Users/samiksha/FOSSEE/frontend && npm install && npm start
```

#### **Terminal 3 (Desktop):**
```bash
cd /Users/samiksha/FOSSEE/desktop && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python main.py
```

### ⚠️ Important Notes
- **Start Terminal 1 first** - other apps depend on the backend API
- **Backend API**: `http://localhost:8000/api/`
- **Web Frontend**: `http://localhost:3000`
- **Admin Panel**: `http://localhost:8000/admin/`
- **Desktop App**: Opens automatically
- **Login**: Use any username/password for web app (no auth required for basic usage)
- Keep **all 3 terminals open** while using the application
- Use `sample_equipment_data.csv` in the root directory for testing

## Setup Instructions

### 1. Backend Setup (Django)

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run database migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create a superuser (for admin access and authentication):
```bash
python manage.py createsuperuser
```
Follow the prompts to create a username and password. **Remember these credentials as you'll need them to login to both web and desktop applications.**

6. Start the Django development server:
```bash
python manage.py runserver
```

The backend API will be available at `http://localhost:8000`

### 2. Web Frontend Setup (React)

1. Open a new terminal and navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the React development server:
```bash
npm start
```

The web application will be available at `http://localhost:3000`

### 3. Desktop Application Setup (PyQt5)

1. Open a new terminal and navigate to the desktop directory:
```bash
cd desktop
```

2. Create a virtual environment (if not using the backend's):
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the desktop application:
```bash
python main.py
```

## Usage

### Web Application

1. Open your browser and navigate to `http://localhost:3000`
2. Login with the superuser credentials you created during backend setup
3. Click "Choose CSV File" and select a CSV file (use `sample_equipment_data.csv` for testing)
4. Click "Upload File" to upload and process the CSV
5. View summary statistics, charts, and data tables
6. Click "View Full Data Table" to see all equipment records
7. Click "Download PDF Report" to generate a PDF report
8. View upload history in the "Upload History" section

### Desktop Application

1. Launch the desktop application by running `python main.py`
2. Enter your username and password (same as web app) and click "Login"
3. Click "Browse CSV File" and select a CSV file
4. Click "Upload File" to upload and process the CSV
5. View summary statistics and charts
6. Click "Load Full Data Table" to view all equipment records
7. Click "Download PDF Report" to generate a PDF report
8. Click "Load History" to view upload history

### CSV File Format

The CSV file must contain the following columns (case-sensitive):
- `Equipment Name`: Name of the equipment
- `Type`: Type of equipment (e.g., Reactor, Distillation Column, etc.)
- `Flowrate`: Flowrate value (numeric)
- `Pressure`: Pressure value (numeric)
- `Temperature`: Temperature value (numeric)

Example:
```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Reactor-001,Reactor,150.5,2.5,85.0
Distillation Column-001,Distillation Column,200.0,1.8,120.5
```

A sample CSV file (`sample_equipment_data.csv`) is provided in the root directory.

## API Endpoints

All endpoints require Basic Authentication.

- `POST /api/upload/` - Upload a CSV file
- `GET /api/summary/` - Get summary for the latest dataset
- `GET /api/summary/<dataset_id>/` - Get summary for a specific dataset
- `GET /api/history/` - Get upload history (last 5 datasets)
- `GET /api/dataset/<dataset_id>/` - Get full data for a dataset
- `GET /api/report/<dataset_id>/` - Generate PDF report for a dataset

## Features in Detail

### Data Summary
- Total equipment count
- Average flowrate, pressure, and temperature
- Equipment type distribution

### Visualizations
- **Pie Chart**: Equipment type distribution
- **Bar Chart**: Average parameter values (Flowrate, Pressure, Temperature)

### History Management
- Automatically stores the last 5 uploaded datasets
- Older datasets are automatically deleted
- Each dataset includes metadata and summary statistics

### PDF Reports
- Comprehensive PDF reports with:
  - Upload date and dataset name
  - Summary statistics
  - Equipment type distribution table

## Troubleshooting

### Backend Issues

1. **Port already in use**: If port 8000 is in use, change it:
   ```bash
   python manage.py runserver 8001
   ```
   Then update the API_BASE_URL in frontend/src/App.js and desktop/main.py

2. **Database errors**: Delete `db.sqlite3` and run migrations again:
   ```bash
   rm db.sqlite3
   python manage.py migrate
   ```

3. **CORS errors**: Ensure `corsheaders` is installed and CORS settings are configured in `settings.py`

### Frontend Issues

1. **Port 3000 in use**: React will automatically use the next available port
2. **API connection errors**: Ensure the Django backend is running on port 8000
3. **Authentication errors**: Verify you're using the correct superuser credentials

### Desktop Application Issues

1. **PyQt5 installation errors**: On some systems, you may need to install system dependencies:
   - Ubuntu/Debian: `sudo apt-get install python3-pyqt5`
   - macOS: `brew install pyqt5`
   - Windows: Usually works with pip install

2. **Connection errors**: Ensure the Django backend is running before starting the desktop app

## Development

### Running Tests

Backend tests:
```bash
cd backend
python manage.py test
```

### Adding New Features

1. Backend: Add new views in `equipment/views.py` and update `equipment/urls.py`
2. Web Frontend: Modify `frontend/src/App.js` and add new components as needed
3. Desktop Frontend: Update `desktop/main.py` with new functionality

## Deployment

### Web Application Deployment

1. Build the React app:
```bash
cd frontend
npm run build
```

2. Configure Django to serve static files in production
3. Deploy to a hosting service (Heroku, AWS, etc.)

### Desktop Application Distribution

1. Use PyInstaller to create an executable:
```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```

## License

This project is created for the FOSSEE intern screening task.

## Contact

For issues or questions, please refer to the project repository.
