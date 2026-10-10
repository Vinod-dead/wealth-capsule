from pathlib import Path


def test_prompt_explains_missing_categories_carefully():
    prompt_file = (
        Path(__file__).resolve().parents[1]
        / "app"
        / "llm"
        / "nemotron.py"
    )
    source = prompt_file.read_text(encoding="utf-8")

    assert (
        "no transactions for that category were recorded "
        in source
    )
    assert (
        "not proof of zero real-world spending"
        in source
    )