import json
from pathlib import Path

from retrieval import retrieve_glitches


TEST_CASES_PATH = Path(__file__).parent / "test_cases.json"


def test_labeled_cases_retrieve_expected_report_and_category():
    with TEST_CASES_PATH.open(encoding="utf-8") as file:
        test_cases = json.load(file)

    for test_case in test_cases:
        case_input = test_case["input"]
        results = retrieve_glitches(
            case_input["description"],
            case_input["game"],
            case_input["platform"],
        )

        assert results, f"{test_case['id']} returned no reports"
        assert results[0]["id"] == test_case["expected_report_id"]
        assert results[0]["category"] == test_case["expected_category"]


def test_unrelated_description_returns_no_reports():
    results = retrieve_glitches(
        "The controller battery indicator has the wrong color.",
        "Example Game",
        "PC",
    )

    assert results == []
