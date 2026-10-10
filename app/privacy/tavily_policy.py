import re


SENSITIVE_PATTERNS = [
    # Currency amounts
    r"₹\s?\d[\d,]*(?:\.\d+)?",
    r"\bINR\s?\d[\d,]*(?:\.\d+)?",
    r"\b\d[\d,]*(?:\.\d+)?\s?(?:rupees|rs)\b",

    # Percentages
   r"\b\d+(?:\.\d+)?\s?(?:%|percent\b|percentage\b)",
    # Email addresses
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",

    # Dates
    r"\b\d{4}-\d{2}-\d{2}\b",
    r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",

    # Account/card-like numbers
    r"\b\d{8,20}\b",
]


def contains_sensitive_data(text: str) -> bool:
    """
    Check whether text contains values that should not
    be sent to Tavily.
    """

    if not isinstance(text, str):
        return True

    for pattern in SENSITIVE_PATTERNS:
        if re.search(pattern, text, flags=re.IGNORECASE):
            return True

    return False


def validate_tavily_query(query: str) -> dict:
    """
    Deterministically decide whether a query is safe
    to send to Tavily.
    """

    if not isinstance(query, str) or not query.strip():
        return {
            "allowed": False,
            "reason": "empty_query",
        }

    query = query.strip()

    if contains_sensitive_data(query):
        return {
            "allowed": False,
            "reason": "sensitive_data_detected",
        }

    return {
        "allowed": True,
        "reason": "policy_passed",
    }