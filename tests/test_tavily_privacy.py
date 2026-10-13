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
        
def test_comma_formatted_financial_amounts_are_blocked_before_tavily_is_called():
    query = "Expenses of 29,500 and food spending of 10,950"

    with patch("app.tools.tavily_tool.TavilyClient") as client:
        with pytest.raises(ValueError, match="sensitive_data_detected"):
            search_public_knowledge(query)

        client.assert_not_called()
def test_rewritten_financial_request_sends_only_generic_query_to_tavily(monkeypatch):
    from unittest.mock import patch
    from app.privacy.query_rewriter import build_public_research_query
    from app.tools.tavily_tool import search_public_knowledge

    private_request = (
        "Research how to manage a monthly expense of 29,500, "
        "with 10,950 spent on food."
    )

    safe_query = build_public_research_query(private_request)

    monkeypatch.setenv("TAVILY_API_KEY", "test-key")

    with patch("app.tools.tavily_tool.TavilyClient") as mock_client:
        mock_client.return_value.search.return_value = {"results": []}

        search_public_knowledge(safe_query)

        mock_client.return_value.search.assert_called_once()
        actual_query = mock_client.return_value.search.call_args.kwargs["query"]

        assert actual_query == safe_query
        assert "29,500" not in actual_query
        assert "10,950" not in actual_query


def test_sensitive_query_never_calls_tavily_client(monkeypatch):
    from unittest.mock import patch
    from app.tools.tavily_tool import search_public_knowledge
    import pytest

    monkeypatch.setenv("TAVILY_API_KEY", "test-key")

    private_query = "Research expenses of 29,500 and food spending of 10,950"

    with patch("app.tools.tavily_tool.TavilyClient") as mock_client:
        with pytest.raises(ValueError, match="sensitive_data_detected"):
            search_public_knowledge(private_query)

        mock_client.assert_not_called()
