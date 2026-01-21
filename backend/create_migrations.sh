#!/bin/bash

# TravesIA Backend - Migration Setup Script

set -e

echo "=========================================="
echo "  TravesIA Backend - Migrations Setup"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if we're in the backend directory
if [ ! -f "manage.py" ]; then
    echo -e "${RED}Error: manage.py not found. Please run this script from the backend/ directory.${NC}"
    exit 1
fi

echo -e "${YELLOW}Step 1: Creating migrations for all apps...${NC}"
echo ""

# Create migrations for each app
apps=("authentication" "circuits" "suppliers" "operations" "financial" "documents")

for app in "${apps[@]}"; do
    echo -e "${GREEN}Creating migrations for apps.${app}...${NC}"
    python manage.py makemigrations $app
    echo ""
done

echo -e "${YELLOW}Step 2: Checking for any other pending migrations...${NC}"
python manage.py makemigrations
echo ""

echo -e "${YELLOW}Step 3: Showing migration plan...${NC}"
python manage.py showmigrations
echo ""

echo -e "${GREEN}=========================================="
echo "  Migrations created successfully!"
echo "==========================================${NC}"
echo ""
echo "To apply migrations, run:"
echo "  python manage.py migrate"
echo ""
echo "Or using Docker:"
echo "  docker-compose exec web python manage.py migrate"
echo ""
