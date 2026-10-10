from unittest.mock import patch

import pytest

from app.privacy.query_rewriter import build_public_research_query
from app.privacy.tavily_policy import validate_tavily_query
from app.tools.tavily_tool import search_public_knowledge


def test_private_financial_details_are_not_sent_to_tavily():
    user_request = (
        "Why did my spending increase from ₹9300 to ₹14500 "
        "and what current budgeting strategies could help?"
    )

    public_query = build_public_research_query(user_request)

    assert "9300" not in public_query
    assert "14500" not in public_query
    assert "₹" not in public_query

    result = validate_tavily_query(public_query)
    assert result["allowed"] is True


def test_transaction_dates_are_not_sent_to_tavily():
    user_request = (
        "Why did I spend more on 2026-10-05 "
        "and what budgeting strategies could help?"
    )

    public_query = build_public_research_query(user_request)

    assert "2026-10-05" not in public_query
    assert validate_tavily_query(public_query)["allowed"] is True


def test_private_categories_are_not_leaked():
    user_request = (
        "I spent ₹5000 on Shopping and ₹3000 on Food. "
        "What current budgeting strategies could help?"
    )

    public_query = build_public_research_query(user_request)

    assert "5000" not in public_query
    assert "3000" not in public_query
    assert "₹" not in public_query
    assert validate_tavily_query(public_query)["allowed"] is True


def test_sensitive_query_is_blocked_before_tavily_is_called():
    with patch("app.tools.tavily_tool.TavilyClient") as client:
        with pytest.raises(ValueError, match="sensitive_data_detected"):
            search_public_knowledge("reduce spending by ₹10,900")

        client.assert_not_called()