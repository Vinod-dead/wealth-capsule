
def clean_model_response(response: str) -> str:
    """Return clean, user-facing model text."""
    if not response:
        return "I could not generate a response."

    text = response.strip()

    markers = ["Final Answer:", "Final answer:", "Answer:"]
    for marker in markers:
        if marker in text:
            text = text.split(marker, 1)[1].strip()
            break

    # Repair common mojibake using explicit Unicode code points.
    rupee = "\u20b9"
    text = text.replace("\u00e2\u00b9", rupee)
    text = text.replace("\u00e2\u201a\u00b9", rupee)

    return text
