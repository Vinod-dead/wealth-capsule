import re


def extract_rupee_amounts(text: str) -> list[float]:
    """
    Extract INR amounts written as:
    ₹10,900
    INR 10,900
    10,900 INR
    10,900 rupees
    """

    if not isinstance(text, str):
        return []

    patterns = [
        r"₹\s*([0-9][0-9,]*(?:\.[0-9]+)?)",
        r"\bINR\s*([0-9][0-9,]*(?:\.[0-9]+)?)",
        r"\b([0-9][0-9,]*(?:\.[0-9]+)?)\s*INR\b",
        r"\b([0-9][0-9,]*(?:\.[0-9]+)?)\s*rupees\b",
    ]

    amounts = []

    for pattern in patterns:
        matches = re.findall(
            pattern,
            text,
            flags=re.IGNORECASE,
        )

        for value in matches:
            try:
                amounts.append(
                    float(value.replace(",", ""))
                )
            except (ValueError, AttributeError):
                pass

    return amounts


def extract_percentages(text: str) -> list[float]:
    """
    Extract percentages such as 53.96%.
    """

    if not isinstance(text, str):
        return []

    matches = re.findall(
        r"([0-9]+(?:\.[0-9]+)?)\s?%",
        text,
    )

    return [
        float(value)
        for value in matches
    ]


def validate_financial_numbers(
    answer: str,
    safe_context: dict,
) -> dict:

    expected_amounts = []

    if safe_context.get("change") is not None:
        expected_amounts.append(
            round(
                abs(float(safe_context["change"])),
                2,
            )
        )

    expected_percentages = []

    if safe_context.get("percentage_change") is not None:
        expected_percentages.append(
            round(
                abs(float(safe_context["percentage_change"])),
                2,
            )
        )

    actual_amounts = extract_rupee_amounts(answer)
    actual_percentages = extract_percentages(answer)

    amount_checks = [
        any(
            abs(actual - expected) < 0.01
            for actual in actual_amounts
        )
        for expected in expected_amounts
    ]

    percentage_checks = [
        any(
            abs(actual - expected) < 0.01
            for actual in actual_percentages
        )
        for expected in expected_percentages
    ]

    numbers_valid = (
        all(amount_checks)
        and all(percentage_checks)
    )

    return {
        "valid": numbers_valid,
        "expected_amounts": expected_amounts,
        "actual_amounts": actual_amounts,
        "expected_percentages": expected_percentages,
        "actual_percentages": actual_percentages,
        "amount_checks": amount_checks,
        "percentage_checks": percentage_checks,
    }


def validate_source_urls(
    answer: str,
    research_results: list[dict],
) -> dict:

    returned_urls = {
        result.get("url")
        for result in research_results
        if result.get("url")
    }

    answer_urls = set(
        re.findall(
            r"https?://[^\s)]+",
            answer or "",
        )
    )

    valid_urls = []
    invalid_urls = []

    for url in answer_urls:
        cleaned_url = url.rstrip(".,;")

        if cleaned_url in returned_urls:
            valid_urls.append(cleaned_url)
        else:
            invalid_urls.append(cleaned_url)

    return {
        "valid": len(invalid_urls) == 0,
        "returned_urls": sorted(returned_urls),
        "answer_urls": sorted(answer_urls),
        "valid_urls": sorted(valid_urls),
        "invalid_urls": sorted(invalid_urls),
    }


def validate_answer(
    answer: str,
    safe_context: dict,
    research_results: list[dict] | None = None,
) -> dict:

    research_results = research_results or []

    financial_check = validate_financial_numbers(
        answer,
        safe_context,
    )

    source_check = validate_source_urls(
        answer,
        research_results,
    )

    return {
        "valid": (
            financial_check["valid"]
            and source_check["valid"]
        ),
        "financial_numbers": financial_check,
        "sources": source_check,
    }