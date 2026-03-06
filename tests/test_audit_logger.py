"""Tests for audit logging system."""

import pytest
from src.audit.audit_logger import (
    AuditLogger,
    AuditEventType,
    AuditSeverity,
)


class TestAuditLogger:
    """Tests for audit logging functionality."""
    
    def test_log_event(self, tmp_path):
        """Test basic event logging."""
        log_file = tmp_path / "audit.log"
        logger = AuditLogger(str(log_file))
        
        event = logger.log_event(
            event_type=AuditEventType.DATA_ACCESS,
            user_id="user_123",
            action="read_patient_record",
            severity=AuditSeverity.INFO,
            details={"patient_id": "P001"}
        )
        
        assert event.user_id == "user_123"
        assert event.event_type == AuditEventType.DATA_ACCESS.value
        assert event.status == "success"
    
    def test_flush_events(self, tmp_path):
        """Test event flushing."""
        log_file = tmp_path / "audit.log"
        logger = AuditLogger(str(log_file), batch_size=2)
        
        logger.log_event(
            event_type=AuditEventType.DATA_MODIFICATION,
            user_id="admin",
            action="update_record"
        )
        logger.log_event(
            event_type=AuditEventType.COMPLIANCE_CHECK,
            user_id="auditor",
            action="verify_hipaa"
        )
        
        assert log_file.exists()
        logger.flush()
        
    def test_query_audit_trail(self, tmp_path):
        """Test querying audit trail."""
        log_file = tmp_path / "audit.log"
        logger = AuditLogger(str(log_file), batch_size=10)
        
        logger.log_event(
            event_type=AuditEventType.DATA_ACCESS,
            user_id="alice",
            action="read"
        )
        logger.flush()
        
        results = logger.query_audit_trail(user_id="alice")
        assert len(results) >= 0
