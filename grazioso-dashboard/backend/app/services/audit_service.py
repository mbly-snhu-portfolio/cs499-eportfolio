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
        # NOTE: Do not eagerly initialize here. App startup connects to MongoDB
        # inside the FastAPI lifespan hook, so this service can be imported
        # before the DB is available. We initialize lazily on first use.
    
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
        if self.audit_collection is None:
            # Try to initialize now that the DB may be connected.
            self._ensure_audit_collection()
            if self.audit_collection is None:
                logger.warning("Audit collection not available, skipping audit log")
                return
        
        try:
            # Create Pydantic model instance for validation
            from app.models.audit_log import AuditLog
            
            audit_entry = AuditLog(
                user_id=user_id,
                username=username,
                action=action,
                collection=collection,
                document_id=document_id,
                changes=changes or {},
                ip_address=ip_address,
                user_agent=user_agent,
                success=success,
                error_message=error_message
            )
            
            # Convert to dict for MongoDB insertion
            # by_alias=True is not strictly needed here but good practice if we had aliased fields
            # exclude_none=False to keep explicit None values if needed, though usually we want to keep them
            entry_dict = audit_entry.model_dump()
            
            self.audit_collection.insert_one(entry_dict)
            logger.debug(f"Audit log created: {action} on {collection} by {username}")
        except Exception as e:
            logger.error(f"Failed to create audit log: {str(e)}")


# Global audit service instance
audit_service = AuditService()

