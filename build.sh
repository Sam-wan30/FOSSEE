#!/bin/bash

echo "Building Chemical Equipment Parameter Visualizer..."

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r backend/requirements.txt

# Install Node.js dependencies and build frontend
echo "Installing Node.js dependencies..."
cd frontend
npm install

echo "Building frontend..."
npm run build

# Copy built frontend to Django static files
echo "Copying frontend build to Django..."
cd ..
mkdir -p backend/static
cp -r frontend/build/* backend/static/

# Run Django migrations
echo "Running Django migrations..."
cd backend
python manage.py migrate

echo "Build completed successfully!"
