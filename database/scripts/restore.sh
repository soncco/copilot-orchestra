#!/bin/bash
# =====================================================
# TravesIA Database - Restore Script
# =====================================================
# Description: Restores a PostgreSQL database from backup
# Author: Database Agent
# Date: 2026-01-20
# Version: 1.0
# =====================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Configuration
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"
DB_NAME="${DB_NAME:-travesia}"
DB_USER="${DB_USER:-postgres}"
BACKUP_FILE=$1

if [ -z "$BACKUP_FILE" ]; then
    echo -e "${RED}Error: Backup file not specified${NC}"
    echo "Usage: $0 <backup_file.backup.gz>"
    echo ""
    echo "Available backups:"
    ls -lh ./backups/*.backup.gz 2>/dev/null || echo "No backups found"
    exit 1
fi

if [ ! -f "$BACKUP_FILE" ]; then
    echo -e "${RED}Error: Backup file not found: $BACKUP_FILE${NC}"
    exit 1
fi

echo -e "${YELLOW}========================================${NC}"
echo -e "${YELLOW}TravesIA Database Restore${NC}"
echo -e "${YELLOW}========================================${NC}"
echo ""
echo "Database: $DB_NAME"
echo "Backup file: $BACKUP_FILE"
echo ""
echo -e "${RED}WARNING: This will DROP the existing database!${NC}"
echo -e "${RED}All current data will be LOST!${NC}"
echo ""
read -p "Are you sure you want to continue? (yes/no): " CONFIRM

if [ "$CONFIRM" != "yes" ]; then
    echo "Restore cancelled."
    exit 0
fi

# Decompress if needed
if [[ $BACKUP_FILE == *.gz ]]; then
    echo -e "${YELLOW}Decompressing backup...${NC}"
    gunzip -k $BACKUP_FILE
    BACKUP_FILE="${BACKUP_FILE%.gz}"
fi

# Terminate active connections
echo -e "${YELLOW}Terminating active connections...${NC}"
PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d postgres << EOF
SELECT pg_terminate_backend(pg_stat_activity.pid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname = '$DB_NAME'
  AND pid <> pg_backend_pid();
EOF

# Drop existing database
echo -e "${YELLOW}Dropping existing database...${NC}"
PGPASSWORD=$DB_PASSWORD dropdb -h $DB_HOST -p $DB_PORT -U $DB_USER --if-exists $DB_NAME

# Create new database
echo -e "${YELLOW}Creating new database...${NC}"
PGPASSWORD=$DB_PASSWORD createdb -h $DB_HOST -p $DB_PORT -U $DB_USER $DB_NAME

# Restore from backup
echo -e "${YELLOW}Restoring from backup...${NC}"
PGPASSWORD=$DB_PASSWORD pg_restore \
    -h $DB_HOST \
    -p $DB_PORT \
    -U $DB_USER \
    -d $DB_NAME \
    -v \
    $BACKUP_FILE

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}Restore completed successfully!${NC}"
    echo -e "${GREEN}========================================${NC}"
else
    echo -e "${RED}✗ Restore failed${NC}"
    exit 1
fi

# Clean up decompressed file if it was compressed
if [[ $1 == *.gz ]]; then
    rm $BACKUP_FILE
fi
