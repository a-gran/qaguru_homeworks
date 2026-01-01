import os
from datetime import date

import pytest

from src.email import Email
from src.email_address import EmailAddress
from src.service import EmailService, LoggingEmailService
from src.status import Status


class TestEmailAddress:
    """Tests for EmailAddress class."""

    def test_valid_email_creation(self):
        """Test creating valid email addresses."""
        email = EmailAddress("user@example.com")
        assert email.address == "user@example.com"

    def test_email_normalization(self):
        """Test email normalization (lowercase and strip)."""
        email = EmailAddress("  User@Example.COM  ")
        assert email.address == "user@example.com"

    def test_invalid_email_no_at(self):
        """Test invalid email without @ symbol."""
        with pytest.raises(ValueError):
            EmailAddress("userexample.com")

    def test_invalid_email_wrong_domain(self):
        """Test invalid email with wrong domain."""
        with pytest.raises(ValueError):
            EmailAddress("user@example.org")

    def test_masked_email(self):
        """Test masked email property."""
        email = EmailAddress("alice@example.com")
        assert email.masked == "al***@example.com"

    def test_valid_domains(self):
        """Test all valid domain extensions."""
        valid_emails = [
            "user@example.com",
            "user@example.ru",
            "user@example.net",
        ]
        for email_str in valid_emails:
            email = EmailAddress(email_str)
            assert email.address == email_str


class TestEmail:
    """Tests for Email dataclass."""

    def test_email_creation_single_recipient(self):
        """Test creating email with single recipient."""
        sender = EmailAddress("alice@example.com")
        recipient = EmailAddress("bob@example.com")
        email = Email(
            subject="Test",
            body="Hello",
            sender=sender,
            recipients=recipient,
        )
        assert len(email.recipients) == 1
        assert email.recipients[0] == recipient

    def test_email_creation_multiple_recipients(self):
        """Test creating email with multiple recipients."""
        sender = EmailAddress("alice@example.com")
        recipients = [
            EmailAddress("bob@example.com"),
            EmailAddress("charlie@example.ru"),
        ]
        email = Email(
            subject="Test",
            body="Hello",
            sender=sender,
            recipients=recipients,
        )
        assert len(email.recipients) == 2

    def test_get_recipients_str(self):
        """Test getting recipients as comma-separated string."""
        sender = EmailAddress("alice@example.com")
        recipients = [
            EmailAddress("bob@example.com"),
            EmailAddress("charlie@example.ru"),
        ]
        email = Email(
            subject="Test",
            body="Hello",
            sender=sender,
            recipients=recipients,
        )
        assert email.get_recipients_str() == "bob@example.com, charlie@example.ru"

    def test_clean_data(self):
        """Test cleaning email data."""
        sender = EmailAddress("alice@example.com")
        recipient = EmailAddress("bob@example.com")
        email = Email(
            subject="Test\n\tSubject",
            body="Hello\n\tWorld",
            sender=sender,
            recipients=recipient,
        )
        email.clean_data()
        assert email.subject == "Test Subject"
        assert email.body == "Hello World"

    def test_add_short_body(self):
        """Test adding short body."""
        sender = EmailAddress("alice@example.com")
        recipient = EmailAddress("bob@example.com")
        email = Email(
            subject="Test",
            body="This is a long message",
            sender=sender,
            recipients=recipient,
        )
        email.add_short_body(10)
        assert email.short_body == "This is a ..."

    def test_is_valid_fields_valid(self):
        """Test field validation with valid data."""
        sender = EmailAddress("alice@example.com")
        recipient = EmailAddress("bob@example.com")
        email = Email(
            subject="Test",
            body="Hello",
            sender=sender,
            recipients=recipient,
        )
        assert email.is_valid_fields() is True

    def test_is_valid_fields_empty_subject(self):
        """Test field validation with empty subject."""
        sender = EmailAddress("alice@example.com")
        recipient = EmailAddress("bob@example.com")
        email = Email(
            subject="",
            body="Hello",
            sender=sender,
            recipients=recipient,
        )
        assert email.is_valid_fields() is False

    def test_prepare_valid_email(self):
        """Test preparing valid email."""
        sender = EmailAddress("alice@example.com")
        recipient = EmailAddress("bob@example.com")
        email = Email(
            subject="Test\n\tSubject",
            body="Hello\n\tWorld",
            sender=sender,
            recipients=recipient,
        )
        email.prepare()
        assert email.status == Status.READY
        assert email.subject == "Test Subject"
        assert email.short_body is not None

    def test_prepare_invalid_email(self):
        """Test preparing invalid email."""
        sender = EmailAddress("alice@example.com")
        recipient = EmailAddress("bob@example.com")
        email = Email(
            subject="",
            body="Hello",
            sender=sender,
            recipients=recipient,
        )
        email.prepare()
        assert email.status == Status.INVALID


class TestEmailService:
    """Tests for EmailService class."""

    def test_add_send_date(self):
        """Test getting current date."""
        service = EmailService()
        send_date = service.add_send_date()
        assert send_date == date.today().isoformat()

    def test_send_email_single_recipient(self):
        """Test sending email to single recipient."""
        service = EmailService()
        sender = EmailAddress("alice@example.com")
        recipient = EmailAddress("bob@example.com")
        email = Email(
            subject="Test",
            body="Hello",
            sender=sender,
            recipients=recipient,
            status=Status.READY,
        )

        sent_emails = service.send_email(email)

        assert len(sent_emails) == 1
        assert sent_emails[0].status == Status.SENT
        assert sent_emails[0].date is not None
        assert email.status == Status.READY
        assert email.date is None

    def test_send_email_multiple_recipients(self):
        """Test sending email to multiple recipients."""
        service = EmailService()
        sender = EmailAddress("alice@example.com")
        recipients = [
            EmailAddress("bob@example.com"),
            EmailAddress("charlie@example.ru"),
        ]
        email = Email(
            subject="Test",
            body="Hello",
            sender=sender,
            recipients=recipients,
            status=Status.READY,
        )

        sent_emails = service.send_email(email)

        assert len(sent_emails) == 2
        assert all(e.status == Status.SENT for e in sent_emails)
        assert all(e.date is not None for e in sent_emails)
        assert email.recipients == recipients

    def test_send_email_not_ready(self):
        """Test sending email that is not ready."""
        service = EmailService()
        sender = EmailAddress("alice@example.com")
        recipient = EmailAddress("bob@example.com")
        email = Email(
            subject="Test",
            body="Hello",
            sender=sender,
            recipients=recipient,
            status=Status.DRAFT,
        )

        sent_emails = service.send_email(email)

        assert len(sent_emails) == 1
        assert sent_emails[0].status == Status.FAILED


class TestLoggingEmailService:
    """Tests for LoggingEmailService class."""

    def test_logging_email_service(self, tmp_path):
        """Test logging email service."""
        log_file = tmp_path / "test_send.log"
        service = LoggingEmailService(str(log_file))

        sender = EmailAddress("alice@example.com")
        recipient = EmailAddress("bob@example.com")
        email = Email(
            subject="Test",
            body="Hello",
            sender=sender,
            recipients=recipient,
            status=Status.READY,
        )

        sent_emails = service.send_email(email)

        assert len(sent_emails) == 1
        assert log_file.exists()

        log_content = log_file.read_text(encoding="utf-8")
        assert "alice@example.com" in log_content
        assert "bob@example.com" in log_content
        assert "Test" in log_content
        assert Status.SENT in log_content

    def test_cleanup_log_file(self):
        """Clean up log file after tests."""
        log_file = "send.log"
        if os.path.exists(log_file):
            os.remove(log_file)
