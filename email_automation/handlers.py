"""
Category-specific handlers for post-processing actions.
"""
import logging
from .models import Email
from .services import (
    send_complaint_response,
    send_standard_response,
    create_urgent_ticket,
    create_support_ticket,
    log_customer_feedback
)

logger = logging.getLogger(__name__)

def complaint_handler(email: Email, response: str) -> None:
    """
    Handle complaint category: create urgent ticket and send complaint response.
    """
    create_urgent_ticket(email.id, context=email.body)
    send_complaint_response(email.id, response)

def inquiry_handler(email: Email, response: str) -> None:
    """
    Handle inquiry category: send a standard response.
    """
    send_standard_response(email.id, response)

def feedback_handler(email: Email, response: str) -> None:
    """
    Handle feedback category: log feedback and send thank-you response.
    """
    log_customer_feedback(email.id, feedback=email.body)
    send_standard_response(email.id, response)

def support_request_handler(email: Email, response: str) -> None:
    """
    Handle support_request category: create support ticket and send acknowledgment.
    """
    create_support_ticket(email.id, context=email.body)
    send_standard_response(email.id, response)

def other_handler(email: Email, response: str) -> None:
    """
    Handle other category: send a generic response.
    """
    send_standard_response(email.id, response)