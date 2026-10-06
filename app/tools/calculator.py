def calculate(expression: str) -> float:
    """
    Safely evaluate basic arithmetic expressions.

    Allowed:
    +, -, *, /, %, **, parentheses, and numbers.
    """

    if not isinstance(expression, str) or not expression.strip():
        raise ValueError("Expression must be a non-empty string.")

    allowed = set("0123456789+-*/%.() ")

    if any(character not in allowed for character in expression):
        raise ValueError("Expression contains unsupported characters.")

    try:
        result = eval(expression, {"__builtins__": {}}, {})
    except Exception as exc:
        raise ValueError("Invalid arithmetic expression.") from exc

    if not isinstance(result, (int, float)):
        raise ValueError("Expression did not produce a number.")

    return round(float(result), 2)