def clean_text(text: str) -> str:
    """
    Replace tabs and newlines with spaces, trim excess whitespace.

    Args:
        text: Text to clean

    Returns:
        Cleaned text with normalized whitespace
    """
    return " ".join(text.split())
