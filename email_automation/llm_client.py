"""
Wrapper around OpenAI LLM calls with retry and error handling.
"""
import time
import logging
from openai import OpenAI, OpenAIError
from .config import (
    OPENAI_API_KEY,
    LLM_MAX_RETRIES,
    LLM_RETRY_BACKOFF
)

logger = logging.getLogger(__name__)

class LLMClient:
    """
    LLM Client to handle chat completions with retry logic.
    """
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def chat_completion(self, model: str, messages: list, temperature: float) -> str:
        """
        Call OpenAI chat completion with retries on failure.

        Returns the assistant's response content.
        Raises the last exception if all retries fail.
        """
        last_exception = None
        backoff = LLM_RETRY_BACKOFF
        for attempt in range(1, LLM_MAX_RETRIES + 1):
            try:
                response = self.client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=temperature
                )
                content = response.choices[0].message.content
                return content
            except OpenAIError as e:
                last_exception = e
                logger.warning(
                    f"LLM request failed attempt {attempt}/{LLM_MAX_RETRIES}: {e}"
                )
                if attempt < LLM_MAX_RETRIES:
                    time.sleep(backoff)
                    backoff *= 2
                else:
                    logger.error(
                        f"LLM request failed after {LLM_MAX_RETRIES} attempts."
                    )
        # All retries exhausted
        raise last_exception