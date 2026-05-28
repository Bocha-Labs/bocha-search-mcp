import json
import os
from collections.abc import Iterable

import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()

BOCHA_WEB_SEARCH_ENDPOINT = "https://api.bocha.cn/v1/web-search?utm_source=bocha-mcp-local"
BOCHA_AI_SEARCH_ENDPOINT = "https://api.bocha.cn/v1/ai-search?utm_source=bocha-mcp-local"
DEFAULT_TIMEOUT = 10.0
VALID_FRESHNESS_VALUES = {
    "noLimit",
    "oneYear",
    "oneMonth",
    "oneWeek",
    "oneDay",
}


SERVER_INSTRUCTIONS = """
Bocha Search MCP Server provides two tools for real-time web search and semantic AI search.

Available tools:
- bocha_web_search: General web search with title, URL, description(snippets, summary), published date, and site name.
- bocha_ai_search: Semantic search with structured cards and richer vertical-domain results.

Usage notes:
- Use bocha_web_search for standard web retrieval and citations.
- Use bocha_ai_search when semantic retrieval or structured results are preferred.
- bocha_ai_search may require separate API access permission.

If the API key is missing, invalid, or lacks permission, return the upstream error message clearly.
"""


server = FastMCP("Bocha Search", instructions=SERVER_INSTRUCTIONS)


def _validate_count(count: int) -> None:
    if not 1 <= count <= 50:
        raise ValueError("count must be between 1 and 50")


def _validate_freshness(freshness: str) -> None:
    if not freshness:
        raise ValueError("freshness cannot be empty")

    if freshness in VALID_FRESHNESS_VALUES:
        return

    is_single_date = len(freshness) == 10 and freshness.count("-") == 2
    is_date_range = (
        ".." in freshness
        and len(freshness.split("..")) == 2
        and all(len(part) == 10 and part.count("-") == 2 for part in freshness.split(".."))
    )

    if is_single_date or is_date_range:
        return

    raise ValueError(
        "freshness must be one of: YYYY-MM-DD, YYYY-MM-DD..YYYY-MM-DD, "
        "noLimit, oneYear, oneMonth, oneWeek, oneDay"
    )


def _get_api_key() -> str:
    api_key = os.environ.get("BOCHA_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError(
            "Bocha API key is not configured. Please set the BOCHA_API_KEY environment variable."
        )
    return api_key


def _format_web_result(result: dict) -> str:
    return "\n".join(
        [
            f"Title: {result.get('name', '')}",
            f"URL: {result.get('url', '')}",
            f"Description: {result.get('summary', '')}",
            f"Published date: {result.get('datePublished', '')}",
            f"Site name: {result.get('siteName', '')}",
        ]
    )


def _safe_parse_json(text: str) -> dict:
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        return {}

    return parsed if isinstance(parsed, dict) else {}


async def _post_json(endpoint: str, payload: dict) -> dict:
    headers = {
        "Authorization": f"Bearer {_get_api_key()}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            endpoint,
            headers=headers,
            json=payload,
            timeout=DEFAULT_TIMEOUT,
        )
        response.raise_for_status()
        return response.json()


def _join_results(results: Iterable[str]) -> str:
    items = [item for item in results if item]
    return "\n\n".join(items) if items else "No results found."


@server.tool()
async def bocha_web_search(
    query: str, freshness: str = "noLimit", count: int = 10
) -> str:
    """Search with Bocha Web Search and get enhanced search details from billions of web documents,
    including page titles, urls, summaries, site names, site icons, publication dates, image links, and more.

    Args:
        query: Search query (required)
        freshness: The time range for the search results. (Available options YYYY-MM-DD, YYYY-MM-DD..YYYY-MM-DD, noLimit, oneYear, oneMonth, oneWeek, oneDay. Default is noLimit)
        count: Number of results (1-50, default 10)
    """
    try:
        _validate_freshness(freshness)
        _validate_count(count)

        payload = {
            "query": query,
            "summary": True,
            "freshness": freshness,
            "count": count,
        }

        response = await _post_json(BOCHA_WEB_SEARCH_ENDPOINT, payload)
        data = response.get("data", {})
        web_pages = data.get("webPages", {})
        items = web_pages.get("value", [])

        return _join_results(_format_web_result(item) for item in items if isinstance(item, dict))
    except ValueError as e:
        return f"Invalid input: {e}"
    except RuntimeError as e:
        return f"Error: {e}"
    except httpx.HTTPStatusError as e:
        return (
            "Bocha Web Search API HTTP error occurred: "
            f"{e.response.status_code} - {e.response.text}"
        )
    except httpx.RequestError as e:
        return f"Error communicating with Bocha Web Search API: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"


@server.tool()
async def bocha_ai_search(
    query: str, freshness: str = "noLimit", count: int = 10
) -> str:
    """Search with Bocha AI Search, recognizes the semantics of search terms
    and additionally returns structured modal cards with content from vertical domains.

    Args:
        query: Search query (required)
        freshness: The time range for the search results. (Available options noLimit, oneYear, oneMonth, oneWeek, oneDay. Default is noLimit)
        count: Number of results (1-50, default 10)
    """
    try:
        _validate_freshness(freshness)
        _validate_count(count)

        payload = {
            "query": query,
            "freshness": freshness,
            "count": count,
            "answer": False,
            "stream": False,
        }

        response = await _post_json(BOCHA_AI_SEARCH_ENDPOINT, payload)
        results: list[str] = []

        for message in response.get("messages", []):
            if not isinstance(message, dict):
                continue

            content_text = str(message.get("content", ""))
            content_type = message.get("content_type")
            parsed_content = _safe_parse_json(content_text)

            if content_type == "webpage":
                for item in parsed_content.get("value", []):
                    if isinstance(item, dict):
                        results.append(_format_web_result(item))
                continue

            if content_type != "image" and content_text and content_text != "{}":
                results.append(content_text)

        return _join_results(results)
    except ValueError as e:
        return f"Invalid input: {e}"
    except RuntimeError as e:
        return f"Error: {e}"
    except httpx.HTTPStatusError as e:
        return (
            "Bocha AI Search API HTTP error occurred: "
            f"{e.response.status_code} - {e.response.text}"
        )
    except httpx.RequestError as e:
        return f"Error communicating with Bocha AI Search API: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"
