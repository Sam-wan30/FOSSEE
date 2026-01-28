#!/bin/bash

# Setup script for Chemical Equipment Parameter Visualizer

echo "========================================="
echo "Chemical Equipment Parameter Visualizer"
echo "Setup Script"
echo "========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version || { echo "Python 3 is required but not installed. Aborting."; exit 1; }

# Check Node.js version
echo "Checking Node.js version..."
node --version || { echo "Node.js is required but not installed. Aborting."; exit 1; }

# Setup Backend
echo ""
echo "Setting up Django Backend..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
echo ""
echo "Creating superuser for authentication..."
echo "Please enter username, email, and password when prompted:"
python manage.py createsuperuser
cd ..

# Setup Frontend
echo ""
echo "Setting up React Frontend..."
cd frontend
npm install
cd ..

# Setup Desktop
echo ""
echo "Setting up Desktop Application..."
cd desktop
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt
cd ..

echo ""
echo "========================================="
echo "Setup Complete!"
echo "========================================="
echo ""
echo "To start the application:"
echo ""
echo "1. Start Django Backend (Terminal 1):"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python manage.py runserver"
echo ""
echo "2. Start React Frontend (Terminal 2):"
echo "   cd frontend"
echo "   npm start"
echo ""
echo "3. Start Desktop App (Terminal 3):"
echo "   cd desktop"
echo "   source venv/bin/activate"
echo "   python main.py"
echo ""
echo "Web app will be available at: http://localhost:3000"
echo "API will be available at: http://localhost:8000"
echo ""
