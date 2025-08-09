from core.email_imap import fetch_imap_emails
from core.email_sender import send_email, send_draft_to_gmail
from utils.logger import get_logger
from config import IMAP_USERNAME, IMAP_PASSWORD, IMAP_SERVER
from core.supervisor import supervisor_langgraph
from core.state import EmailState


logger = get_logger(__name__)


def process_email_action(email, your_name, action_type="send", gmail_address=None):
    """Process email action - send or draft"""
    if action_type == "send":
        if send_email(email, your_name):
            logger.info("Email sent successfully.")
            return {"status": "success", "message": "Email sent successfully"}
        else:
            logger.warning("Failed to send email.")
            return {"status": "error", "message": "Failed to send email"}
    elif action_type == "draft":
        if not gmail_address:
            return {"status": "error", "message": "Gmail address required for drafting"}
        if send_draft_to_gmail(email, your_name, gmail_address):
            logger.info("Draft sent to Gmail successfully.")
            return {"status": "success", "message": "Draft sent to Gmail successfully"}
        else:
            logger.warning("Failed to send draft to Gmail.")
            return {"status": "error", "message": "Failed to send draft to Gmail"}
    else:
        logger.warning("Invalid action type.")
        return {"status": "error", "message": "Invalid action type"}


def process_email_workflow(
    your_name, recipient_name, email_choice, action_type="send", gmail_address=None
):
    """Main email processing workflow for SUPERVAIZE agent"""
    logger.info("Starting email processing workflow.")

    try:
        # Use IMAP to fetch live emails
        emails = fetch_imap_emails(IMAP_USERNAME, IMAP_PASSWORD, IMAP_SERVER)
        logger.debug(f"Fetched {len(emails)} emails from IMAP.")

        if not emails:
            logger.info("No emails found.")
            return {"status": "error", "message": "No emails found"}

        latest_emails = emails[-5:]  # get the last 5 emails

        # Validate email choice
        if email_choice < 1 or email_choice > len(latest_emails):
            return {
                "status": "error",
                "message": f"Invalid email choice. Must be 1-{len(latest_emails)}",
            }

        selected_email = latest_emails[email_choice - 1]

        # Create state and process the email through the workflow
        state = EmailState()
        state.emails = [selected_email]
        state.current_email = selected_email
        state = supervisor_langgraph(selected_email, state, your_name, recipient_name)

        # Get the generated response
        response = selected_email.get("response", "No response generated.")

        # Process the action
        action_result = process_email_action(
            selected_email, your_name, action_type, gmail_address
        )

        return {
            "status": "success",
            "email_subject": selected_email.get("subject", "No subject"),
            "response": response,
            "action_result": action_result,
            "state": str(state),
        }

    except Exception as e:
        logger.error(f"Error in email processing workflow: {str(e)}")
        return {"status": "error", "message": f"Error processing email: {str(e)}"}


def check_email_status(email_id):
    """Check status of email processing"""
    logger.info(f"Checking status for email ID: {email_id}")

    # This would typically check against a database or state store
    # For now, return a simple status
    return {
        "status": "completed",
        "email_id": email_id,
        "timestamp": "2024-01-01T00:00:00Z",
        "message": "Email processing completed",
    }
