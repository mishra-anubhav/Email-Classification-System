"""
Entry point for running the Email Automation System demonstration.
"""
import pandas as pd

from email_automation.config import configure_logging
from email_automation.llm_client import LLMClient
from email_automation.processor import EmailProcessor
from email_automation.automation import EmailAutomationSystem
from email_automation.sample_data import sample_emails


def run_demo() -> pd.DataFrame:
    """
    Configure logging, initialize system components, and process sample emails.
    Returns a pandas DataFrame summarizing the results.
    """
    logger = configure_logging()
    logger.info("Starting Email Automation System demo...")

    # Initialize LLM client and email processor
    llm_client = LLMClient()
    processor = EmailProcessor(llm_client)
    system = EmailAutomationSystem(processor)

    # Process sample emails
    results = system.process_batch(sample_emails)

    # Build summary DataFrame
    df = pd.DataFrame([r.__dict__ for r in results])
    logger.info("Demo completed. Here is the summary:")
    print(df[["email_id", "success", "classification", "response_sent"]])
    return df


if __name__ == "__main__":
    run_demo()