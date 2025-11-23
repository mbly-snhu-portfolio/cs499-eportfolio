"""
Data Importer for Austin Animal Center (AAC) Dataset
CS 340 Module Four Milestone

This module provides functionality to import the AAC shelter outcomes CSV file
into MongoDB using the AnimalShelter CRUD operations.
"""

import pandas as pd
import logging
import sys
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from tqdm import tqdm
import time

from .animal_shelter import AnimalShelter


class AACDataImporter:
    """
    Data importer for Austin Animal Center dataset.
    
    This class handles the import of the AAC shelter outcomes CSV file into
    MongoDB using the AnimalShelter CRUD operations.
    """
    
    def __init__(self, csv_path: Optional[str] = None):
        """
        Initialize the AAC data importer.
        
        Args:
            csv_path (Optional[str]): Path to the AAC CSV file. If None, will look
                                    in common locations including /usr/local/datasets/
        """
        self.csv_path = self._find_csv_file(csv_path)
        self.shelter = None
        self._setup_logging()
        
    def _find_csv_file(self, csv_path: Optional[str]) -> Path:
        """
        Find the AAC CSV file in common locations.
        
        Args:
            csv_path (Optional[str]): Explicit path to CSV file
            
        Returns:
            Path: Path to the CSV file
            
        Raises:
            FileNotFoundError: If CSV file cannot be found
        """
        if csv_path:
            path = Path(csv_path)
            if path.exists():
                return path
            else:
                raise FileNotFoundError(f"CSV file not found at specified path: {csv_path}")
        
        # Get search paths from environment variable or use defaults
        csv_search_paths = os.getenv('CSV_SEARCH_PATHS', 
            '/usr/local/datasets/aac_shelter_outcomes.csv,./aac_shelter_outcomes.csv,./data/aac_shelter_outcomes.csv,./assets/aac_shelter_outcomes.csv')
        
        search_paths = [Path(path.strip()) for path in csv_search_paths.split(',')]
        
        for path in search_paths:
            if path.exists():
                return path
        
        # If not found, provide helpful error message
        raise FileNotFoundError(
            f"AAC CSV file not found. Searched in: {[str(p) for p in search_paths]}\n"
            f"Please ensure the file 'aac_shelter_outcomes.csv' is available in one of these locations."
        )
        
    def _setup_logging(self) -> None:
        """Configure logging for the data import process."""
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(logging.INFO)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
    
    def validate_csv_file(self) -> bool:
        """
        Validate that the CSV file exists and is readable.
        
        Returns:
            bool: True if file is valid, False otherwise
        """
        try:
            if not self.csv_path.exists():
                self.logger.error(f"CSV file not found: {self.csv_path}")
                return False
            
            if not self.csv_path.is_file():
                self.logger.error(f"Path is not a file: {self.csv_path}")
                return False
            
            # Try to read the first few lines to validate format
            with open(self.csv_path, 'r', encoding='utf-8') as f:
                first_line = f.readline().strip()
                if not first_line or ',' not in first_line:
                    self.logger.error("CSV file appears to be empty or invalid format")
                    return False
            
            self.logger.info(f"CSV file validated: {self.csv_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Error validating CSV file: {str(e)}")
            return False
    
    def load_csv_data(self) -> pd.DataFrame:
        """
        Load the CSV data into a pandas DataFrame.
        
        Returns:
            pd.DataFrame: Loaded CSV data
        
        Raises:
            Exception: If CSV loading fails
        """
        try:
            self.logger.info(f"Loading CSV data from: {self.csv_path}")
            
            # Load CSV with pandas
            df = pd.read_csv(self.csv_path, encoding='utf-8')
            
            self.logger.info(f"Successfully loaded {len(df)} records with {len(df.columns)} columns")
            self.logger.info(f"Columns: {list(df.columns)}")
            
            # Display basic statistics
            self.logger.info(f"DataFrame shape: {df.shape}")
            self.logger.info(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
            
            return df
            
        except Exception as e:
            self.logger.error(f"Failed to load CSV data: {str(e)}")
            raise Exception(f"CSV loading failed: {str(e)}") from e
    
    def clean_data(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Clean and prepare the data for MongoDB import.
        
        Args:
            df (pd.DataFrame): Raw CSV data
        
        Returns:
            List[Dict[str, Any]]: Cleaned data ready for MongoDB
        """
        try:
            self.logger.info("Starting data cleaning process...")
            
            # Make a copy to avoid modifying original
            cleaned_df = df.copy()
            
            # Handle missing values
            cleaned_df = cleaned_df.fillna('')
            
            # Convert column names to lowercase for consistency
            cleaned_df.columns = cleaned_df.columns.str.lower()
            
            # Ensure animal_id is unique and not empty
            if 'animal_id' in cleaned_df.columns:
                # Remove rows with empty animal_id
                initial_count = len(cleaned_df)
                cleaned_df = cleaned_df[cleaned_df['animal_id'].astype(str).str.strip() != '']
                
                # Remove duplicates based on animal_id
                cleaned_df = cleaned_df.drop_duplicates(subset=['animal_id'])
                final_count = len(cleaned_df)
                
                if initial_count != final_count:
                    self.logger.info(f"Removed {initial_count - final_count} duplicate/empty animal_id records")
            
            # Convert DataFrame to list of dictionaries
            records = cleaned_df.to_dict('records')
            
            self.logger.info(f"Data cleaning completed. {len(records)} records ready for import")
            return records
            
        except Exception as e:
            self.logger.error(f"Error during data cleaning: {str(e)}")
            raise
    
    def import_data(self, records: List[Dict[str, Any]], batch_size: int = None) -> Dict[str, Any]:
        """
        Import data into MongoDB using the AnimalShelter class.
        
        Args:
            records (List[Dict[str, Any]]): List of records to import
            batch_size (int): Number of records to process in each batch
        
        Returns:
            Dict[str, Any]: Import statistics
        """
        try:
            self.logger.info(f"Starting data import of {len(records)} records...")
            
            # Get batch size from environment or use default
            if batch_size is None:
                batch_size = int(os.getenv('BATCH_SIZE', '1000'))
            
            # Initialize AnimalShelter connection
            self.shelter = AnimalShelter()
            
            # Import statistics
            stats = {
                'total_records': len(records),
                'successful_imports': 0,
                'failed_imports': 0,
                'errors': [],
                'start_time': time.time(),
                'end_time': None,
                'duration': None
            }
            
            # Process records in batches with progress bar
            total_batches = (len(records) + batch_size - 1) // batch_size
            
            with tqdm(total=len(records), desc="Importing records", unit="record") as pbar:
                for i in range(0, len(records), batch_size):
                    batch = records[i:i + batch_size]
                    batch_num = (i // batch_size) + 1
                    
                    self.logger.info(f"Processing batch {batch_num}/{total_batches} ({len(batch)} records)")
                    
                    for record in batch:
                        try:
                            # Use the create method from AnimalShelter
                            result = self.shelter.create(record)
                            if result:
                                stats['successful_imports'] += 1
                            else:
                                stats['failed_imports'] += 1
                                stats['errors'].append(f"Failed to import record: {record.get('animal_id', 'Unknown')}")
                        
                        except Exception as e:
                            stats['failed_imports'] += 1
                            error_msg = f"Error importing record {record.get('animal_id', 'Unknown')}: {str(e)}"
                            stats['errors'].append(error_msg)
                            self.logger.error(error_msg)
                        
                        pbar.update(1)
                    
                    # Progress update
                    progress = (i + len(batch)) / len(records) * 100
                    self.logger.info(f"Import progress: {progress:.1f}%")
            
            # Calculate final statistics
            stats['end_time'] = time.time()
            stats['duration'] = stats['end_time'] - stats['start_time']
            
            self.logger.info("Data import completed!")
            self.logger.info(f"Successful imports: {stats['successful_imports']}")
            self.logger.info(f"Failed imports: {stats['failed_imports']}")
            self.logger.info(f"Duration: {stats['duration']:.2f} seconds")
            
            return stats
            
        except Exception as e:
            self.logger.error(f"Error during data import: {str(e)}")
            raise
        finally:
            if self.shelter:
                self.shelter.close_connection()
    
    def check_existing_data(self) -> Dict[str, Any]:
        """
        Check if AAC data already exists in the database.
        
        Returns:
            Dict[str, Any]: Information about existing data including count and sample
        """
        try:
            self.logger.info("Checking for existing AAC data...")
            
            # Create new connection for checking
            shelter = AnimalShelter()
            
            # Get total document count
            total_docs = shelter.collection.count_documents({})
            
            if total_docs == 0:
                shelter.close_connection()
                return {
                    "data_exists": False,
                    "total_documents": 0,
                    "message": "No data found in database"
                }
            
            # Check if this looks like AAC data by examining sample documents
            sample_docs = list(shelter.collection.find().limit(5))
            
            # Look for AAC-specific fields
            aac_fields = ['animal_id', 'rec_num', 'outcome_type', 'animal_type']
            has_aac_structure = all(
                any(field in doc for field in aac_fields) 
                for doc in sample_docs
            )
            
            if has_aac_structure:
                # Get some statistics about the data
                animal_types = shelter.collection.distinct("animal_type")
                outcome_types = shelter.collection.distinct("outcome_type")
                
                shelter.close_connection()
                return {
                    "data_exists": True,
                    "total_documents": total_docs,
                    "animal_types": animal_types,
                    "outcome_types": outcome_types,
                    "sample_documents": sample_docs,
                    "message": f"Found {total_docs} AAC records in database"
                }
            else:
                shelter.close_connection()
                return {
                    "data_exists": False,
                    "total_documents": total_docs,
                    "message": f"Found {total_docs} documents but they don't appear to be AAC data"
                }
                
        except Exception as e:
            self.logger.error(f"Error checking existing data: {e}")
            return {
                "data_exists": False,
                "error": str(e),
                "message": f"Error checking database: {e}"
            }

    def verify_import(self) -> Dict[str, Any]:
        """
        Verify the imported data by checking collection statistics.
        
        Returns:
            Dict[str, Any]: Verification results
        """
        try:
            self.logger.info("Verifying imported data...")
            
            # Create new connection for verification
            shelter = AnimalShelter()
            
            # Get collection statistics
            stats = shelter.get_collection_stats()
            
            # Sample some records to verify data quality
            sample_records = shelter.read({})
            sample_size = min(5, len(sample_records))
            
            verification_results = {
                'collection_stats': stats,
                'sample_records': sample_records[:sample_size] if sample_records else [],
                'verification_passed': True,
                'sample_size': sample_size
            }
            
            self.logger.info(f"Verification completed. Collection contains {stats['total_documents']} documents")
            
            shelter.close_connection()
            return verification_results
            
        except Exception as e:
            self.logger.error(f"Error during verification: {str(e)}")
            return {'verification_passed': False, 'error': str(e)}
    
    def run_full_import(self, batch_size: int = None, force_import: bool = False) -> Dict[str, Any]:
        """
        Run the complete data import process.
        
        Args:
            batch_size (int): Number of records to process in each batch
            force_import (bool): If True, import even if data already exists
        
        Returns:
            Dict[str, Any]: Complete import results
        """
        try:
            self.logger.info("Starting full AAC data import process...")
            
            # Step 1: Check for existing data (unless forced)
            if not force_import:
                existing_data = self.check_existing_data()
                if existing_data.get("data_exists", False):
                    self.logger.info(f"Data already exists: {existing_data['message']}")
                    return {
                        'success': True,
                        'skipped': True,
                        'existing_data': existing_data,
                        'message': 'Import skipped - data already exists. Use force_import=True to override.',
                        'csv_file': str(self.csv_path)
                    }
            
            # Step 2: Validate CSV file
            if not self.validate_csv_file():
                raise Exception("CSV file validation failed")
            
            # Step 3: Load CSV data
            df = self.load_csv_data()
            
            # Step 4: Clean data
            records = self.clean_data(df)
            
            # Step 5: Import data
            import_stats = self.import_data(records, batch_size)
            
            # Step 6: Verify import
            verification_results = self.verify_import()
            
            # Combine results
            results = {
                'import_stats': import_stats,
                'verification_results': verification_results,
                'success': True,
                'skipped': False,
                'csv_file': str(self.csv_path),
                'total_records_processed': len(records)
            }
            
            self.logger.info("Full import process completed successfully!")
            return results
            
        except Exception as e:
            self.logger.error(f"Full import process failed: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'import_stats': {},
                'verification_results': {},
                'csv_file': str(self.csv_path) if hasattr(self, 'csv_path') else 'Unknown'
            }
    
    def get_import_summary(self, results: Dict[str, Any]) -> str:
        """
        Generate a human-readable summary of the import results.
        
        Args:
            results (Dict[str, Any]): Import results from run_full_import
            
        Returns:
            str: Formatted summary string
        """
        if not results['success']:
            return f"❌ Import failed: {results['error']}"
        
        stats = results['import_stats']
        verification = results['verification_results']
        
        summary = f"""
🎉 AAC DATA IMPORT COMPLETED SUCCESSFULLY
{'='*50}
📁 CSV File: {results['csv_file']}
📊 Total Records Processed: {results['total_records_processed']:,}
Successful Imports: {stats['successful_imports']:,}
❌ Failed Imports: {stats['failed_imports']:,}
⏱️  Duration: {stats['duration']:.2f} seconds
📈 Collection Documents: {verification['collection_stats']['total_documents']:,}
🎯 Success Rate: {(stats['successful_imports']/stats['total_records'])*100:.1f}%
{'='*50}
        """
        
        return summary.strip()


def main():
    """Main function to run the data import process."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Import AAC shelter data into MongoDB')
    parser.add_argument('--force', action='store_true', 
                       help='Force import even if data already exists')
    parser.add_argument('--check-only', action='store_true',
                       help='Only check if data exists, do not import')
    parser.add_argument('--batch-size', type=int, default=None,
                       help='Number of records to process in each batch')
    
    args = parser.parse_args()
    
    try:
        # Create importer instance
        importer = AACDataImporter()
        
        if args.check_only:
            # Only check existing data
            existing_data = importer.check_existing_data()
            print(f"📊 Database Status: {existing_data['message']}")
            if existing_data.get('data_exists', False):
                print(f"📈 Total Documents: {existing_data['total_documents']:,}")
                print(f"🐕 Animal Types: {', '.join(existing_data['animal_types'])}")
                print(f"🏠 Outcome Types: {', '.join(existing_data['outcome_types'])}")
            return
        
        # Run full import process
        results = importer.run_full_import(force_import=args.force, batch_size=args.batch_size)
        
        # Handle skipped imports
        if results.get('skipped', False):
            print(f"⏭️  {results['message']}")
            existing = results['existing_data']
            print(f"📊 Found {existing['total_documents']:,} existing records")
            print(f"🐕 Animal Types: {', '.join(existing['animal_types'])}")
            return
        
        # Display summary for successful imports
        if results['success']:
            summary = importer.get_import_summary(results)
            print(summary)
        else:
            print(f"❌ Import failed: {results['error']}")
            sys.exit(1)
            
    except Exception as e:
        print(f"Critical error in main: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main() 