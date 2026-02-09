#!/bin/bash

# Quick Setup Script for ETF Tracker
# This script helps you set up the project quickly

echo "=================================================="
echo "ETF TRACKER - QUICK SETUP"
echo "=================================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed${NC}"
    echo "Please install Python 3 and try again"
    exit 1
fi

echo -e "${GREEN}✅ Python 3 found${NC}"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo -e "${GREEN}✅ Dependencies installed${NC}"

# Copy .env.example to .env if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file from template..."
    cp .env.example .env
    echo -e "${YELLOW}⚠️  Please edit .env file and add your credentials${NC}"
    echo ""
    echo "You need to add:"
    echo "  - TELEGRAM_BOT_TOKEN"
    echo "  - TELEGRAM_CHAT_ID"
    echo "  - GOLD_API_KEY (optional)"
fi

echo ""
echo "=================================================="
echo "SETUP COMPLETE!"
echo "=================================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your credentials:"
echo "   ${YELLOW}nano .env${NC}"
echo ""
echo "2. Test locally:"
echo "   ${YELLOW}python test_local.py${NC}"
echo ""
echo "3. Run the tracker:"
echo "   ${YELLOW}python etf_tracker.py${NC}"
echo ""
echo "4. Set up GitHub:"
echo "   - Create a new repository"
echo "   - Add secrets in Settings > Secrets > Actions"
echo "   - Push this code to GitHub"
echo ""
echo "5. Set up cron-job.org for reliable scheduling"
echo ""
echo "For detailed instructions, see README.md"
echo ""
