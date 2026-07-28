import hashlib
import re
import secrets


def hash_password(plain_password: str) -> str:
    """Hash a password using SHA-256 with a random salt.

    Returns a string in the format 'salt:hash'.
    """
    salt = secrets.token_hex(32)
    hash_value = hashlib.sha256((salt + plain_password).encode()).hexdigest()
    return f"{salt}:{hash_value}"


def verify_password(plain_password: str, stored_hash: str) -> bool:
    """Verify a plain password against a stored 'salt:hash' string."""
    try:
        salt, original_hash = stored_hash.split(":", 1)
        new_hash = hashlib.sha256((salt + plain_password).encode()).hexdigest()
        return secrets.compare_digest(new_hash, original_hash)
    except ValueError:
        return False


def validate_password_complexity(password: str) -> tuple[bool, str]:
    """Validate password complexity rules.

    Rules: minimum 8 characters, at least one uppercase letter,
    one lowercase letter, and one digit.

    Returns a tuple of (is_valid: bool, error_message: str).
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."
    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."
    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one digit."
    return True, ""


def validate_email(email: str) -> bool:
    """Validate email format using a standard regex pattern."""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))
