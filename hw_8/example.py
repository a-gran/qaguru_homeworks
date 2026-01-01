"""
Demonstration of the Email System.
"""

from src.email import Email
from src.email_address import EmailAddress
from src.service import EmailService, LoggingEmailService
from src.status import Status


def demo_basic_usage():
    """Demonstrate basic email system usage."""
    print("=" * 60)
    print("DEMO: Basic Email System Usage")
    print("=" * 60)

    # Create email addresses
    sender = EmailAddress("alice@example.com")
    recipient1 = EmailAddress("bob@example.com")
    recipient2 = EmailAddress("charlie@example.ru")

    print(f"\nSender: {sender.address}")
    print(f"Masked sender: {sender.masked}")
    print(f"Recipients: {recipient1.address}, {recipient2.address}")

    # Create email
    email = Email(
        subject="Quarterly Report",
        body="Hello team,\n\tHere is the quarterly report.",
        sender=sender,
        recipients=[recipient1, recipient2],
    )

    print(f"\nOriginal email status: {email.status}")
    print(f"Original email: {email}")

    # Prepare email
    email.prepare()
    print(f"\nAfter prepare:")
    print(f"  Status: {email.status}")
    print(f"  Subject: '{email.subject}'")
    print(f"  Body: '{email.body}'")
    print(f"  Short body: '{email.short_body}'")

    # Send email
    service = EmailService()
    sent_emails = service.send_email(email)

    print(f"\nSent {len(sent_emails)} emails:")
    for sent_email in sent_emails:
        recipient = (
            sent_email.recipients[0].address
            if sent_email.recipients
            else "unknown"
        )
        print(f"  To: {recipient}")
        print(f"  Date: {sent_email.date}")
        print(f"  Status: {sent_email.status}")

    # Verify original email is unchanged
    print(f"\nOriginal email unchanged:")
    print(f"  Date: {email.date}")
    print(f"  Status: {email.status}")
    print(f"  Recipients count: {len(email.recipients)}")


def demo_invalid_email():
    """Demonstrate handling invalid email."""
    print("\n" + "=" * 60)
    print("DEMO: Invalid Email Handling")
    print("=" * 60)

    sender = EmailAddress("alice@example.com")
    recipient = EmailAddress("bob@example.com")

    # Email with empty subject
    email = Email(
        subject="",
        body="Hello",
        sender=sender,
        recipients=recipient,
    )

    email.prepare()
    print(f"\nEmail with empty subject:")
    print(f"  Status: {email.status}")

    # Try to send
    service = EmailService()
    sent_emails = service.send_email(email)

    print(f"\nSent emails:")
    for sent_email in sent_emails:
        print(f"  Status: {sent_email.status}")


def demo_invalid_email_address():
    """Demonstrate invalid email address handling."""
    print("\n" + "=" * 60)
    print("DEMO: Invalid Email Address")
    print("=" * 60)

    invalid_addresses = [
        "userexample.com",
        "user@example.org",
        "@example.com",
        "user@.com",
    ]

    for address in invalid_addresses:
        try:
            EmailAddress(address)
            print(f"  {address} - SHOULD HAVE FAILED!")
        except ValueError as e:
            print(f"  {address} - Rejected: {e}")


def demo_logging_service():
    """Demonstrate logging email service."""
    print("\n" + "=" * 60)
    print("DEMO: Logging Email Service")
    print("=" * 60)

    sender = EmailAddress("alice@example.com")
    recipients = [
        EmailAddress("bob@example.com"),
        EmailAddress("charlie@example.ru"),
    ]

    email = Email(
        subject="Test Email",
        body="This is a test",
        sender=sender,
        recipients=recipients,
        status=Status.READY,
    )

    # Send with logging
    service = LoggingEmailService("demo_send.log")
    sent_emails = service.send_email(email)

    print(f"\nSent {len(sent_emails)} emails with logging")
    print("Check demo_send.log for details")

    # Read and display log
    with open("demo_send.log", "r", encoding="utf-8") as f:
        print("\nLog contents:")
        print(f.read())


def main():
    """Run all demonstrations."""
    demo_basic_usage()
    demo_invalid_email()
    demo_invalid_email_address()
    demo_logging_service()

    print("\n" + "=" * 60)
    print("All demonstrations completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
