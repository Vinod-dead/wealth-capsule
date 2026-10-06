ALLOWED_MODEL_FIELDS = {
    "total_spending",
    "category_totals",
    "previous_total",
    "change",
    "percentage_change",
    "category_changes",
}


def apply_privacy_policy(context: dict) -> dict:
    """
    Allow only approved aggregated fields to leave
    the private data environment.
    """

    return {
        key: value
        for key, value in context.items()
        if key in ALLOWED_MODEL_FIELDS
    }