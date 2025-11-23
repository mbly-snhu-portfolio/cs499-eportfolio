#!/bin/bash
# Startup script for data importer

echo "🚀 Starting AAC Data Importer..."

# Wait for MongoDB to be ready
echo "⏳ Waiting for MongoDB to be ready..."
until python -c "
import sys
import os
sys.path.append('.')
from animal_shelter.animal_shelter import AnimalShelter
try:
    host = os.getenv('MONGODB_HOST', 'mongodb')
    port = int(os.getenv('MONGODB_PORT', '27017'))
    shelter = AnimalShelter(host=host, port=port)
    shelter.close_connection()
    print('MongoDB is ready!')
    exit(0)
except Exception as e:
    print(f'MongoDB not ready yet: {e}')
    exit(1)
" 2>/dev/null; do
    echo "MongoDB not ready yet, waiting..."
    sleep 5
done

echo "MongoDB is ready!"

# Check if CSV file exists
if [ -f "assets/aac_shelter_outcomes.csv" ]; then
    echo "📁 Found CSV file, starting import (will skip if data already exists)..."
    python import_aac_data.py
else
    echo "⚠️  No CSV file found in assets/, skipping import"
    echo "💡 To import data later, place aac_shelter_outcomes.csv in assets/ and run:"
    echo "   docker-compose run --rm data-importer python import_aac_data.py"
fi

echo "Startup complete!" 