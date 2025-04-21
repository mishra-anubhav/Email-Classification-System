"""
Mock service functions simulating integrations (email, ticketing, feedback).
"""
import logging

logger = logging.getLogger(__name__)

def send_complaint_response(email_id: str, response: str) -> None:
    """
    Mock: send a complaint response via email service.
    """
    logger.info(f"[Service] Sending complaint response for email {email_id}")
    # TODO: Integrate with real email sending service

def send_standard_response(email_id: str, response: str) -> None:
    """
    Mock: send a standard response via email service.
    """
    logger.info(f"[Service] Sending standard response for email {email_id}")
    # TODO: Integrate with real email sending service

def create_urgent_ticket(email_id: str, context: str) -> None:
    """
    Mock: create an urgent ticket in the ticketing system.
    """
    logger.info(f"[Service] Creating urgent ticket for email {email_id}")
    # TODO: Integrate with real ticketing system

def create_support_ticket(email_id: str, context: str) -> None:
    """
    Mock: create a support ticket in the ticketing system.
    """
    logger.info(f"[Service] Creating support ticket for email {email_id}")
    # TODO: Integrate with real ticketing system

def log_customer_feedback(email_id: str, feedback: str) -> None:
    """
    Mock: log customer feedback in the feedback tracking system.
    """
    logger.info(f"[Service] Logging feedback for email {email_id}")
    # TODO: Integrate with real feedback tracking system