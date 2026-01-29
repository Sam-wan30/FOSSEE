🧪 Chemical Equipment Parameter Visualizer

A comprehensive web + desktop application for visualizing and analyzing chemical equipment datasets from CSV files.
Built with a modern UI, automated analytics, interactive charts, and PDF reporting.

🎯 Created as part of the FOSSEE Internship Screening Task

⸻

✨ Highlights

✔️ Upload CSV and get instant analytics
✔️ Interactive charts and tables
✔️ Auto-generated PDF reports
✔️ Works on Web and Desktop
✔️ Clean UI with professional design
✔️ Real-time statistics & history tracking

⸻

🚀 Live Demo & Source Code

� Live Web App: [Deployed Live Demo on Replit](https://your-replit-url.replit.app)
🔗 GitHub Repository: [https://github.com/Sam-wan30/FOSSEE](https://github.com/Sam-wan30/FOSSEE)
🎥 Demo Video: Coming Soon

⸻

📊 Key Features

🎨 Modern UI
	•	Chemical-themed design
	•	Glassmorphism effects
	•	Responsive layout
	•	Smooth transitions

� Data Analysis & Visualization
	•	Intelligent CSV parsing
	•	Automatic summary generation
	•	Pie Chart → Equipment distribution
	•	Bar Chart → Average parameters
	•	Sortable data tables
	•	Upload history (last 5 datasets)

📄 Reporting
	•	One-click PDF report generation
	•	Includes charts + statistics
	•	Downloadable reports

🔐 Authentication
	•	Secure login
	•	Session-based access
	•	Protected API routes

💻 Multi-Platform Support
	•	🌐 Web App (React + Django)
	•	🖥 Desktop App (PyQt5)
	•	Compatible with Windows, macOS, Linux

⸻

🛠 Tech Stack

Backend
	•	Django
	•	Django REST Framework
	•	Pandas
	•	SQLite
	•	ReportLab

Web Frontend
	•	React
	•	Chart.js
	•	Axios
	•	CSS3

Desktop App
	•	PyQt5
	•	Matplotlib

⸻

� Project Structure

FOSSEE/
│
├── backend/      → Django API
├── frontend/     → React Web App
├── desktop/      → PyQt5 Desktop App
├── sample_equipment_data.csv
├── setup.sh
├── setup.bat
└── README.md


⸻

⚡ Quick Start (3 Terminals)

Terminal 1 – Backend

cd backend
source venv/bin/activate
python manage.py migrate
python manage.py runserver

Terminal 2 – Frontend

cd frontend
npm install
npm start

Terminal 3 – Desktop App

cd desktop
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py


⸻

🌐 Access URLs

Service	URL
Web App	http://localhost:3000
Backend API	http://localhost:8000/api/
Admin Panel	http://localhost:8000/admin/
Desktop App	Opens automatically


⸻

📁 CSV Format

Required columns:
	•	Equipment Name
	•	Type
	•	Flowrate
	•	Pressure
	•	Temperature

Example:

Equipment Name,Type,Flowrate,Pressure,Temperature
Reactor-001,Reactor,150.5,2.5,85.0
Distillation-01,Column,200.0,1.8,120.5


⸻

� API Endpoints

| Method | Endpoint | Purpose |
|—––|––––|
| POST | /api/upload/ | Upload CSV |
| GET | /api/summary/ | Dataset summary |
| GET | /api/history/ | Last 5 uploads |
| GET | /api/report// | Download PDF |

⸻

🧠 Why this project stands out

✔ Demonstrates full-stack development
✔ Shows ability to handle real-world data pipelines
✔ Covers UI/UX, backend logic, visualization, and reporting
✔ Includes both web + desktop engineering
✔ Strong showcase for internships and technical roles

⸻

📜 License

Created for educational and internship evaluation purposes.

⸻

👩‍💻 Author

Samiksha Wanjari
B.Tech Student, VIT Bhopal
GitHub: [https://github.com/Sam-wan30](https://github.com/Sam-wan30)
LinkedIn: [your-linkedin]

⸻

✅ If you want, I can also help you with:

✔ Making your GitHub repo more impressive
✔ Writing a strong project description for resume
✔ Writing explanation for interview
✔ Creating a portfolio-ready project section
✔ Improving your FOSSEE submission text

Just tell me: "Make this resume-ready"
