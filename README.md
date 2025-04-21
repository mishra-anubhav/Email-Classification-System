 # Email Classification & Automation System

 This repository implements a modular, end-to-end pipeline for classifying incoming customer emails using an LLM (OpenAI GPT-3.5) and automatically generating appropriate responses. Below is a technical walkthrough of the architecture, setup, implementation details, and workflow, designed for demonstration and extension.

 ## Architecture & Components

 1. **EmailProcessor**
    - Encapsulates all communication with the OpenAI API.
    - Methods:
      - `classify_email(email: Dict) -> Optional[str]`
        • Uses a zero-temperature chat completion (temperature=0) to deterministically assign one of five categories: `complaint`, `inquiry`, `feedback`, `support_request`, or `other`.
        • Validates that the model’s output matches a predefined set, logs warnings on unexpected outputs, and returns `None` if classification fails.
      - `generate_response(email: Dict, classification: str) -> Optional[str]`
        • Uses a moderate-temperature completion (temperature=0.7) to draft a concise, professional reply tailored to the input classification and email content.
        • Catches and logs any API errors, returning `None` on failure.

 2. **EmailAutomationSystem**
    - Orchestrates the full processing pipeline for each email.
    - `process_email(email: Dict) -> Dict`
      1. Classifies the email via `EmailProcessor.classify_email`.
      2. Generates a response via `EmailProcessor.generate_response`.
      3. Routes the output to category-specific handlers:
         - `complaint`: create an urgent ticket, send complaint response
         - `inquiry`: send standard response
         - `feedback`: log feedback, send thank-you response
         - `support_request`: create support ticket, send acknowledgment
         - `other`: send generic acknowledgment
      4. Returns a structured result object:
         ```python
         {
           "email_id": str,
           "classification": Optional[str],
           "response_sent": bool,
           "success": bool,
           "error": Optional[str]
         }
         ```

 3. **Mock Service Functions**
    - Stand-ins for real-world integrations (e.g., email dispatch, ticketing systems, feedback logs).
    - Easily replaceable with production-grade implementations.

 ## Setup & Installation

 1. **Clone the repository**:
    ```bash
    git clone <repo_url>
    cd <repo_dir>
    ```

 2. **Create and activate a Python virtual environment** (Python 3.9+):
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

 3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

 4. **Configure API credentials**:
    - Create a `.env` file in the project root:
      ```text
      OPENAI_API_KEY=your_openai_api_key_here
      ```
    - The code will load this environment variable via `python-dotenv`.

 ## Implementation Details & Justifications

 ### Classification Strategy
 - **Deterministic Output**: We set `temperature=0` to force the model to choose the most likely category, minimizing randomness.
 - **Prompt Structure**: A system prompt defines the role (classification engine) and a user prompt provides clear instructions, email subject/body, and enumerates valid categories.
 - **Validation Layer**: Any output not matching the hard-coded set is treated as a failure, triggering safe fall‑back behavior in the pipeline.

 ### Response Generation
 - **Contextual Prompting**: We pass both the assigned classification and original email content to the model.
 - **Balanced Creativity**: We use `temperature=0.7` to allow some variation in tone while keeping replies professional.
 - **Role Framing**: A system prompt frames the model as a “customer support assistant,” guiding response style.

 ### Pipeline Orchestration & Error Handling
 - **Separation of Concerns**: `EmailProcessor` handles all LLM interactions; `EmailAutomationSystem` focuses on business logic (ticketing, dispatch).
 - **Granular Error Management**: Each step (classification, generation, handling) is wrapped in try/except, logged, and the pipeline continues or fails gracefully without crashing.
 - **Result Aggregation**: Each processed email returns a dict capturing key metadata, enabling easy summary and downstream monitoring.

 ## Workflow Demonstration

1. **Run the main script**:
    ```bash
    python run.py
    ```
 2. **Observe console output**:
    - Logs showing classification decisions, API calls, and handler invocations.
    - A final Pandas DataFrame summarizing each email’s `email_id`, `classification`, `response_sent`, and `success` status.

 ## Extensibility & Production Considerations

 - **Real Integrations**: Swap out mock service functions (`send_standard_response`, `create_support_ticket`, etc.) for real API calls.
 - **Retry & Backoff**: Introduce exponential backoff strategies for transient API failures.
 - **Prompt Versioning**: Store prompts in version control or a prompt registry to track changes and perform A/B testing.
 - **Observability**: Integrate with centralized logging/metrics platforms (e.g., Datadog, ELK) to monitor classification accuracy, throughput, and error rates.
 - **Security & Compliance**: Securely manage API keys, encrypt sensitive data, and ensure compliance with data protection regulations (e.g., GDPR, HIPAA).

 ---

 With this blueprint and modular codebase, you have a clear, extensible framework for leveraging LLMs in automated email processing and response workflows.

## Prompt Engineering Iterations

### Initial Prompt
We began with a straightforward prompt:

```text
You are an email classification engine. Given the email subject and body, return only one of the following categories: complaint, inquiry, feedback, support_request, or other.
Email Subject: {subject}
Email Body: {body}
```

### Problems Encountered
- The model sometimes returned synonyms or variations (e.g., "support request" vs. "support_request").
- Without strict enumeration, classifications were inconsistent.
- Higher temperatures introduced randomness and misclassification.

### Improvements Made
- Explicit enumeration of valid categories in the prompt.
- Set `temperature=0` for deterministic classification.
- Added a validation layer to normalize and reject unexpected outputs.

## Examples Run

Run the pipeline on diverse email samples:

```bash
$ python run.py
[INFO] Processing Email ID: 1
[INFO] Classification: complaint
[INFO] Generated Response: "Hello Jane, I’m sorry to hear about the delay..."
[INFO] Processing Email ID: 2
[INFO] Classification: inquiry
[INFO] Generated Response: "Dear John, thank you for reaching out..."
[INFO] Processing Email ID: 3
[INFO] Classification: feedback
[INFO] Generated Response: "Hi Alex, thank you for your feedback..."
[INFO] Processing Email ID: 4
[INFO] Classification: support_request
[INFO] Generated Response: "Hello Sarah, I've created a ticket..."
[INFO] Processing Email ID: 5
[INFO] Classification: other
[INFO] Generated Response: "Hello, thank you for contacting us..."
```

We also tested edge cases:
- Empty subject or body defaults to `other`.
- Emails with ambiguous or minimal content.
- Non-English characters (ASCII encoding).

## Summary

- **Design Decisions**
  - Separation of concerns between classification and response generation.
  - Deterministic classification (`temperature=0`).
  - Modular handlers for each category.

- **Challenges Encountered**
  - Variations in model output formats.
  - Ensuring prompt clarity to avoid misclassification.
  - Managing API rate limits and error handling.

- **Potential Improvements**
  - Add retry/backoff logic for transient API failures.
  - Include few-shot examples to improve classification accuracy.
  - Expand or dynamically load categories based on configurations.
  - A/B test different prompts to optimize response style.

- **Production Considerations**
  - Secure management and rotation of API keys.
  - Centralized logging and monitoring of classification accuracy and latency.
  - Integration with real email and ticketing systems.
  - Compliance with data privacy regulations (e.g., GDPR, HIPAA).

- **Notes and Tips**
  - Start with a simple prompt implementation and iterate.
  - Document all prompt changes and measure their impact.
  - Always validate and normalize model outputs against expected formats.
  - Consider edge cases in email content (empty, ambiguous, non-English, special characters).

- **Assumptions**
  - Emails are plain text without attachments.
  - Inputs are in English.
  - Categories limited to: complaint, inquiry, feedback, support_request, other.