#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}🚀 Telethon Resend - Docker Startup${NC}"

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${RED}❌ File .env tidak ditemukan!${NC}"
    echo -e "${YELLOW}📝 Salin .env.example ke .env dan isi dengan credentials Anda${NC}"
    echo -e "${YELLOW}   cp .env.example .env${NC}"
    exit 1
fi

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# Validate required environment variables
required_vars=("API_ID" "API_HASH" "SOURCE_CHAT" "TARGET_GROUP")
missing_vars=()

for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        missing_vars+=("$var")
    fi
done

if [ ${#missing_vars[@]} -gt 0 ]; then
    echo -e "${RED}❌ Harap penuhi kebutuhan environment terlebih dahulu!${NC}"
    echo -e "${RED}❌ Missing: ${missing_vars[*]}${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Environment variables valid${NC}"
echo -e "${GREEN}🐳 Starting Docker container...${NC}"

# Build dan run docker-compose
docker-compose up --build
