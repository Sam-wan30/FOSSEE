#!/bin/bash

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies
cd frontend
npm install
cd ..

# Run Django migrations
cd backend
python manage.py migrate
cd ..

# Start both backend and frontend
# Start backend in background
cd backend
python manage.py runserver 0.0.0.0:8000 &
BACKEND_PID=$!
cd ..

# Start frontend with proxy to backend
cd frontend
# Set proxy to backend API
REACT_APP_API_URL=http://localhost:8000/api npm start &
FRONTEND_PID=$!
cd ..

# Wait for both processes
wait $BACKEND_PID
wait $FRONTEND_PID
