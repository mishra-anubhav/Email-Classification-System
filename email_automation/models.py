"""
Data models for Email Automation System.
"""
from dataclasses import dataclass
from typing import Optional

@dataclass
class Email:
    """
    Represents a customer email to be processed.
    """
    id: str
    sender: str
    subject: str
    body: str
    timestamp: Optional[str] = None

@dataclass
class ProcessingResult:
    """
    Result of processing an email through the automation pipeline.
    """
    email_id: str
    classification: Optional[str] = None
    response_sent: bool = False
    success: bool = False
    error: Optional[str] = None