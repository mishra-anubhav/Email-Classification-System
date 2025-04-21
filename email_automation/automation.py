"""
Orchestration of the email processing workflow.
"""
import logging
from typing import List
from .models import Email, ProcessingResult
from .processor import EmailProcessor
from .handlers import (
    complaint_handler,
    inquiry_handler,
    feedback_handler,
    support_request_handler,
    other_handler
)

logger = logging.getLogger(__name__)

class EmailAutomationSystem:
    """
    Automates classification, response generation, and handling of emails.
    """
    HANDLERS = {
        "complaint": complaint_handler,
        "inquiry": inquiry_handler,
        "feedback": feedback_handler,
        "support_request": support_request_handler,
        "other": other_handler,
    }

    def __init__(self, processor: EmailProcessor):
        self.processor = processor

    def process(self, email: Email) -> ProcessingResult:
        """
        Process a single email and return the ProcessingResult.
        """
        result = ProcessingResult(email_id=email.id)
        # Classification
        category = self.processor.classify(email)
        result.classification = category
        if not category:
            result.error = "Classification failed"
            logger.debug(f"Email {email.id}: Classification failed")
            return result
        # Response generation
        response = self.processor.generate_response(email, category)
        if response is None:
            result.error = "Response generation failed"
            logger.debug(f"Email {email.id}: Response generation failed")
            return result
        # Dispatch to handler
        handler = self.HANDLERS.get(category)
        try:
            handler(email, response)
            result.response_sent = True
            result.success = True
        except Exception as e:
            result.error = f"Handler error: {e}"
            logger.error(f"Error handling email {email.id}: {e}")
        return result

    def process_batch(self, emails: List[Email]) -> List[ProcessingResult]:
        """
        Process a batch of emails sequentially.
        """
        results = []
        for email in emails:
            logger.info(f"Processing email {email.id}")
            res = self.process(email)
            results.append(res)
        return results