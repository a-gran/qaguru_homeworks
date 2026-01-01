from copy import deepcopy
from datetime import date

from .email import Email
from .status import Status


class EmailService:
    """Service for sending emails."""

    @staticmethod
    def add_send_date() -> str:
        """
        Get current date in YYYY-MM-DD format.

        Returns:
            Current date as ISO format string
        """
        return date.today().isoformat()

    def send_email(self, email: Email) -> list[Email]:
        """
        Send email to all recipients.

        Creates a deep copy of the email for each recipient,
        sets the send date, and updates status based on preparation.
        Original email is not modified.

        Args:
            email: Email to send

        Returns:
            List of sent emails (one per recipient)
        """
        sent_emails = []

        for recipient in email.recipients:
            email_copy = deepcopy(email)
            email_copy.recipients = [recipient]
            email_copy.date = self.add_send_date()

            if email.status == Status.READY:
                email_copy.status = Status.SENT
            else:
                email_copy.status = Status.FAILED

            sent_emails.append(email_copy)

        return sent_emails


class LoggingEmailService(EmailService):
    """Email service with logging capabilities."""

    def __init__(self, log_file: str = "send.log"):
        """
        Initialize logging email service.

        Args:
            log_file: Path to log file
        """
        self.log_file = log_file

    def send_email(self, email: Email) -> list[Email]:
        """
        Send email with logging.

        Args:
            email: Email to send

        Returns:
            List of sent emails (one per recipient)
        """
        sent_emails = super().send_email(email)

        with open(self.log_file, "a", encoding="utf-8") as f:
            for sent_email in sent_emails:
                recipient = (
                    sent_email.recipients[0].address
                    if sent_email.recipients
                    else "unknown"
                )
                log_entry = (
                    f"Date: {sent_email.date}, "
                    f"From: {sent_email.sender.address}, "
                    f"To: {recipient}, "
                    f"Subject: {sent_email.subject}, "
                    f"Status: {sent_email.status}\n"
                )
                f.write(log_entry)

        return sent_emails
