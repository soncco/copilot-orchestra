#!/bin/bash
# =====================================================
# TravesIA Database - Master Setup Script
# =====================================================
# Description: Executes all schema files in order
# Author: Database Agent
# Date: 2026-01-20
# Version: 1.0
# =====================================================

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Database connection parameters
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"
DB_NAME="${DB_NAME:-travesia}"
DB_USER="${DB_USER:-postgres}"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}TravesIA Database Setup${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Host: $DB_HOST"
echo "Port: $DB_PORT"
echo "Database: $DB_NAME"
echo "User: $DB_USER"
echo ""

# Check if database exists
echo -e "${YELLOW}Checking if database exists...${NC}"
DB_EXISTS=$(PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -lqt | cut -d \| -f 1 | grep -w $DB_NAME | wc -l)

if [ $DB_EXISTS -eq 0 ]; then
    echo -e "${YELLOW}Database does not exist. Creating...${NC}"
    PGPASSWORD=$DB_PASSWORD createdb -h $DB_HOST -p $DB_PORT -U $DB_USER $DB_NAME
    echo -e "${GREEN}✓ Database created${NC}"
else
    echo -e "${GREEN}✓ Database already exists${NC}"
fi

# Function to execute SQL file
execute_sql() {
    local file=$1
    local description=$2

    echo -e "${YELLOW}Executing: $description${NC}"
    PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f $file

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ $description completed${NC}"
    else
        echo -e "${RED}✗ Error executing $description${NC}"
        exit 1
    fi
}

# Execute schema files in order
SCHEMA_DIR="$(dirname "$0")/../schemas"

echo ""
echo -e "${YELLOW}========================================${NC}"
echo -e "${YELLOW}Installing Extensions${NC}"
echo -e "${YELLOW}========================================${NC}"
execute_sql "$SCHEMA_DIR/00_extensions.sql" "PostgreSQL Extensions"

echo ""
echo -e "${YELLOW}========================================${NC}"
echo -e "${YELLOW}Creating Schemas${NC}"
echo -e "${YELLOW}========================================${NC}"

execute_sql "$SCHEMA_DIR/01_circuit_management.sql" "Circuit Management Context"
execute_sql "$SCHEMA_DIR/02_suppliers.sql" "Supplier Management Context"
execute_sql "$SCHEMA_DIR/03_operations.sql" "Operations Context"
execute_sql "$SCHEMA_DIR/04_financial.sql" "Financial Context"
execute_sql "$SCHEMA_DIR/05_documents.sql" "Document Management Context"
execute_sql "$SCHEMA_DIR/06_auth_users.sql" "Authentication & Users"

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Database Setup Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Next steps:"
echo "1. Review the sample data inserted"
echo "2. Change the default admin password"
echo "3. Configure Django settings to connect to this database"
echo ""
