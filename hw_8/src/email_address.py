class EmailAddress:
    """Email address with validation and masking capabilities."""

    VALID_DOMAINS = (".com", ".ru", ".net")

    def __init__(self, address: str):
        """
        Initialize EmailAddress with validation.

        Args:
            address: Email address string

        Raises:
            ValueError: If email address is invalid
        """
        self._address = self.normalize_address(address)
        if not self._check_correct_email():
            raise ValueError(f"Invalid email address: {address}")

    @staticmethod
    def normalize_address(address: str) -> str:
        """
        Normalize email address to lowercase and strip whitespace.

        Args:
            address: Email address to normalize

        Returns:
            Normalized email address
        """
        return address.strip().lower()

    def _check_correct_email(self) -> bool:
        """
        Validate email address format.

        Returns:
            True if email is valid, False otherwise
        """
        if not self._address or "@" not in self._address:
            return False

        parts = self._address.split("@")
        if len(parts) != 2:
            return False

        login, domain = parts
        if not login or not domain:
            return False

        if not domain.endswith(self.VALID_DOMAINS):
            return False

        for valid_domain in self.VALID_DOMAINS:
            if domain.endswith(valid_domain):
                domain_without_zone = domain[: -len(valid_domain)]
                if domain_without_zone:
                    return True

        return False

    @property
    def address(self) -> str:
        """Get normalized email address."""
        return self._address

    @property
    def masked(self) -> str:
        """
        Get masked email address (first 2 chars + '***@' + domain).

        Returns:
            Masked email address
        """
        login, domain = self._address.split("@")
        return f"{login[:2]}***@{domain}"

    def __str__(self) -> str:
        """String representation of email address."""
        return self._address

    def __repr__(self) -> str:
        """Detailed representation of email address."""
        return f"EmailAddress('{self._address}')"

    def __eq__(self, other) -> bool:
        """Check equality with another EmailAddress."""
        if isinstance(other, EmailAddress):
            return self._address == other._address
        return False

    def __hash__(self) -> int:
        """Hash function for using in sets and dicts."""
        return hash(self._address)
