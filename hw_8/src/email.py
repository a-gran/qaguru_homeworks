from dataclasses import dataclass, field
from typing import Optional

from .email_address import EmailAddress
from .status import Status
from .utils import clean_text


@dataclass
class Email:
    """Email message with validation and preparation capabilities."""

    subject: str
    body: str
    sender: EmailAddress
    recipients: list[EmailAddress] = field(default_factory=list)
    date: Optional[str] = None
    short_body: Optional[str] = None
    status: Status = Status.DRAFT

    def __post_init__(self):
        """Ensure recipients is always a list."""
        if isinstance(self.recipients, EmailAddress):
            self.recipients = [self.recipients]
        elif not isinstance(self.recipients, list):
            self.recipients = list(self.recipients)

    def get_recipients_str(self) -> str:
        """
        Get comma-separated string of recipient addresses.

        Returns:
            Comma-separated recipient addresses
        """
        return ", ".join(recipient.address for recipient in self.recipients)

    def clean_data(self) -> "Email":
        """
        Clean subject and body text.

        Returns:
            Self for method chaining
        """
        self.subject = clean_text(self.subject)
        self.body = clean_text(self.body)
        return self

    def add_short_body(self, n: int = 10) -> "Email":
        """
        Add shortened body version (first n characters + '...').

        Args:
            n: Number of characters to include

        Returns:
            Self for method chaining
        """
        if len(self.body) > n:
            self.short_body = self.body[:n] + "..."
        else:
            self.short_body = self.body
        return self

    def is_valid_fields(self) -> bool:
        """
        Check if all required fields are non-empty.

        Returns:
            True if subject, body, sender, and recipients are valid
        """
        return bool(
            self.subject.strip()
            and self.body.strip()
            and self.sender
            and self.recipients
        )

    def prepare(self) -> "Email":
        """
        Prepare email for sending: clean data, validate, set status.

        Returns:
            Self for method chaining
        """
        self.clean_data()
        self.add_short_body()

        if self.is_valid_fields():
            self.status = Status.READY
        else:
            self.status = Status.INVALID

        return self

    def __str__(self) -> str:
        """
        String representation using masked sender and recipient list.

        Returns:
            Formatted email string
        """
        return (
            f"Email(subject='{self.subject}', "
            f"from={self.sender.masked}, "
            f"to=[{self.get_recipients_str()}], "
            f"status={self.status})"
        )
