def clean_model_response(response: str) -> str:
    """
    Return only the user-facing part of a model response.
    """

    if not response:
        return "I could not generate a response."

    text = response.strip()

    # Remove common reasoning sections if the model returns them.
    markers = [
        "Final Answer:",
        "Final answer:",
        "Answer:",
    ]

    for marker in markers:
        if marker in text:
            text = text.split(marker, 1)[1].strip()
            break

    return text