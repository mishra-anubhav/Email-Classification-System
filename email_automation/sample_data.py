"""
Sample data for demonstration of the Email Automation System.
"""
from .models import Email

# Predefined set of sample emails
sample_emails = [
    Email(
        id="001",
        sender="angry.customer@example.com",
        subject="Broken product received",
        body=(
            "I received my order #12345 yesterday but it arrived completely damaged. "
            "This is unacceptable and I demand a refund immediately. "
            "This is the worst customer service I've experienced."
        ),
        timestamp="2024-03-15T10:30:00Z"
    ),
    Email(
        id="002",
        sender="curious.shopper@example.com",
        subject="Question about product specifications",
        body=(
            "Hi, I'm interested in buying your premium package but I couldn't find "
            "information about whether it's compatible with Mac OS. Could you please clarify this? Thanks!"
        ),
        timestamp="2024-03-15T11:45:00Z"
    ),
    Email(
        id="003",
        sender="happy.user@example.com",
        subject="Amazing customer support",
        body=(
            "I just wanted to say thank you for the excellent support I received from Sarah on your team. "
            "She went above and beyond to help resolve my issue. Keep up the great work!"
        ),
        timestamp="2024-03-15T13:15:00Z"
    ),
    Email(
        id="004",
        sender="tech.user@example.com",
        subject="Need help with installation",
        body=(
            "I've been trying to install the software for the past hour but keep getting error code 5123. "
            "I've already tried restarting my computer and clearing the cache. Please help!"
        ),
        timestamp="2024-03-15T14:20:00Z"
    ),
    Email(
        id="005",
        sender="business.client@example.com",
        subject="Partnership opportunity",
        body=(
            "Our company is interested in exploring potential partnership opportunities with your organization. "
            "Would it be possible to schedule a call next week to discuss this further?"
        ),
        timestamp="2024-03-15T15:00:00Z"
    ),
]