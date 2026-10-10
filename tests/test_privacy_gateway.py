from app.privacy.tavily_policy import validate_tavily_query


def test_allows_public_research_query():
    result = validate_tavily_query(
        "current strategies for reducing discretionary spending"
    )

    assert result["allowed"] is True
    assert result["reason"] == "policy_passed"


def test_blocks_rupee_amount():
    result = validate_tavily_query(
        "How can I reduce my spending of ₹9300?"
    )

    assert result["allowed"] is False
    assert result["reason"] == "sensitive_data_detected"


def test_blocks_percentage():
    result = validate_tavily_query(
        "My spending changed by 53.96 percent. What should I do?"
    )

    assert result["allowed"] is False
    assert result["reason"] == "sensitive_data_detected"


def test_blocks_date():
    result = validate_tavily_query(
        "What happened with my spending on 2026-10-05?"
    )

    assert result["allowed"] is False
    assert result["reason"] == "sensitive_data_detected"


def test_blocks_email():
    result = validate_tavily_query(
        "Please research vinod@example.com budgeting"
    )

    assert result["allowed"] is False
    assert result["reason"] == "sensitive_data_detected"


def test_blocks_account_like_number():
    result = validate_tavily_query(
        "Research budgeting for account 123456789012"
    )

    assert result["allowed"] is False
    assert result["reason"] == "sensitive_data_detected"