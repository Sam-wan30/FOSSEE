import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QGridLayout, QLabel, QPushButton, QLineEdit, QGroupBox, 
                             QTableWidget, QTableWidgetItem, QHeaderView, QFileDialog, 
                             QMessageBox, QStatusBar, QScrollArea, QSizePolicy)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QPalette, QColor, QLinearGradient, QBrush
import requests
from requests.auth import HTTPBasicAuth
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import json


class APIWorker(QThread):
    """Worker thread for API calls"""
    finished = pyqtSignal(object)  # Changed to object to accept dict, list, or any JSON type
    error = pyqtSignal(str)

    def __init__(self, method, url, auth=None, files=None, data=None):
        super().__init__()
        self.method = method
        self.url = url
        self.auth = auth
        self.files = files
        self.data = data

    def run(self):
        try:
            if self.method == 'GET':
                response = requests.get(self.url, auth=self.auth, timeout=10)
            elif self.method == 'POST':
                response = requests.post(self.url, auth=self.auth, files=self.files, data=self.data, timeout=30)
            else:
                self.error.emit(f"Unsupported method: {self.method}")
                return

            if response.status_code == 200 or response.status_code == 201:
                try:
                    self.finished.emit(response.json())
                except ValueError:
                    # Response might not be JSON (e.g., empty response)
                    self.finished.emit({})
            else:
                error_msg = f"Error {response.status_code}"
                try:
                    error_data = response.json()
                    if 'error' in error_data:
                        error_msg = error_data['error']
                except:
                    error_msg = f"{error_msg}: {response.text[:200]}"
                self.error.emit(error_msg)
        except requests.exceptions.ConnectionError:
            self.error.emit("Connection Error: Cannot connect to backend. Make sure Django server is running on http://localhost:8000")
        except requests.exceptions.Timeout:
            self.error.emit("Request timeout: Server took too long to respond")
        except Exception as e:
            self.error.emit(f"Error: {str(e)}")


class ChemicalEquipmentApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.api_base_url = "http://localhost:8000/api"
        self.username = ""
        self.password = ""
        self.is_authenticated = False
        self.current_summary = None
        self.current_dataset_id = None
        self.current_data = None
        # Store worker references to prevent garbage collection
        self.active_workers = []
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Chemical Equipment Parameter Visualizer")
        self.setGeometry(50, 50, 1800, 1200)  # Increased size and position
        
        # Modern glassmorphism dark theme
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0f0f23, stop:0.5 #1a1a2e, stop:1 #16213e);
                color: #e8e8e8;
            }
            QWidget {
                background-color: transparent;
                color: #e8e8e8;
                font-family: 'Segoe UI', 'Roboto', sans-serif;
            }
            QGroupBox {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 16px;
                margin-top: 12px;
                padding-top: 20px;
                font-size: 16px;
                font-weight: 600;
                color: #ffffff;
                backdrop-filter: blur(10px);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                padding: 0 8px 0 8px;
                color: #00d4ff;
                font-weight: 700;
                font-size: 18px;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00d4ff, stop:1 #0099cc);
                border: none;
                border-radius: 12px;
                color: white;
                font-weight: 600;
                font-size: 14px;
                padding: 12px 24px;
                min-height: 45px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00e5ff, stop:1 #00b3e6);
                transform: translateY(-2px);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0099cc, stop:1 #007399);
            }
            QPushButton:disabled {
                background: rgba(255, 255, 255, 0.1);
                color: rgba(255, 255, 255, 0.3);
            }
            QLineEdit {
                background: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 12px;
                padding: 12px 16px;
                color: #ffffff;
                font-size: 14px;
                selection-background-color: #00d4ff;
            }
            QLineEdit:focus {
                border: 2px solid #00d4ff;
                background: rgba(255, 255, 255, 0.12);
            }
            QTableWidget {
                background: rgba(255, 255, 255, 0.03);
                alternate-background-color: rgba(255, 255, 255, 0.06);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                color: #ffffff;
                selection-background-color: #00d4ff;
                gridline-color: rgba(255, 255, 255, 0.05);
            }
            QTableWidget::item {
                padding: 12px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            }
            QTableWidget::item:selected {
                background-color: rgba(0, 212, 255, 0.3);
            }
            QHeaderView::section {
                background: rgba(0, 212, 255, 0.15);
                color: #ffffff;
                padding: 12px;
                font-weight: 600;
                border: none;
                border-bottom: 2px solid #00d4ff;
            }
            QLabel {
                color: #e8e8e8;
                font-size: 14px;
            }
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background: rgba(255, 255, 255, 0.05);
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: rgba(0, 212, 255, 0.5);
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(0, 212, 255, 0.8);
            }
        """)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Modern header with gradient
        header_widget = QWidget()
        header_widget.setMinimumHeight(140)
        header_widget.setMaximumHeight(160)
        header_layout = QVBoxLayout()
        header_widget.setLayout(header_layout)
        header_widget.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(0, 212, 255, 0.1), stop:0.5 rgba(0, 212, 255, 0.05), stop:1 rgba(0, 212, 255, 0.1));
                border-radius: 16px;
                margin: 5px;
            }
        """)
        
        title = QLabel("Chemical Equipment Parameter Visualizer")
        title.setFont(QFont("Segoe UI", 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00d4ff, stop:0.5 #00ff88, stop:1 #00d4ff);
                background: transparent;
                padding: 10px;
            }
        """)
        
        subtitle = QLabel("Advanced Analytics & Real-time Monitoring Dashboard")
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.7);
                background: transparent;
                padding: 5px;
            }
        """)
        
        header_layout.addWidget(title)
        header_layout.addWidget(subtitle)
        main_layout.addWidget(header_widget)

        # Main content area with glassmorphism and scroll
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #0f0f23, stop:0.5 #1a1a2e, stop:1 #16213e);
            }
            QScrollBar:vertical {
                background: rgba(255, 255, 255, 0.05);
                width: 8px;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: rgba(0, 212, 255, 0.5);
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgba(0, 212, 255, 0.8);
            }
        """)
        
        content_widget = QWidget()
        content_widget.setStyleSheet("""
            QWidget {
                background: transparent;
            }
        """)
        content_layout = QVBoxLayout()
        content_layout.setSpacing(20)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_widget.setLayout(content_layout)
        
        # Create grid layout for cards
        cards_grid = QGridLayout()
        cards_grid.setSpacing(20)
        
        # Authentication card
        self.auth_group = QGroupBox("🔐 Secure Access")
        self.auth_group.setStyleSheet("""
            QGroupBox {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 16px;
                margin-top: 12px;
                padding-top: 20px;
                font-size: 16px;
                font-weight: 600;
                color: #ffffff;
                backdrop-filter: blur(10px);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                padding: 0 8px 0 8px;
                color: #00d4ff;
                font-weight: 700;
                font-size: 18px;
            }
        """)
        auth_layout = QGridLayout()
        auth_layout.setSpacing(15)
        auth_layout.setContentsMargins(20, 20, 20, 20)
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.handle_login)
        self.logout_button = QPushButton("Logout")
        self.logout_button.clicked.connect(self.handle_logout)
        self.logout_button.setEnabled(False)
        
        auth_layout.addWidget(QLabel("Username:"), 0, 0)
        auth_layout.addWidget(self.username_input, 0, 1)
        auth_layout.addWidget(QLabel("Password:"), 1, 0)
        auth_layout.addWidget(self.password_input, 1, 1)
        auth_layout.addWidget(self.login_button, 2, 0)
        auth_layout.addWidget(self.logout_button, 2, 1)
        
        self.auth_group.setLayout(auth_layout)
        
        # Upload card
        self.upload_group = QGroupBox("📁 Data Import")
        self.upload_group.setStyleSheet("""
            QGroupBox {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 16px;
                margin-top: 12px;
                padding-top: 20px;
                font-size: 16px;
                font-weight: 600;
                color: #ffffff;
                backdrop-filter: blur(10px);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                padding: 0 8px 0 8px;
                color: #00d4ff;
                font-weight: 700;
                font-size: 18px;
            }
        """)
        upload_layout = QVBoxLayout()
        upload_layout.setSpacing(15)
        upload_layout.setContentsMargins(20, 20, 20, 20)
        
        self.file_label = QLabel("No file selected")
        self.browse_button = QPushButton("Browse CSV File")
        self.browse_button.clicked.connect(self.browse_file)
        self.upload_button = QPushButton("Upload File")
        self.upload_button.clicked.connect(self.upload_file)
        self.upload_button.setEnabled(False)
        
        upload_layout.addWidget(self.file_label)
        upload_layout.addWidget(self.browse_button)
        upload_layout.addWidget(self.upload_button)
        
        self.upload_group.setLayout(upload_layout)
        self.upload_group.setEnabled(False)
        
        # Summary statistics cards
        self.summary_group = QGroupBox("📊 Analytics Overview")
        self.summary_group.setMinimumHeight(200)
        self.summary_group.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.summary_group.setStyleSheet("""
            QGroupBox {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 16px;
                margin-top: 12px;
                padding-top: 20px;
                font-size: 16px;
                font-weight: 600;
                color: #ffffff;
                backdrop-filter: blur(10px);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                padding: 0 8px 0 8px;
                color: #00d4ff;
                font-weight: 700;
                font-size: 18px;
            }
        """)
        
        summary_layout = QGridLayout()
        summary_layout.setSpacing(20)
        summary_layout.setContentsMargins(20, 30, 20, 20)
        
        # Create individual stat cards for summary
        self.total_count_widget, self.total_count_label = self.create_stat_card("📊 Total Count", "0", "units")
        self.avg_flowrate_widget, self.avg_flowrate_label = self.create_stat_card("💧 Avg Flowrate", "0", "L/min")
        self.avg_pressure_widget, self.avg_pressure_label = self.create_stat_card("🔧 Avg Pressure", "0", "bar")
        self.avg_temperature_widget, self.avg_temperature_label = self.create_stat_card("🌡️ Avg Temperature", "0", "°C")
        
        # Add widgets to layout
        summary_layout.addWidget(self.total_count_widget, 0, 0)
        summary_layout.addWidget(self.avg_flowrate_widget, 0, 1)
        summary_layout.addWidget(self.avg_pressure_widget, 1, 0)
        summary_layout.addWidget(self.avg_temperature_widget, 1, 1)
        
        # CRITICAL: Set the layout on the group box
        self.summary_group.setLayout(summary_layout)
        self.summary_group.setEnabled(False)
        self.summary_group.setVisible(True)
        
        # Data visualization card
        charts_container = QGroupBox("📈 Data Visualization")
        charts_container.setMinimumHeight(300)
        charts_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        charts_container.setStyleSheet("""
            QGroupBox {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 16px;
                margin-top: 12px;
                padding-top: 20px;
                font-size: 16px;
                font-weight: 600;
                color: #ffffff;
                backdrop-filter: blur(10px);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                padding: 0 8px 0 8px;
                color: #00d4ff;
                font-weight: 700;
                font-size: 18px;
            }
        """)
        
        charts_layout = QHBoxLayout()
        charts_layout.setSpacing(40)
        charts_layout.setContentsMargins(20, 20, 20, 20)
        charts_layout.setAlignment(Qt.AlignCenter)
        
        # Create separate containers for each chart
        pie_container = QWidget()
        pie_container.setMinimumHeight(250)
        pie_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        pie_container.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.03);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                padding: 15px;
            }
        """)
        pie_layout = QVBoxLayout()
        pie_layout.setAlignment(Qt.AlignCenter)
        pie_container.setLayout(pie_layout)
        
        # Pie chart for equipment type distribution
        self.pie_figure = Figure(figsize=(5, 4), dpi=100)
        self.pie_canvas = FigureCanvas(self.pie_figure)
        self.pie_canvas.setMinimumSize(400, 200)
        self.pie_canvas.setMaximumSize(450, 300)
        pie_layout.addWidget(self.pie_canvas)
        
        # Bar chart container
        bar_container = QWidget()
        bar_container.setMinimumHeight(250)
        bar_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        bar_container.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.03);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                padding: 15px;
            }
        """)
        bar_layout = QVBoxLayout()
        bar_layout.setAlignment(Qt.AlignCenter)
        bar_container.setLayout(bar_layout)
        
        # Bar chart for parameters
        self.bar_figure = Figure(figsize=(6, 4), dpi=100)
        self.bar_canvas = FigureCanvas(self.bar_figure)
        self.bar_canvas.setMinimumSize(400, 200)
        self.bar_canvas.setMaximumSize(550, 300)
        bar_layout.addWidget(self.bar_canvas)
        
        # CRITICAL: Add containers to charts layout
        charts_layout.addWidget(pie_container)
        charts_layout.addWidget(bar_container)
        
        # CRITICAL: Set the layout on the charts container
        charts_container.setLayout(charts_layout)
        self.charts_container = charts_container
        self.charts_container.setEnabled(True)
        self.charts_container.setVisible(True)
        
        # Data table card
        table_container = QGroupBox("📋 Equipment Database")
        table_container.setMinimumHeight(250)  # Force minimum height
        table_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Force vertical expansion
        table_container.setStyleSheet("""
            QGroupBox {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 16px;
                margin-top: 12px;
                padding-top: 20px;
                font-size: 16px;
                font-weight: 600;
                color: #ffffff;
                backdrop-filter: blur(10px);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                padding: 0 8px 0 8px;
                color: #00d4ff;
                font-weight: 700;
                font-size: 18px;
            }
        """)
        table_layout = QVBoxLayout()
        table_layout.setContentsMargins(20, 20, 20, 20)
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            "Equipment Name", "Type", "Flowrate", "Pressure", "Temperature"
        ])
        # Ensure headers are visible
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(True)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # Style headers to be more visible
        self.table.horizontalHeader().setStyleSheet("""
            QHeaderView::section {
                background-color: rgba(0, 212, 255, 0.2);
                color: #ffffff;
                padding: 12px;
                font-weight: 700;
                font-size: 14px;
                border: none;
                border-bottom: 2px solid #00d4ff;
                text-align: center;
            }
        """)
        self.table.setEnabled(False)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSortingEnabled(True)
        self.table.setMinimumHeight(200)
        
        table_layout.addWidget(self.table)
        table_container.setLayout(table_layout)
        self.table_container = table_container
        
        # Action buttons card
        buttons_container = QGroupBox("⚙️ Control Panel")
        buttons_container.setStyleSheet("""
            QGroupBox {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 16px;
                margin-top: 12px;
                padding-top: 20px;
                font-size: 16px;
                font-weight: 600;
                color: #ffffff;
                backdrop-filter: blur(10px);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                padding: 0 8px 0 8px;
                color: #00d4ff;
                font-weight: 700;
                font-size: 18px;
            }
        """)
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)
        buttons_layout.setContentsMargins(20, 20, 20, 20)
        
        # Create buttons with icons and better styling
        self.load_data_button = self.create_styled_button("📊 Load Full Data Table")
        self.load_data_button.clicked.connect(self.load_dataset_data)
        self.load_data_button.setEnabled(False)
        
        self.download_pdf_button = self.create_styled_button("📄 Download PDF Report")
        self.download_pdf_button.clicked.connect(self.download_pdf)
        self.download_pdf_button.setEnabled(False)
        
        self.load_history_button = self.create_styled_button("📜 Load History")
        self.load_history_button.clicked.connect(self.load_history)
        self.load_history_button.setEnabled(False)
        
        self.refresh_summary_button = self.create_styled_button("🔄 Refresh Summary")
        self.refresh_summary_button.clicked.connect(self.manual_refresh_summary)
        self.refresh_summary_button.setEnabled(False)
        
        # Add a test charts button for debugging
        self.test_charts_button = self.create_styled_button("🧪 Test Charts")
        self.test_charts_button.clicked.connect(self.test_charts_directly)
        self.test_charts_button.setEnabled(True)  # Always enabled for testing
        
        buttons_layout.addWidget(self.load_data_button)
        buttons_layout.addWidget(self.download_pdf_button)
        buttons_layout.addWidget(self.load_history_button)
        buttons_layout.addWidget(self.refresh_summary_button)
        buttons_layout.addWidget(self.test_charts_button)
        
        buttons_container.setLayout(buttons_layout)
        
        # Add all cards to grid layout
        cards_grid.addWidget(self.auth_group, 0, 0, 1, 1)
        cards_grid.addWidget(self.upload_group, 0, 1, 1, 1)
        cards_grid.addWidget(self.summary_group, 1, 0, 1, 2)
        cards_grid.addWidget(charts_container, 2, 0, 1, 2)
        cards_grid.addWidget(table_container, 3, 0, 1, 2)
        cards_grid.addWidget(buttons_container, 4, 0, 1, 2)
        
        # Set row stretches to ensure proper space allocation
        cards_grid.setRowStretch(0, 0)  # Auth/Upload - no stretch
        cards_grid.setRowStretch(1, 1)  # Summary - stretch
        cards_grid.setRowStretch(2, 1)  # Charts - stretch
        cards_grid.setRowStretch(3, 2)  # Table - more stretch
        cards_grid.setRowStretch(4, 0)  # Buttons - no stretch
        
        content_layout.addLayout(cards_grid)
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)
        
        # Modern status bar
        self.statusBar().setStyleSheet("""
            QStatusBar {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(0, 212, 255, 0.1), stop:0.5 rgba(0, 212, 255, 0.05), stop:1 rgba(0, 212, 255, 0.1));
                color: #ffffff;
                border-top: 2px solid #00d4ff;
                padding: 8px;
                font-weight: 500;
            }
        """)
        self.statusBar().showMessage("🚀 System Ready - Awaiting Authentication")

        self.selected_file_path = None
        
        # Initialize charts with test data to ensure they're visible
        self.initialize_charts()
    
    def initialize_charts(self):
        """Initialize charts with simple test data to ensure they're visible"""
        try:
            print("Initializing charts with test data...")
            
            # Simple pie chart
            self.pie_figure.clear()
            ax1 = self.pie_figure.add_subplot(111)
            ax1.pie([30, 25, 20, 15, 10], 
                   labels=['A', 'B', 'C', 'D', 'E'], 
                   colors=['red', 'green', 'blue', 'yellow', 'purple'],
                   autopct='%1.0f%%')
            ax1.set_title('Test Chart')
            self.pie_canvas.draw()
            self.pie_canvas.update()
            print("Pie chart initialized")
            
            # Simple bar chart
            self.bar_figure.clear()
            ax2 = self.bar_figure.add_subplot(111)
            ax2.bar(['X', 'Y', 'Z'], [10, 20, 15], color=['red', 'green', 'blue'])
            ax2.set_title('Test Bar')
            self.bar_canvas.draw()
            self.bar_canvas.update()
            print("Bar chart initialized")
            
        except Exception as e:
            print(f"Chart initialization failed: {e}")
            import traceback
            traceback.print_exc()
    
    def create_stat_card(self, title, value, unit):
        """Create a modern stat card widget and return both card and value label"""
        card = QWidget()
        card.setFixedHeight(120)
        card.setMinimumSize(200, 120)
        card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        card.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(0, 212, 255, 0.1), stop:1 rgba(0, 255, 136, 0.1));
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 12px;
                padding: 15px;
            }
        """)
        
        layout = QVBoxLayout()
        card.setLayout(layout)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        title_label.setStyleSheet("""
            color: #ffffff;
            background: transparent;
            padding: 2px;
        """)
        
        value_label = QLabel(str(value))
        value_label.setFont(QFont("Segoe UI", 24, QFont.Bold))
        value_label.setStyleSheet("""
            color: #00d4ff;
            background: transparent;
            padding: 2px;
        """)
        
        unit_label = QLabel(unit)
        unit_label.setFont(QFont("Segoe UI", 10))
        unit_label.setStyleSheet("""
            color: rgba(255, 255, 255, 0.8);
            background: transparent;
            padding: 2px;
        """)
        unit_label.setAlignment(Qt.AlignRight)
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addWidget(unit_label)
        
        return card, value_label
    
    def create_styled_button(self, text):
        """Create a button with enhanced styling"""
        button = QPushButton(text)
        button.setMinimumHeight(45)
        button.setFont(QFont("Segoe UI", 11, QFont.Bold))
        return button

    def handle_login(self):
        self.username = self.username_input.text()
        self.password = self.password_input.text()
        
        if not self.username or not self.password:
            QMessageBox.warning(self, "Error", "Please enter username and password")
            return
        
        # Test authentication using history endpoint (works even when no data exists)
        worker = APIWorker('GET', f"{self.api_base_url}/history/",
                          auth=HTTPBasicAuth(self.username, self.password))
        worker.finished.connect(self.on_login_success)
        worker.error.connect(self.on_login_error)
        worker.finished.connect(lambda: self.remove_worker(worker))
        worker.error.connect(lambda: self.remove_worker(worker))
        self.active_workers.append(worker)
        worker.start()
        
        self.statusBar().showMessage("🔒 Authenticating...")

    def remove_worker(self, worker):
        """Remove worker from active list and clean up"""
        if worker in self.active_workers:
            self.active_workers.remove(worker)
        if worker.isRunning():
            worker.quit()
            worker.wait(1000)  # Wait up to 1 second
        worker.deleteLater()

    def on_login_success(self, data):
        try:
            # Handle both list and dict responses
            # History endpoint returns a list, but we just need to verify auth worked
            self.is_authenticated = True
            self.upload_group.setEnabled(True)
            self.summary_group.setEnabled(True)
            self.table.setEnabled(True)
            self.login_button.setEnabled(False)
            self.logout_button.setEnabled(True)
            self.username_input.setEnabled(False)
            self.password_input.setEnabled(False)
            self.load_history_button.setEnabled(True)
            
            self.statusBar().showMessage("✅ Login successful!")
            QMessageBox.information(self, "Success", "Login successful!")
            
            # Load initial summary (only if data exists)
            # Don't load summary immediately - let user upload data first
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error during login: {str(e)}")
            import traceback
            traceback.print_exc()

    def on_login_error(self, error):
        try:
            self.statusBar().showMessage("🚫 Login failed")
            error_str = str(error)
            if "401" in error_str or "Unauthorized" in error_str:
                QMessageBox.critical(self, "Login Failed", "Invalid credentials. Please check your username and password.")
            elif "Connection" in error_str or "refused" in error_str.lower():
                QMessageBox.critical(self, "Connection Error", "Cannot connect to backend. Make sure the Django server is running on http://localhost:8000")
            else:
                QMessageBox.critical(self, "Login Failed", f"Authentication failed: {error_str}")
        except Exception as e:
            print(f"Error in on_login_error: {e}")
            import traceback
            traceback.print_exc()

    def handle_logout(self):
        self.is_authenticated = False
        self.username = ""
        self.password = ""
        self.upload_group.setEnabled(False)
        self.summary_group.setEnabled(False)
        self.table.setEnabled(False)
        self.login_button.setEnabled(True)
        self.logout_button.setEnabled(False)
        self.username_input.setEnabled(True)
        self.password_input.setEnabled(True)
        self.load_data_button.setEnabled(False)
        self.download_pdf_button.setEnabled(False)
        self.load_history_button.setEnabled(False)
        self.refresh_summary_button.setEnabled(False)
        self.username_input.clear()
        self.password_input.clear()
        self.statusBar().showMessage("🚪 Logged out")

    def browse_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV File", "", "CSV Files (*.csv)"
        )
        if file_path:
            self.selected_file_path = file_path
            self.file_label.setText(f"Selected: {os.path.basename(file_path)}")
            self.upload_button.setEnabled(True)

    def upload_file(self):
        if not self.selected_file_path:
            QMessageBox.warning(self, "Error", "Please select a file first")
            return
        
        self.statusBar().showMessage("📤 Uploading file...")
        self.upload_button.setEnabled(False)
        
        # Read file content into memory before passing to worker thread
        try:
            with open(self.selected_file_path, 'rb') as f:
                file_content = f.read()
                files = {'file': (os.path.basename(self.selected_file_path), file_content, 'text/csv')}
                worker = APIWorker(
                    'POST',
                    f"{self.api_base_url}/upload/",
                    auth=HTTPBasicAuth(self.username, self.password),
                    files=files
                )
                worker.finished.connect(self.on_upload_success)
                worker.error.connect(self.on_upload_error)
                worker.finished.connect(lambda: self.remove_worker(worker))
                worker.error.connect(lambda: self.remove_worker(worker))
                self.active_workers.append(worker)
                worker.start()
        except Exception as e:
            self.statusBar().showMessage("🚫 Upload failed")
            QMessageBox.critical(self, "Upload Failed", f"Failed to read file: {str(e)}")
            self.upload_button.setEnabled(True)

    def on_upload_success(self, data):
        try:
            self.statusBar().showMessage("✅ File uploaded successfully!")
            QMessageBox.information(self, "Success", "File uploaded successfully!")
            
            # Debug: Print the response structure
            print(f"Upload response type: {type(data)}")
            print(f"Upload response: {data}")
            
            # Handle response structure - upload returns {'summary': {...}, 'dataset': {...}}
            if isinstance(data, dict):
                self.current_summary = data.get('summary')
                dataset_info = data.get('dataset', {})
                if isinstance(dataset_info, dict):
                    self.current_dataset_id = dataset_info.get('id')
                    print(f"Dataset ID from dict: {self.current_dataset_id}")
                elif isinstance(dataset_info, (int, str)):
                    self.current_dataset_id = int(dataset_info) if str(dataset_info).isdigit() else None
                    print(f"Dataset ID from value: {self.current_dataset_id}")
                else:
                    self.current_dataset_id = None
            else:
                # Fallback - try to extract from response
                print(f"Unexpected data type: {type(data)}")
                print(f"Data content: {data}")
                self.current_dataset_id = None
            
            # If we don't have dataset_id, try to get it from the latest dataset
            if not self.current_dataset_id:
                print("No dataset ID found, loading from latest dataset...")
                # Load summary which will get the latest dataset
                self.load_summary()
            
            # Update display if we have summary data
            if self.current_summary:
                print(f"Updating display with summary: {self.current_summary}")
                self.update_summary_display()
                self.update_charts()
                # Enable all sections after successful upload
                self.summary_group.setEnabled(True)
                self.charts_container.setEnabled(True)
                self.table_container.setEnabled(True)
            else:
                # If no summary in response, load it separately
                print("No summary in response, loading separately...")
                if self.current_dataset_id:
                    print(f"Loading summary for dataset ID: {self.current_dataset_id}")
                    self.load_summary(self.current_dataset_id)
                else:
                    print("Loading latest summary...")
                    self.load_summary()  # Load latest
            
            # Enable buttons - enable even if dataset_id is None, user can refresh
            self.load_data_button.setEnabled(True)
            self.download_pdf_button.setEnabled(True)
            self.refresh_summary_button.setEnabled(True)
            self.upload_button.setEnabled(True)
            
            print(f"Current dataset ID: {self.current_dataset_id}")
            print(f"Current summary: {self.current_summary is not None}")
        except Exception as e:
            print(f"Error in on_upload_success: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.warning(self, "Warning", f"Upload succeeded but error displaying data: {str(e)}")
            # Still enable buttons even on error
            self.load_data_button.setEnabled(True)
            self.refresh_summary_button.setEnabled(True)

    def on_upload_error(self, error):
        self.statusBar().showMessage("🚫 Upload failed")
        QMessageBox.critical(self, "Upload Failed", f"Upload failed: {error}")
        self.upload_button.setEnabled(True)

    def manual_refresh_summary(self):
        """Manually refresh summary with debugging"""
        print("Manual refresh summary triggered")
        self.statusBar().showMessage("🔄 Refreshing summary...")
        
        # Enable the summary group to make it visible
        self.summary_group.setEnabled(True)
        self.summary_group.setVisible(True)
        
        # Test stat cards with dummy data first
        print("Testing stat cards with dummy data...")
        self.total_count_label.setText("25")
        self.avg_flowrate_label.setText("219.06")
        self.avg_pressure_label.setText("4.26")
        self.avg_temperature_label.setText("79.74")
        
        # Force the summary group to update
        self.summary_group.update()
        self.summary_group.repaint()
        
        # Test charts with dummy data
        print("Testing charts with dummy data...")
        dummy_summary = {
            'total_count': 25,
            'avg_flowrate': 219.06,
            'avg_pressure': 4.26,
            'avg_temperature': 79.74,
            'equipment_type_distribution': {
                'Reactor': 8,
                'Pump': 6,
                'Compressor': 5,
                'Heat Exchanger': 4,
                'Valve': 2
            }
        }
        self.current_summary = dummy_summary
        
        # Enable the charts section first
        self.charts_container.setEnabled(True)
        self.charts_container.setVisible(True)
        
        # Try to update charts
        try:
            self.update_charts()
            print("Charts update completed")
        except Exception as e:
            print(f"Error updating charts: {e}")
            # Try a simple direct approach
            self.test_charts_directly()
        
        # Now load real data
        if self.current_dataset_id:
            print(f"Loading summary for dataset ID: {self.current_dataset_id}")
            self.load_summary(self.current_dataset_id)
        else:
            print("Loading latest summary...")
            self.load_summary()
    
    def test_charts_directly(self):
        """Direct test of chart functionality - most basic approach"""
        try:
            print("Testing charts directly...")
            
            # Most basic pie chart
            self.pie_figure.clear()
            ax1 = self.pie_figure.add_subplot(111)
            ax1.pie([1, 2, 3], labels=['A', 'B', 'C'])
            self.pie_canvas.draw()
            print("Basic pie chart test completed")
            
            # Most basic bar chart
            self.bar_figure.clear()
            ax2 = self.bar_figure.add_subplot(111)
            ax2.bar([1, 2, 3], [4, 5, 6])
            self.bar_canvas.draw()
            print("Basic bar chart test completed")
            
        except Exception as e:
            print(f"Direct chart test failed: {e}")
            import traceback
            traceback.print_exc()
    
    def load_summary(self, dataset_id=None):
        try:
            url = f"{self.api_base_url}/summary/"
            if dataset_id:
                url = f"{self.api_base_url}/summary/{dataset_id}/"
            
            worker = APIWorker('GET', url, auth=HTTPBasicAuth(self.username, self.password))
            worker.finished.connect(self.on_summary_loaded)
            worker.error.connect(self.on_summary_error)
            worker.finished.connect(lambda: self.remove_worker(worker))
            worker.error.connect(lambda: self.remove_worker(worker))
            self.active_workers.append(worker)
            worker.start()
        except Exception as e:
            print(f"Error in load_summary: {e}")
            import traceback
            traceback.print_exc()
    
    def on_summary_error(self, error):
        """Handle summary loading errors gracefully"""
        error_str = str(error)
        if "404" in error_str or "No datasets available" in error_str:
            # This is okay - user just needs to upload data first
            self.statusBar().showMessage("📊 No data available. Please upload a CSV file.")
        else:
            self.statusBar().showMessage(f"🚫 Error loading summary: {error_str}")

    def on_summary_loaded(self, data):
        try:
            print(f"Summary loaded successfully: {data}")
            self.current_summary = data
            print(f"Current summary set: {self.current_summary}")
            
            # Update displays
            self.update_summary_display()
            self.update_charts()
            
            # Enable sections
            self.summary_group.setEnabled(True)
            self.charts_container.setEnabled(True)
            
            print("Summary display and charts updated")
        except Exception as e:
            print(f"Error in on_summary_loaded: {e}")
            import traceback
            traceback.print_exc()
            QMessageBox.warning(self, "Warning", f"Error displaying summary: {str(e)}")

    def update_summary_display(self):
        """Update the summary display with current data"""
        try:
            print(f"Updating summary display with data: {self.current_summary}")
            
            if not self.current_summary:
                print("No current summary data available")
                return
            
            # Extract values from summary data
            total_count = self.current_summary.get('total_count', 0)
            avg_flowrate = self.current_summary.get('avg_flowrate', 0)
            avg_pressure = self.current_summary.get('avg_pressure', 0)
            avg_temperature = self.current_summary.get('avg_temperature', 0)
            
            print(f"Values - Count: {total_count}, Flowrate: {avg_flowrate}, Pressure: {avg_pressure}, Temp: {avg_temperature}")
            
            # Direct update using instance variables
            self.total_count_label.setText(str(total_count))
            self.avg_flowrate_label.setText(f"{avg_flowrate:.2f}")
            self.avg_pressure_label.setText(f"{avg_pressure:.2f}")
            self.avg_temperature_label.setText(f"{avg_temperature:.2f}")
            
            print("Direct label updates completed successfully")
            
        except Exception as e:
            print(f"Error updating summary display: {e}")
            import traceback
            traceback.print_exc()

    def update_stat_card(self, card_widget, title, value, unit):
        """Update the values in a stat card"""
        try:
            print(f"Updating stat card with value: {value}")
            
            # Direct approach: use the stored reference to value label
            if hasattr(card_widget, 'value_label'):
                print("Using direct value label reference")
                card_widget.value_label.setText(str(value))
                card_widget.value_label.setStyleSheet("""
                    color: #00d4ff; 
                    font-size: 24px; 
                    font-weight: bold;
                    background: transparent; 
                    padding: 2px;
                """)
                card_widget.value_label.update()
                card_widget.value_label.repaint()
                print(f"Direct update successful: {value}")
                return
            
            # Fallback: find by object name
            layout = card_widget.layout()
            if layout:
                print(f"Layout has {layout.count()} items")
                for i in range(layout.count()):
                    widget = layout.itemAt(i).widget()
                    if isinstance(widget, QLabel) and widget.objectName() == "value_label":
                        print(f"Found value label by object name, setting to: {value}")
                        widget.setText(str(value))
                        widget.setStyleSheet("""
                            color: #00d4ff; 
                            font-size: 24px; 
                            font-weight: bold;
                            background: transparent; 
                            padding: 2px;
                        """)
                        widget.update()
                        widget.repaint()
                        print(f"Object name update successful: {value}")
                        return
                
                # Final fallback: update by position
                print("No object name found - trying position fallback")
                if layout.count() >= 2:
                    widget = layout.itemAt(1).widget()
                    if isinstance(widget, QLabel):
                        print(f"Fallback: updating label at position 1 to: {value}")
                        widget.setText(str(value))
                        widget.setStyleSheet("""
                            color: #00d4ff; 
                            font-size: 24px; 
                            font-weight: bold;
                            background: transparent; 
                            padding: 2px;
                        """)
                        widget.update()
                        widget.repaint()
                        print(f"Position fallback successful: {value}")
                        return
                else:
                    print("Not enough labels in stat card for fallback")
            else:
                print("No layout found in stat card")
                
        except Exception as e:
            print(f"Error updating stat card: {e}")
            import traceback
            traceback.print_exc()

    def update_charts(self):
        if not self.current_summary:
            print("No current summary available for charts")
            return
        
        try:
            print(f"Updating charts with summary: {self.current_summary}")
            
            # Simple pie chart
            self.pie_figure.clear()
            ax1 = self.pie_figure.add_subplot(111)
            
            type_dist = self.current_summary.get('equipment_type_distribution', {})
            print(f"Equipment type distribution: {type_dist}")
            
            if type_dist and isinstance(type_dist, dict) and len(type_dist) > 0:
                labels = list(type_dist.keys())
                sizes = list(type_dist.values())
                ax1.pie(sizes, labels=labels, autopct='%1.1f%%')
                ax1.set_title('Equipment Types')
            else:
                ax1.text(0.5, 0.5, 'No Data', ha='center', va='center')
                ax1.set_title('Equipment Types')
            
            self.pie_canvas.draw()
            print("Pie chart updated")
            
            # Simple bar chart
            self.bar_figure.clear()
            ax2 = self.bar_figure.add_subplot(111)
            
            values = [
                self.current_summary.get('avg_flowrate', 0),
                self.current_summary.get('avg_pressure', 0),
                self.current_summary.get('avg_temperature', 0)
            ]
            print(f"Parameter values: {values}")
            
            if any(v > 0 for v in values):
                params = ['Flow', 'Pressure', 'Temp']
                ax2.bar(params, values)
                ax2.set_title('Parameters')
            else:
                ax2.text(0.5, 0.5, 'No Data', ha='center', va='center')
                ax2.set_title('Parameters')
            
            self.bar_canvas.draw()
            print("Bar chart updated")
            
        except Exception as e:
            print(f"Error updating charts: {e}")
            import traceback
            traceback.print_exc()

    def load_dataset_data(self):
        # If no dataset_id, try to get it from the latest dataset
        if not self.current_dataset_id:
            # First get the latest dataset ID from history
            self.statusBar().showMessage("🕰️ Getting latest dataset...")
            worker = APIWorker(
                'GET',
                f"{self.api_base_url}/history/",
                auth=HTTPBasicAuth(self.username, self.password)
            )
            worker.finished.connect(self.on_history_for_dataset_id)
            worker.error.connect(lambda e: QMessageBox.critical(self, "Error", f"Failed to get dataset: {e}"))
            worker.finished.connect(lambda: self.remove_worker(worker))
            worker.error.connect(lambda: self.remove_worker(worker))
            self.active_workers.append(worker)
            worker.start()
            return
        
        self.statusBar().showMessage("📊 Loading dataset data...")
        
        worker = APIWorker(
            'GET',
            f"{self.api_base_url}/dataset/{self.current_dataset_id}/",
            auth=HTTPBasicAuth(self.username, self.password)
        )
        worker.finished.connect(self.on_data_loaded)
        worker.error.connect(lambda e: QMessageBox.critical(self, "Error", f"Failed to load data: {e}"))
        worker.finished.connect(lambda: self.remove_worker(worker))
        worker.error.connect(lambda: self.remove_worker(worker))
        self.active_workers.append(worker)
        worker.start()
    
    def on_history_for_dataset_id(self, data):
        """Get dataset ID from history and then load data"""
        if isinstance(data, list) and len(data) > 0:
            self.current_dataset_id = data[0].get('id')
            print(f"Got dataset ID from history: {self.current_dataset_id}")
            # Now load the data
            self.load_dataset_data()  # Recursive call, but now with dataset_id
        else:
            QMessageBox.warning(self, "Error", "No datasets available. Please upload a CSV file first.")

    def on_data_loaded(self, data):
        self.current_data = data.get('data', [])
        
        if not self.current_data:
            QMessageBox.warning(self, "Warning", "No data available")
            return
        
        self.table.setRowCount(len(self.current_data))
        
        for row_idx, row_data in enumerate(self.current_data):
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(row_data.get('Equipment Name', ''))))
            self.table.setItem(row_idx, 1, QTableWidgetItem(str(row_data.get('Type', ''))))
            self.table.setItem(row_idx, 2, QTableWidgetItem(str(row_data.get('Flowrate', ''))))
            self.table.setItem(row_idx, 3, QTableWidgetItem(str(row_data.get('Pressure', ''))))
            self.table.setItem(row_idx, 4, QTableWidgetItem(str(row_data.get('Temperature', ''))))
        
        # Ensure headers are visible and properly styled
        self.table.horizontalHeader().setVisible(True)
        self.table.verticalHeader().setVisible(False)
        
        # Resize columns to fit content
        self.table.resizeColumnsToContents()
        # Ensure minimum column width
        for col in range(5):
            if self.table.columnWidth(col) < 120:
                self.table.setColumnWidth(col, 120)
        
        # Force header update
        self.table.horizontalHeader().update()
        
        self.statusBar().showMessage(f"📊 Loaded {len(self.current_data)} records")

    def download_pdf(self):
        if not self.current_dataset_id:
            QMessageBox.warning(self, "Error", "No dataset selected")
            return
        
        self.statusBar().showMessage("📄 Generating PDF report...")
        
        try:
            response = requests.get(
                f"{self.api_base_url}/report/{self.current_dataset_id}/",
                auth=HTTPBasicAuth(self.username, self.password),
                stream=True
            )
            
            if response.status_code == 200:
                save_path, _ = QFileDialog.getSaveFileName(
                    self, "Save PDF Report", f"equipment_report_{self.current_dataset_id}.pdf",
                    "PDF Files (*.pdf)"
                )
                
                if save_path:
                    with open(save_path, 'wb') as f:
                        f.write(response.content)
                    QMessageBox.information(self, "Success", f"PDF report saved to {save_path}")
                    self.statusBar().showMessage("✅ PDF report generated successfully")
            else:
                QMessageBox.critical(self, "Error", f"Failed to generate PDF: {response.text}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to download PDF: {str(e)}")

    def load_history(self):
        self.statusBar().showMessage("📜 Loading history...")
        
        worker = APIWorker(
            'GET',
            f"{self.api_base_url}/history/",
            auth=HTTPBasicAuth(self.username, self.password)
        )
        worker.finished.connect(self.on_history_loaded)
        worker.error.connect(lambda e: QMessageBox.critical(self, "Error", f"Failed to load history: {e}"))
        worker.finished.connect(lambda: self.remove_worker(worker))
        worker.error.connect(lambda: self.remove_worker(worker))
        self.active_workers.append(worker)
        worker.start()

    def on_history_loaded(self, data):
        if not data:
            QMessageBox.information(self, "Info", "No history available")
            return
        
        history_text = "Upload History (Last 5):\n\n"
        for dataset in data:
            history_text += f"ID: {dataset['id']} - {dataset['name']}\n"
            history_text += f"  Uploaded: {dataset['uploaded_at']}\n"
            history_text += f"  Count: {dataset['total_count']}\n"
            history_text += f"  Avg Flowrate: {dataset['avg_flowrate']:.2f}\n"
            history_text += f"  Avg Pressure: {dataset['avg_pressure']:.2f}\n"
            history_text += f"  Avg Temperature: {dataset['avg_temperature']:.2f}\n\n"
        
        msg = QMessageBox(self)
        msg.setWindowTitle("Upload History")
        msg.setText(history_text)
        msg.exec_()
        
        self.statusBar().showMessage("📊 History loaded")
    
    def closeEvent(self, event):
        """Handle application close - wait for all threads to finish"""
        # Wait for all active workers to finish
        for worker in self.active_workers[:]:  # Copy list to avoid modification during iteration
            if worker.isRunning():
                worker.quit()
                worker.wait(2000)  # Wait up to 2 seconds for each worker
            worker.deleteLater()
        self.active_workers.clear()
        event.accept()


def main():
    try:
        app = QApplication(sys.argv)
        window = ChemicalEquipmentApp()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        # Show error dialog if possible
        try:
            # Use a different variable name to avoid shadowing
            from PyQt5.QtWidgets import QMessageBox
            app_instance = QApplication.instance()
            if app_instance:
                QMessageBox.critical(None, "Fatal Error", f"The application encountered a fatal error:\n\n{str(e)}\n\nCheck the console for details.")
        except:
            pass
        sys.exit(1)


if __name__ == '__main__':
    main()
