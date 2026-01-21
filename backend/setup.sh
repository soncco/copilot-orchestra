#!/bin/bash

# TravesIA Backend - Quick Setup Script
# This script sets up the development environment

set -e

echo "🚀 TravesIA Backend Setup"
echo "=========================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check Python version
echo "📋 Checking prerequisites..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "   Python version: $python_version"

# Check if PostgreSQL is installed
if command -v psql &> /dev/null; then
    echo -e "   ${GREEN}✓${NC} PostgreSQL installed"
else
    echo -e "   ${RED}✗${NC} PostgreSQL not found. Please install PostgreSQL 15+"
    exit 1
fi

# Check if Redis is installed
if command -v redis-cli &> /dev/null; then
    echo -e "   ${GREEN}✓${NC} Redis installed"
else
    echo -e "   ${YELLOW}⚠${NC}  Redis not found. Install for caching support"
fi

echo ""

# Create virtual environment
echo "🐍 Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "   ${GREEN}✓${NC} Virtual environment created"
else
    echo -e "   ${YELLOW}⚠${NC}  Virtual environment already exists"
fi

# Activate virtual environment
echo "   Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt
echo -e "   ${GREEN}✓${NC} Dependencies installed"

# Setup environment file
echo ""
if [ ! -f ".env" ]; then
    echo "⚙️  Setting up environment variables..."
    cp .env.example .env
    echo -e "   ${GREEN}✓${NC} .env file created"
    echo -e "   ${YELLOW}⚠${NC}  Please edit .env with your configuration"
else
    echo -e "   ${YELLOW}⚠${NC}  .env file already exists"
fi

# Initialize database
echo ""
read -p "🗄️  Do you want to initialize the database? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "   Running database initialization script..."
    cd ../database
    chmod +x scripts/init_database.sh
    ./scripts/init_database.sh
    cd ../backend
    echo -e "   ${GREEN}✓${NC} Database initialized"
fi

# Run migrations
echo ""
echo "🔄 Running Django migrations..."
python manage.py makemigrations
python manage.py migrate
echo -e "   ${GREEN}✓${NC} Migrations completed"

# Create superuser
echo ""
read -p "👤 Do you want to create a superuser? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python manage.py createsuperuser
fi

# Collect static files
echo ""
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput
echo -e "   ${GREEN}✓${NC} Static files collected"

echo ""
echo -e "${GREEN}✅ Setup complete!${NC}"
echo ""
echo "To start the development server:"
echo "   1. Activate virtual environment: source venv/bin/activate"
echo "   2. Run server: python manage.py runserver"
echo "   3. Visit: http://localhost:8000"
echo "   4. Admin panel: http://localhost:8000/admin/"
echo "   5. API docs: http://localhost:8000/api/docs/"
echo ""
echo "To start with Docker:"
echo "   docker-compose up -d"
echo ""
