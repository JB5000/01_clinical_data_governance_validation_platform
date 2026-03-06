"""Audit logging system for clinical data governance compliance tracking."""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum


class AuditEventType(Enum):
    """Classification of auditable events."""
    DATA_ACCESS = "data_access"
    DATA_MODIFICATION = "data_modification"
    DATA_VALIDATION = "data_validation"
    COMPLIANCE_CHECK = "compliance_check"
    ACCESS_CONTROL = "access_control"
    ERROR_EVENT = "error_event"


class AuditSeverity(Enum):
    """Severity levels for audit events."""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass
class AuditEvent:
    """Immutable audit event record."""
    timestamp: str
    event_type: str
    user_id: str
    action: str
    severity: str
    details: Dict[str, Any]
    status: str


class AuditLogger:
    """Manages audit trail logging for clinical data governance."""
    
    def __init__(self, audit_log_path: str, batch_size: int = 100):
        """Initialize audit logger."""
        self.audit_log_path = Path(audit_log_path)
        self.batch_size = batch_size
        self._event_buffer: List[AuditEvent] = []
        self._setup_logger()
        self._ensure_audit_dir()
    
    def _setup_logger(self) -> None:
        """Configure logging for audit trail."""
        self.logger = logging.getLogger("audit")
        if not self.logger.handlers:
            handler = logging.FileHandler(self.audit_log_path)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
    
    def _ensure_audit_dir(self) -> None:
        """Ensure audit log directory exists."""
        self.audit_log_path.parent.mkdir(parents=True, exist_ok=True)
    
    def log_event(
        self,
        event_type: AuditEventType,
        user_id: str,
        action: str,
        severity: AuditSeverity = AuditSeverity.INFO,
        details: Optional[Dict[str, Any]] = None,
        status: str = "success"
    ) -> AuditEvent:
        """Log an audit event."""
        event = AuditEvent(
            timestamp=datetime.utcnow().isoformat(),
            event_type=event_type.value,
            user_id=user_id,
            action=action,
            severity=severity.value,
            details=details or {},
            status=status
        )
        self._buffer_event(event)
        return event
    
    def _buffer_event(self, event: AuditEvent) -> None:
        """Buffer event for batch writing."""
        self._event_buffer.append(event)
        if len(self._event_buffer) >= self.batch_size:
            self.flush()
    
    def flush(self) -> None:
        """Write buffered events to audit log."""
        if not self._event_buffer:
            return
        
        for event in self._event_buffer:
            try:
                event_dict = asdict(event)
                self.logger.info(json.dumps(event_dict))
            except Exception as e:
                self.logger.error(f"Failed to log audit event: {e}")
        
        self._event_buffer.clear()
    
    def query_audit_trail(
        self,
        user_id: Optional[str] = None,
        event_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Query audit trail with filters."""
        results = []
        
        if not self.audit_log_path.exists():
            return results
        
        with open(self.audit_log_path, 'r') as f:
            for line in f:
                try:
                    if '{' not in line:
                        continue
                    json_str = line[line.index('{'):]
                    event_dict = json.loads(json_str)
                    
                    if user_id and event_dict.get('user_id') != user_id:
                        continue
                    if event_type and event_dict.get('event_type') != event_type:
                        continue
                    
                    results.append(event_dict)
                except (json.JSONDecodeError, ValueError):
                    continue
        
        return results
    
    def __del__(self) -> None:
        """Ensure buffered events are written on cleanup."""
        try:
            self.flush()
        except Exception:
            pass
