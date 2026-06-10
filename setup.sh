#!/bin/bash

# Setup script for Dealership Review Application

echo "=== Dealership Review App Setup ==="

# Create virtual environment
echo "Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/Scripts/activate || . venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r server/requirements.txt

# Run migrations
echo "Running database migrations..."
cd server
python manage.py migrate

# Create superuser
echo "Creating superuser..."
python manage.py createsuperuser

# Load sample data
echo "Loading sample data..."
python manage.py loaddata sample_data.json 2>/dev/null || echo "Sample data fixture not found, skipping..."

# Create test data
echo "Creating test data..."
python populate_data.py

# Start server
echo "Starting Django development server..."
python manage.py runserver

