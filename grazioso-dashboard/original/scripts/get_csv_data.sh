#!/bin/bash
# Script to help users get the AAC CSV data file

echo "📁 AAC CSV Data Setup"
echo "====================="

# Check if assets directory exists
if [ ! -d "assets" ]; then
    echo "Creating assets directory..."
    mkdir -p assets
fi

# Check if CSV file already exists
if [ -f "assets/aac_shelter_outcomes.csv" ]; then
    echo "CSV file already exists in assets/"
    echo "   File size: $(du -h assets/aac_shelter_outcomes.csv | cut -f1)"
    exit 0
fi

echo "📋 To use automatic data import, you need the AAC CSV file."
echo ""
echo "Options:"
echo "1. Copy from existing location:"
echo "   cp /path/to/aac_shelter_outcomes.csv assets/"
echo ""
echo "2. Download from source (if available):"
echo "   wget -O assets/aac_shelter_outcomes.csv <URL>"
echo ""
echo "3. For Apporto deployment:"
echo "   The file should be at /usr/local/datasets/aac_shelter_outcomes.csv"
echo ""
echo "4. Manual import later:"
echo "   Place the file anywhere and run: python import_aac_data.py"
echo ""
echo "💡 Once you have the CSV file in assets/, run:"
echo "   docker-compose up -d"
echo "   This will automatically import the data when containers start." 