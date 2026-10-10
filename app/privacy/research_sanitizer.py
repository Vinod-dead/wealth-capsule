import re


INSTRUCTION_PATTERNS = [
    r"ignore previous instructions",
    r"ignore all previous instructions",
    r"follow these instructions instead",
    r"system message",
    r"developer message",
    r"reveal your prompt",
    r"reveal the system prompt",
    r"disregard previous instructions",
]


def contains_instruction_like_text(text: str) -> bool:
    """
    Detect common prompt-injection patterns in external
    research content.
    """

    if not isinstance(text, str):
        return True

    for pattern in INSTRUCTION_PATTERNS:
        if re.search(pattern, text, flags=re.IGNORECASE):
            return True

    return False


def sanitize_research_results(
    research_results: list[dict],
) -> list[dict]:
    """
    Treat Tavily results as untrusted external information.

    Instruction-like content is removed from the information
    passed to the language model.
    """

    safe_results = []

    for result in research_results:
        title = result.get("title") or ""
        url = result.get("url") or ""
        content = result.get("content") or ""

        if contains_instruction_like_text(content):
            content = (
                "External source content was filtered because "
                "it contained instruction-like text."
            )

        safe_results.append(
            {
                "title": title,
                "url": url,
                "content": content,
            }
        )

    return safe_results