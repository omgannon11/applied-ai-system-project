"""Local keyword retrieval for synthetic glitch demonstration reports."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


DEFAULT_KNOWLEDGE_BASE = Path(__file__).parent / "data" / "glitch_reports.json"
TOKEN_PATTERN = re.compile(r"[a-z0-9]+")
STOP_WORDS = {
    "a",
    "after",
    "an",
    "and",
    "are",
    "at",
    "before",
    "but",
    "for",
    "from",
    "game",
    "in",
    "is",
    "it",
    "my",
    "of",
    "on",
    "or",
    "the",
    "to",
    "when",
    "with",
}


def _tokens(value: str) -> set[str]:
    """Normalize text into a set of lowercase search tokens."""
    return set(TOKEN_PATTERN.findall(value.lower())) - STOP_WORDS


def load_glitch_reports(path: str | Path = DEFAULT_KNOWLEDGE_BASE) -> list[dict[str, Any]]:
    """Load and minimally validate the local glitch-report knowledge base."""
    knowledge_base_path = Path(path)
    try:
        with knowledge_base_path.open(encoding="utf-8") as file:
            reports = json.load(file)
    except FileNotFoundError as exc:
        raise ValueError(f"Knowledge base not found: {knowledge_base_path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Knowledge base contains invalid JSON: {knowledge_base_path}") from exc

    if not isinstance(reports, list):
        raise ValueError("Knowledge base must contain a JSON list of reports.")

    required_fields = {
        "id",
        "game",
        "platform",
        "category",
        "symptoms",
        "possible_causes",
        "recommended_steps",
        "source",
    }
    for index, report in enumerate(reports):
        if not isinstance(report, dict) or not required_fields.issubset(report):
            raise ValueError(f"Knowledge-base report at index {index} is missing required fields.")
    return reports


def _searchable_text(report: dict[str, Any]) -> str:
    fields = [
        report["game"],
        report["platform"],
        report["category"],
        *report["symptoms"],
        *report["possible_causes"],
        *report["recommended_steps"],
    ]
    return " ".join(str(field) for field in fields)


def retrieve_glitches(
    user_description: str,
    game: str,
    platform: str,
    *,
    top_k: int = 3,
    knowledge_base_path: str | Path = DEFAULT_KNOWLEDGE_BASE,
) -> list[dict[str, Any]]:
    """Return up to ``top_k`` local reports ranked by keyword relevance.

    Game and platform matches receive small bonuses. Reports with no matching
    description, game, or platform terms are omitted so callers can clearly
    distinguish a no-match result.
    """
    if not all(isinstance(value, str) for value in (user_description, game, platform)):
        raise TypeError("Description, game, and platform must be strings.")
    if top_k < 1:
        raise ValueError("top_k must be at least 1.")

    description_tokens = _tokens(user_description)
    game_tokens = _tokens(game)
    platform_tokens = _tokens(platform)
    query_tokens = description_tokens | game_tokens | platform_tokens
    if not query_tokens:
        return []

    ranked: list[tuple[float, dict[str, Any]]] = []
    for report in load_glitch_reports(knowledge_base_path):
        report_tokens = _tokens(_searchable_text(report))
        overlap = len(description_tokens & report_tokens)
        score = float(overlap)

        if game.strip() and game.casefold() == str(report["game"]).casefold():
            score += 2.0
        if platform.strip() and platform.casefold() == str(report["platform"]).casefold():
            score += 1.0

        # Metadata improves ranking, but it cannot create a match by itself.
        if overlap > 0:
            result = dict(report)
            result["relevance_score"] = score
            ranked.append((score, result))

    ranked.sort(key=lambda item: (-item[0], item[1]["id"]))
    return [report for _, report in ranked[:top_k]]
