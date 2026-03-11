#!/bin/bash

# ===== NORTHFLANK STARTUP SCRIPT =====
# Untuk deployment di Northflank dengan auto-restart

set -e  # Exit jika error

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}🚀 TELETHON RESEND BOT - NORTHFLANK${NC}"
echo -e "${GREEN}========================================${NC}"

# Check environment variables
echo -e "${YELLOW}🔍 Validating environment variables...${NC}"
required_vars=("API_ID" "API_HASH" "SOURCE_CHAT" "TARGET_GROUP")

for var in "${required_vars[@]}"; do
    if [ -z "${!var}" ]; then
        echo -e "${RED}❌ Missing environment variable: $var${NC}"
        exit 1
    fi
done

echo -e "${GREEN}✅ All environment variables present${NC}"

# Check session file
echo -e "${YELLOW}🔐 Checking session file...${NC}"
if [ ! -f "session.session" ]; then
    echo -e "${RED}❌ Session file not found!${NC}"
    echo -e "${RED}❌ You haven't logged in yet${NC}"
    echo -e "${YELLOW}📝 Steps to fix:${NC}"
    echo -e "   1. Run locally: python login.py"
    echo -e "   2. Upload session.session to Northflank persistent storage"
    echo -e "   3. Then run this script again"
    exit 1
fi

echo -e "${GREEN}✅ Session file found${NC}"

# Check downloads directory
mkdir -p downloads
echo -e "${GREEN}✅ Downloads directory ready${NC}"

# Run bot dengan auto-restart logic
attempt=0
max_attempts=5

while [ $attempt -lt $max_attempts ]; do
    attempt=$((attempt + 1))
    
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}🎯 Attempt $attempt / $max_attempts${NC}"
    echo -e "${GREEN}========================================${NC}"
    
    if python main.py; then
        echo -e "${GREEN}✅ Bot completed successfully${NC}"
        exit 0
    else
        exit_code=$?
        echo -e "${RED}❌ Bot crashed with exit code $exit_code${NC}"
        
        if [ $attempt -lt $max_attempts ]; then
            wait_time=$((2 ** attempt))
            if [ $wait_time -gt 60 ]; then
                wait_time=60
            fi
            echo -e "${YELLOW}🔄 Restarting in ${wait_time}s...${NC}"
            sleep $wait_time
        fi
    fi
done

echo -e "${RED}========================================${NC}"
echo -e "${RED}❌ Max restart attempts ($max_attempts) exceeded${NC}"
echo -e "${RED}========================================${NC}"
exit 1
