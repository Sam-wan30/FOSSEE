# Chemical Equipment Parameter Visualizer

A hybrid web and desktop application for visualizing and analyzing chemical equipment data from CSV files. The application consists of a Django REST API backend, a React web frontend, and a PyQt5 desktop frontend.

## Features

- **CSV Upload**: Upload CSV files containing chemical equipment data via web or desktop interface
- **Data Analysis**: Automatic calculation of summary statistics (total count, averages, type distribution)
- **Data Visualization**: Interactive charts using Chart.js (web) and Matplotlib (desktop)
- **History Management**: Stores and displays the last 5 uploaded datasets
- **PDF Reports**: Generate and download PDF reports for any dataset
- **Basic Authentication**: Secure access with username/password authentication
- **Data Tables**: View full equipment data in tabular format

## Tech Stack

### Backend
- **Django 4.2.7**: Web framework
- **Django REST Framework**: API development
- **Pandas**: CSV parsing and data analysis
- **SQLite**: Database for storing dataset metadata
- **ReportLab**: PDF report generation

### Web Frontend
- **React 18.2.0**: UI framework
- **Chart.js**: Data visualization
- **Axios**: HTTP client

### Desktop Frontend
- **PyQt5**: Desktop GUI framework
- **Matplotlib**: Data visualization

## Project Structure

```
FOSSEE/
├── backend/                    # Django backend
│   ├── chemical_equipment/     # Django project settings
│   ├── equipment/              # Main app with models, views, serializers
│   ├── manage.py
│   ├── requirements.txt
│   └── media/                  # Uploaded CSV files (created automatically)
├── frontend/                   # React web application
│   ├── public/
│   ├── src/
│   │   ├── App.js
│   │   ├── index.js
│   │   └── index.css
│   └── package.json
├── desktop/                    # PyQt5 desktop application
│   ├── main.py
│   └── requirements.txt
├── sample_equipment_data.csv   # Sample CSV file for testing
└── README.md
```

## Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher and npm
- Git

## Quick Start - Running the Application

To run the complete application, you need to open 3 separate terminals and execute the following commands:

### Terminal 1: Backend Server (Django)
```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment (if not already done)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations (first time only)
python manage.py makemigrations
python manage.py migrate

# Create superuser (first time only)
python manage.py createsuperuser

# Start the Django development server
python manage.py runserver
```

The backend API will be available at `http://localhost:8000`

### Terminal 2: Web Frontend (React)
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (first time only)
npm install

# Start the React development server
npm start
```

The web application will be available at `http://localhost:3000`

### Terminal 3: Desktop Application (PyQt5)
```bash
# Navigate to desktop directory
cd desktop

# Create and activate virtual environment (if not already done)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (first time only)
pip install -r requirements.txt

# Run the desktop application
python main.py
```

The desktop application will open in a new window.

### Important Notes:
- **Terminal 1 must be running first** - the desktop and web applications depend on the backend API
- Use the same superuser credentials for both web and desktop login
- All three terminals should remain open while using the application
- The sample CSV file `sample_equipment_data.csv` is available in the root directory for testing

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
