#!/usr/bin/env python3
"""
Simple AAC Data Import Script
CS 340 Module Four Milestone

This script provides a simple way to import the AAC shelter outcomes CSV file
into MongoDB. It will automatically find the CSV file and import it using
the AnimalShelter CRUD operations.
"""

import sys
import os
from pathlib import Path

# Add the animal_shelter package to the path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from animal_shelter import AACDataImporter
except ImportError as e:
    print(f"❌ Error importing AnimalShelter: {e}")
    print("💡 Make sure you have installed the requirements: pip install -r requirements.txt")
    sys.exit(1)


def main():
    """Main function to run the AAC data import."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Import AAC shelter data into MongoDB')
    parser.add_argument('--force', action='store_true', 
                       help='Force import even if data already exists')
    parser.add_argument('--check-only', action='store_true',
                       help='Only check if data exists, do not import')
    parser.add_argument('--batch-size', type=int, default=None,
                       help='Number of records to process in each batch')
    
    args = parser.parse_args()
    
    print("🚀 AAC Data Import Script")
    print("=" * 50)
    
    try:
        # Create importer instance
        print("📁 Looking for AAC CSV file...")
        importer = AACDataImporter()
        
        print(f"Found CSV file: {importer.csv_path}")
        print(f"📊 File size: {importer.csv_path.stat().st_size / 1024 / 1024:.2f} MB")
        
        if args.check_only:
            # Only check existing data
            print("\n🔍 Checking database status...")
            existing_data = importer.check_existing_data()
            print(f"📊 Database Status: {existing_data['message']}")
            if existing_data.get('data_exists', False):
                print(f"📈 Total Documents: {existing_data['total_documents']:,}")
                print(f"🐕 Animal Types: {', '.join(existing_data['animal_types'])}")
                print(f"🏠 Outcome Types: {', '.join(existing_data['outcome_types'])}")
            return 0
        
        # Run the import
        print("\n🔄 Starting data import...")
        batch_size = args.batch_size or int(os.getenv('BATCH_SIZE', '500'))
        results = importer.run_full_import(batch_size=batch_size, force_import=args.force)
        
        # Handle skipped imports
        if results.get('skipped', False):
            print(f"\n⏭️  {results['message']}")
            existing = results['existing_data']
            print(f"📊 Found {existing['total_documents']:,} existing records")
            print(f"🐕 Animal Types: {', '.join(existing['animal_types'])}")
            print(f"🏠 Outcome Types: {', '.join(existing['outcome_types'])}")
            print("\n💡 Use --force to reimport the data")
            return 0
        
        # Display results for successful imports
        if results['success']:
            print("\n" + "=" * 50)
            summary = importer.get_import_summary(results)
            print(summary)
            print("\n🎉 Import completed successfully!")
            print("📝 You can now run the Jupyter notebook to test the CRUD operations.")
            return 0
        else:
            print(f"\n❌ Import failed: {results['error']}")
            return 1
            
    except FileNotFoundError as e:
        print(f"❌ CSV file not found: {e}")
        print("\n💡 Please ensure the 'aac_shelter_outcomes.csv' file is available.")
        print("   Common locations:")
        print("   - /usr/local/datasets/aac_shelter_outcomes.csv (Apporto)")
        print("   - ./aac_shelter_outcomes.csv (current directory)")
        print("   - ./data/aac_shelter_outcomes.csv (data subdirectory)")
        return 1
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("\n💡 Make sure MongoDB is running and accessible.")
        print("   If using Docker: docker-compose up -d")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 