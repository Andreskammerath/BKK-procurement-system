#!/bin/bash

# BKK Procurement System - Setup Script
# This script helps set up the Django project

echo "================================================"
echo "BKK Procurement System - Setup Script"
echo "================================================"
echo ""

# Check if we're in a Docker environment
if [ -f /.dockerenv ]; then
    echo "Running in Docker environment..."
    IN_DOCKER=true
else
    echo "Running in local environment..."
    IN_DOCKER=false
fi

# Function to run Django commands
run_django() {
    if [ "$IN_DOCKER" = true ]; then
        python manage.py "$@"
    else
        python manage.py "$@"
    fi
}

echo "Step 1: Creating migrations..."
run_django makemigrations users
run_django makemigrations core
run_django makemigrations procurement
run_django makemigrations

echo ""
echo "Step 2: Applying migrations..."
run_django migrate

echo ""
echo "Step 3: Creating directories..."
mkdir -p media staticfiles logs

echo ""
echo "Step 4: Collecting static files..."
run_django collectstatic --noinput

echo ""
echo "================================================"
echo "Setup completed successfully!"
echo "================================================"
echo ""
echo "Next steps:"
echo "1. Create a superuser: python manage.py createsuperuser"
echo "2. Run the development server: python manage.py runserver"
echo "3. Access the application at: http://localhost:8000"
echo "4. Access the admin at: http://localhost:8000/admin/"
echo ""
echo "If using Docker:"
echo "1. docker-compose exec web python manage.py createsuperuser"
echo "2. Access at: http://localhost:8000"
echo ""

