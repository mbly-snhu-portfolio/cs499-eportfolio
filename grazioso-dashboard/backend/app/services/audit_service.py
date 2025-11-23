"""
Audit logging service.
"""
from datetime import datetime
from typing import Dict, Any, Optional
from pymongo.collection import Collection
import logging
from app.core.database import db_manager

logger = logging.getLogger(__name__)


class AuditService:
    """Service for audit logging."""
    
    def __init__(self):
        """Initialize audit service."""
        self.audit_collection: Optional[Collection] = None
        self._ensure_audit_collection()
    
    def _ensure_audit_collection(self) -> None:
        """Ensure audit collection exists."""
        try:
            database = db_manager.get_database()
            self.audit_collection = database.get_collection("audit_logs")
            
            # Create indexes
            self.audit_collection.create_index("timestamp")
            self.audit_collection.create_index("user_id")
            self.audit_collection.create_index("action")
            self.audit_collection.create_index("collection")
            self.audit_collection.create_index("document_id")
        except Exception as e:
            logger.error(f"Failed to initialize audit collection: {str(e)}")
            self.audit_collection = None
    
    def log_operation(
        self,
        action: str,
        collection: str,
        user_id: str,
        username: str,
        document_id: Optional[str] = None,
        changes: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        success: bool = True,
        error_message: Optional[str] = None
    ) -> None:
        """
        Log an operation to the audit trail.
        
        Args:
            action: Action type (CREATE, READ, UPDATE, DELETE)
            collection: Collection name
            user_id: User ID
            username: Username
            document_id: Document ID
            changes: Before/after values
            ip_address: Client IP address
            user_agent: User agent string
            success: Whether operation succeeded
            error_message: Error message if failed
        """
        if not self.audit_collection:
            logger.warning("Audit collection not available, skipping audit log")
            return
        
        try:
            audit_entry = {
                "timestamp": datetime.utcnow(),
                "user_id": user_id,
                "username": username,
                "action": action,
                "collection": collection,
                "document_id": document_id,
                "changes": changes or {},
                "ip_address": ip_address,
                "user_agent": user_agent,
                "success": success,
                "error_message": error_message
            }
            
            self.audit_collection.insert_one(audit_entry)
            logger.debug(f"Audit log created: {action} on {collection} by {username}")
        except Exception as e:
            logger.error(f"Failed to create audit log: {str(e)}")


# Global audit service instance
audit_service = AuditService()

