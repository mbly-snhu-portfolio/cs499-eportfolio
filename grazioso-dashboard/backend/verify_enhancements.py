import sys
import os
import logging
from datetime import datetime

# Add the backend directory to the python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import db_manager
from app.services.animal_shelter_service import AnimalShelterService
from app.services.audit_service import audit_service

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def verify_enhancements():
    try:
        logger.info("Starting verification of database enhancements...")
        
        # Connect to database
        db_manager.connect()
        # Refresh audit collection now that DB is connected
        audit_service._ensure_audit_collection()
        
        service = AnimalShelterService()
        
        # 1. Verify Advanced Indexing
        logger.info("\n[1] Verifying Advanced Indexing...")
        service.ensure_indexes()
        indexes = db_manager.get_collection().index_information()
        expected_indexes = ["idx_type_breed", "idx_outcome_type", "idx_type_age", "idx_text_search"]
        for idx in expected_indexes:
            if idx in indexes:
                logger.info(f"✅ Index '{idx}' exists.")
            else:
                logger.error(f"❌ Index '{idx}' MISSING!")
        
        # 2. Verify Audit Logging (Create, Update, Delete)
        logger.info("\n[2] Verifying Audit Logging...")
        
        # Create
        test_animal = {
            "animal_id": "VERIFY001",
            "name": "VerifyBot",
            "animal_type": "Robot",
            "breed": "Automaton",
            "age_upon_outcome": "1 year",
            "outcome_type": "Transfer",
            "age_upon_outcome_in_weeks": 52.0
        }
        created = service.create(test_animal)
        logger.info(f"Created test animal with ID: {created['_id']}")
        
        # Update
        update_data = {"name": "VerifyBot Updated"}
        service.update(created["animal_id"], update_data)
        logger.info("Updated test animal")
        
        # 3. Verify Aggregation Pipeline
        logger.info("\n[3] Verifying Aggregation Pipeline (Species Stats)...")
        stats = service.get_species_stats()
        if stats:
            logger.info(f"✅ Aggregation returned {len(stats)} groups.")
            logger.info("Top 5 groups by count:")
            for group in stats[:5]:
                logger.info(f" - Species: {group.get('species')}, Outcome: {group.get('outcome')}, Count: {group.get('count')}, Avg Age: {group.get('avg_age_weeks')} weeks")
        else:
            logger.error("❌ Aggregation returned no results!")

        # Delete
        service.delete(created["animal_id"])
        logger.info("Deleted test animal")

        # Check Audit Logs
        audit_logs = list(audit_service.audit_collection.find().sort("timestamp", -1).limit(3))
        logger.info(f"Found {len(audit_logs)} recent audit logs:")
        for log in audit_logs:
            logger.info(f" - [{log['timestamp']}] {log['action']} on {log['collection']} (ID: {log.get('document_id')})")
            
        actions = [log['action'] for log in audit_logs]
        if "DELETE" in actions and "UPDATE" in actions and "CREATE" in actions:
             logger.info("✅ Audit logging verified for CREATE, UPDATE, DELETE.")
        else:
             logger.error("❌ Audit logging verification FAILED. Missing actions.")

        logger.info("\nVerification completed.")
        
    except Exception as e:
        logger.error(f"Verification failed: {str(e)}")
    finally:
        db_manager.disconnect()

if __name__ == "__main__":
    verify_enhancements()
