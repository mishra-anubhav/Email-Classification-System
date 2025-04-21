"""
Prompt templates and engineering notes for Email Automation.

Prompt Engineering Iterations:
1. Initial version combined system and user prompts but led to inconsistent outputs.
2. Separated system prompt to define the assistant's role clearly.
3. Added explicit instruction to 'Respond with only the category' to reduce noise.
4. Set temperature=0 for deterministic classification outputs.

Edge Case Handling:
- Empty subject or body falls back to empty string placeholders.
- Post-validation ensures only predefined categories are accepted.
"""

# Classification prompts
CLASSIFICATION_SYSTEM_PROMPT = (
    "You are a classification engine that assigns customer emails "
    "to one of the following categories: complaint, inquiry, "
    "feedback, support_request, or other. Provide exactly one "
    "category as the output."
)

CLASSIFICATION_USER_PROMPT = (
    "Email Subject: {subject}\n"
    "Email Body: {body}\n\n"
    "Please classify this email into one of: complaint, inquiry, feedback, "
    "support_request, other. Respond with only the category."
)

# Response generation prompts
RESPONSE_SYSTEM_PROMPT = (
    "You are a customer support assistant. Generate a concise, "
    "professional email response tailored to the customer's needs."
)

RESPONSE_USER_PROMPT = (
    "Classification: {classification}\n"
    "Email Subject: {subject}\n"
    "Email Body: {body}\n\n"
    "Write an appropriate response to this email."
)