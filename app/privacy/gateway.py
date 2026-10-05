from typing import Any

from app.privacy.sanitizer import sanitize_financial_context
from app.privacy.policy import apply_privacy_policy


def build_safe_context(
    total_spending: float,
    category_totals: dict[str, float],
    previous_total: float | None = None,
) -> dict[str, Any]:
    """
    Build the only financial context allowed to reach
    external AI services.
    """

    sanitized = sanitize_financial_context(
        total_spending=total_spending,
        category_totals=category_totals,
        previous_total=previous_total,
    )

    safe_context = apply_privacy_policy(sanitized)

    return safe_context
