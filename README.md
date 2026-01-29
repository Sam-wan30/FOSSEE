# Chemical Equipment Parameter Visualizer

A comprehensive web and desktop application for visualizing and analyzing chemical equipment data from CSV files. Features a modern chemical-themed interface with automatic data analysis, interactive charts, and PDF reporting capabilities.

🎯 **FOSSEE Internship Screening Task Submission**

---

## � Submission Requirements

✅ **README file with setup instructions** - Available below  
📹 **Short demo video (2-3 minutes)** - [Watch Demo Video](https://youtube.com/your-video-link) *(Coming Soon)*  
🌐 **Deployment link for web version** - [Live Demo on Replit](https://12dc32cc-49fc-45af-b903-ef8bfd22ac45-00-2w8o2qigt10hq.sisko.replit.dev/)

---

## 🚀 Quick Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 14+ & npm
- Git

### 3-Terminal Setup

**Terminal 1 - Backend:**
```bash
cd /Users/samiksha/FOSSEE/backend
source venv/bin/activate
python manage.py migrate
python manage.py runserver
```

**Terminal 2 - Web Frontend:**
```bash
cd /Users/samiksha/FOSSEE/frontend
npm install
npm start
```

**Terminal 3 - Desktop Application:**
```bash
cd /Users/samiksha/FOSSEE/desktop
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Access URLs
- 🌐 **Web App**: http://localhost:3000
- 🔧 **Backend API**: http://localhost:8000/api/
- ⚙️ **Admin Panel**: http://localhost:8000/admin/
- 🖥️ **Desktop App**: Opens automatically

---

## 🎥 Demo Video

[![Watch Demo Video](https://img.youtube.com/vi/your-video-id/0.jpg)](https://www.youtube.com/watch?v=your-video-id)

*Click the image above to watch the 2-3 minute demo video covering both web and desktop applications*

---

## 🌐 Live Deployment

**Web Application**: [Deployed Live Demo on Replit](https://your-replit-url.replit.app)

- Full-stack application with real CSV processing
- Interactive data visualization
- PDF report generation
- Multi-platform support

---

## ✨ Key Features

### 🎨 Modern Interface
- Chemical-themed login page with animated background
- Glass-morphism design with green glow effects
- Responsive layout for all devices
- Professional UI with smooth transitions

### 📊 Data Analysis & Visualization
- Automatic CSV processing with intelligent parsing
- Real-time statistics (total count, averages, type distribution)
- Interactive charts using Chart.js:
  - Pie chart for equipment type distribution
  - Bar chart for average parameter values
- Sortable data tables with full dataset access
- Upload history tracking (last 5 datasets)

### � Reporting & Export
- One-click PDF report generation
- Comprehensive data summary with charts
- Downloadable reports for sharing

### 🔐 Security & Authentication
- Secure login system with username/password
- Session management for web and desktop
- Protected API endpoints with Django REST Framework

### 💻 Multi-Platform Support
- 🌐 Web Application (React + Django)
- 🖥️ Desktop Application (PyQt5)
- Cross-platform compatibility (Windows, macOS, Linux)

---

## 🛠 Technical Stack

### Backend
- **Django 4.2.7** - Web framework
- **Django REST Framework** - API development
- **Pandas** - CSV parsing and data analysis
- **SQLite** - Database for metadata
- **ReportLab** - PDF report generation

### Web Frontend
- **React 18.2.0** - UI framework
- **Chart.js** - Data visualization
- **Axios** - HTTP client
- **CSS3** - Modern styling with animations

### Desktop Application
- **PyQt5** - Desktop GUI framework
- **Matplotlib** - Data visualization

---

## 📁 Project Structure

```
FOSSEE/
├── backend/                    # Django backend API
│   ├── chemical_equipment/     # Django project settings
│   ├── equipment/              # Main app (models, views, serializers)
│   ├── manage.py              # Django management script
│   └── requirements.txt      # Python dependencies
├── frontend/                   # React web application
│   ├── src/
│   │   ├── App.js            # Main React component
│   │   └── index.css         # Chemical-themed styling
│   └── package.json          # Node.js dependencies
├── desktop/                    # PyQt5 desktop application
│   ├── main.py               # Desktop app main file
│   └── requirements.txt      # Python dependencies
├── sample_equipment_data.csv  # Sample CSV for testing
└── README.md                 # This file
```

---

## 📊 CSV Data Format

**Required Columns:**
- `Equipment Name` - Name of the equipment
- `Type` - Equipment type (Reactor, Column, etc.)
- `Flowrate` - Flow rate value (numeric)
- `Pressure` - Pressure value (numeric)  
- `Temperature` - Temperature value (numeric)

**Example:**
```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Reactor-001,Reactor,150.5,2.5,85.0
Distillation-01,Column,200.0,1.8,120.5
Heat-Exchanger-01,Heat Exchanger,75.2,2.5,160.0
```

---

## 📡 API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/upload/` | Upload CSV file |
| GET | `/api/summary/` | Get dataset summary |
| GET | `/api/history/` | Get upload history |
| GET | `/api/dataset/<id>/` | Get full dataset |
| GET | `/api/report/<id>/` | Download PDF report |

---

## � Why This Project Stands Out

✅ **Full-Stack Development** - Demonstrates end-to-end development skills  
✅ **Real-World Data Processing** - Handles actual CSV data pipelines  
✅ **Multi-Platform Engineering** - Both web and desktop applications  
✅ **Professional UI/UX** - Modern, responsive design  
✅ **Production Deployment** - Live application on Replit  
✅ **Comprehensive Features** - Data viz, reporting, authentication  

---

## 👩‍💻 Author

**Samiksha Wanjari**  
B.Tech Student, VIT Bhopal  
GitHub: [Sam-wan30](https://github.com/Sam-wan30)  
LinkedIn: [your-linkedin-profile]

---

## 📜 License

Created for educational and internship evaluation purposes as part of FOSSEE Internship Screening Task.

---

*This project demonstrates proficiency in full-stack development, data visualization, and multi-platform application development suitable for technical internship roles.*
