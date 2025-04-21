"""
Configuration for Email Automation System.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# OpenAI API configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise EnvironmentError("Missing OPENAI_API_KEY environment variable.")

# LLM settings
CLASSIFICATION_MODEL = os.getenv("CLASSIFICATION_MODEL", "gpt-3.5-turbo")
RESPONSE_MODEL = os.getenv("RESPONSE_MODEL", "gpt-3.5-turbo")
CLASSIFICATION_TEMPERATURE = float(os.getenv("CLASSIFICATION_TEMPERATURE", 0.0))
RESPONSE_TEMPERATURE = float(os.getenv("RESPONSE_TEMPERATURE", 0.7))
# Retry settings for LLM calls
LLM_MAX_RETRIES = int(os.getenv("LLM_MAX_RETRIES", 3))
LLM_RETRY_BACKOFF = float(os.getenv("LLM_RETRY_BACKOFF", 1.5))  # seconds initial backoff

# Logging configuration
import logging

def configure_logging(level: int = logging.INFO):
    """
    Configure root logger to output to console with timestamp and level.
    """
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    logger = logging.getLogger()
    if not logger.handlers:
        logger.addHandler(handler)
    logger.setLevel(level)
    return logger