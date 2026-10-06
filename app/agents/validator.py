import re
from urllib.parse import urlparse


def extract_rupee_amounts(text: str) -> list[float]:
    """
    Extract INR amounts such as ₹5,750 or ₹300.
    """

    if not isinstance(text, str):
        return []

    matches = re.findall(
        r"₹\s?([\d,]+(?:\.\d+)?)",
        text,
    )

    return [
        float(value.replace(",", ""))
        for value in matches
    ]


def extract_percentages(text: str) -> list[float]:
    """
    Extract percentages such as 39.79%.
    """

    if not isinstance(text, str):
        return []

    matches = re.findall(
        r"(\d+(?:\.\d+)?)\s?%",
        text,
    )

    return [float(value) for value in matches]


def validate_financial_numbers(
    answer: str,
    safe_context: dict,
) -> dict:
    """
    Verify that important financial values in the
    model answer match locally calculated values.
    """

    expected_amounts = []

    if safe_context.get("change") is not None:
        expected_amounts.append(
            round(abs(float(safe_context["change"])), 2)
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

    amount_checks = []

    for expected in expected_amounts:
        amount_checks.append(
            any(
                abs(actual - expected) < 0.01
                for actual in actual_amounts
            )
        )

    percentage_checks = []

    for expected in expected_percentages:
        percentage_checks.append(
            any(
                abs(actual - expected) < 0.01
                for actual in actual_percentages
            )
        )

    numbers_valid = all(amount_checks) and all(
        percentage_checks
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
    """
    Verify that URLs appearing in the answer came from
    the Tavily results used for this request.
    """

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
    """
    Run all deterministic validation checks.
    """

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