#!/bin/bash
# =====================================================
# TravesIA Database - Backup Script
# =====================================================
# Description: Creates a backup of the PostgreSQL database
# Author: Database Agent
# Date: 2026-01-20
# Version: 1.0
# =====================================================

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Configuration
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"
DB_NAME="${DB_NAME:-travesia}"
DB_USER="${DB_USER:-postgres}"
BACKUP_DIR="${BACKUP_DIR:-./backups}"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/${DB_NAME}_${DATE}.backup"

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

echo -e "${YELLOW}Creating backup...${NC}"
echo "Database: $DB_NAME"
echo "Backup file: $BACKUP_FILE"
echo ""

# Create backup (custom format, compressed)
PGPASSWORD=$DB_PASSWORD pg_dump \
    -h $DB_HOST \
    -p $DB_PORT \
    -U $DB_USER \
    -F c \
    -b \
    -v \
    -f $BACKUP_FILE \
    $DB_NAME

if [ $? -eq 0 ]; then
    # Compress backup
    gzip $BACKUP_FILE
    BACKUP_FILE="${BACKUP_FILE}.gz"

    BACKUP_SIZE=$(du -h $BACKUP_FILE | cut -f1)

    echo ""
    echo -e "${GREEN}✓ Backup completed successfully${NC}"
    echo "File: $BACKUP_FILE"
    echo "Size: $BACKUP_SIZE"
    echo ""

    # Clean old backups (keep last 7 days)
    echo -e "${YELLOW}Cleaning old backups (keeping last 7 days)...${NC}"
    find $BACKUP_DIR -name "${DB_NAME}_*.backup.gz" -mtime +7 -delete
    echo -e "${GREEN}✓ Cleanup completed${NC}"
else
    echo -e "${RED}✗ Backup failed${NC}"
    exit 1
fi

# Optional: Upload to S3 if configured
if [ ! -z "$AWS_S3_BUCKET" ]; then
    echo ""
    echo -e "${YELLOW}Uploading to S3...${NC}"
    aws s3 cp $BACKUP_FILE "s3://${AWS_S3_BUCKET}/backups/database/"

    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Upload to S3 completed${NC}"
    else
        echo -e "${YELLOW}⚠ S3 upload failed (local backup preserved)${NC}"
    fi
fi
