"""
Email processing: classification and response generation.
"""
import logging
from typing import Optional
from .models import Email
from .llm_client import LLMClient
from .prompts import (
    CLASSIFICATION_SYSTEM_PROMPT,
    CLASSIFICATION_USER_PROMPT,
    RESPONSE_SYSTEM_PROMPT,
    RESPONSE_USER_PROMPT
)
from .config import (
    CLASSIFICATION_MODEL,
    RESPONSE_MODEL,
    CLASSIFICATION_TEMPERATURE,
    RESPONSE_TEMPERATURE
)

logger = logging.getLogger(__name__)

class EmailProcessor:
    """
    Handles email classification and response generation using an LLM.
    """
    def __init__(self, llm_client: LLMClient):
        self.llm = llm_client
        self.valid_categories = {
            "complaint", "inquiry", "feedback", "support_request", "other"
        }

    def classify(self, email: Email) -> Optional[str]:
        """
        Classify an email into a predefined category.
        Returns the category string or None on failure.
        """
        # Prepare prompts
        system_msg = {"role": "system", "content": CLASSIFICATION_SYSTEM_PROMPT}
        user_content = CLASSIFICATION_USER_PROMPT.format(
            subject=email.subject or "",
            body=email.body or ""
        )
        user_msg = {"role": "user", "content": user_content}
        try:
            raw = self.llm.chat_completion(
                model=CLASSIFICATION_MODEL,
                messages=[system_msg, user_msg],
                temperature=CLASSIFICATION_TEMPERATURE
            )
            category = raw.strip().lower()
            if category not in self.valid_categories:
                logger.warning(
                    f"Invalid category '{category}' for email {email.id}"
                )
                return None
            return category
        except Exception as e:
            logger.error(f"Classification error for {email.id}: {e}")
            return None

    def generate_response(self, email: Email, classification: str) -> Optional[str]:
        """
        Generate a response for the email based on its classification.
        Returns the response text or None on failure.
        """
        system_msg = {"role": "system", "content": RESPONSE_SYSTEM_PROMPT}
        user_content = RESPONSE_USER_PROMPT.format(
            classification=classification,
            subject=email.subject or "",
            body=email.body or ""
        )
        user_msg = {"role": "user", "content": user_content}
        try:
            raw = self.llm.chat_completion(
                model=RESPONSE_MODEL,
                messages=[system_msg, user_msg],
                temperature=RESPONSE_TEMPERATURE
            )
            return raw.strip()
        except Exception as e:
            logger.error(f"Response generation error for {email.id}: {e}")
            return None