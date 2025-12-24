from __future__ import annotations

from typing import List, Dict

# NOTE:
# This is intentionally a stub. For a real project, plug in:
# - SerpAPI / Bing Web Search / Tavily / Exa / etc.
# and return structured results (title, url, snippet).
#
# For now we return placeholder "results" so the workflow runs end-to-end.


def search_web(query: str, k: int = 5) -> List[Dict[str, str]]:
    return [
        {"title": f"Placeholder result {i+1} for: {query}", "url": f"https://example.com/{i+1}", "snippet": "Replace this with real web search."}
        for i in range(k)
    ]
