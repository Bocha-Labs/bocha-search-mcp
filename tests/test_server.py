import importlib
import unittest
from unittest.mock import AsyncMock, patch

server_module = importlib.import_module("bocha_search_mcp.server")


class ValidationHelpersTest(unittest.TestCase):
    def test_validate_count_rejects_out_of_range(self) -> None:
        with self.assertRaises(ValueError):
            server_module._validate_count(0)

        with self.assertRaises(ValueError):
            server_module._validate_count(51)

    def test_validate_freshness_accepts_common_values(self) -> None:
        server_module._validate_freshness("noLimit")
        server_module._validate_freshness("oneWeek")
        server_module._validate_freshness("2026-01-01")
        server_module._validate_freshness("2026-01-01..2026-01-31")

    def test_validate_freshness_rejects_invalid_values(self) -> None:
        with self.assertRaises(ValueError):
            server_module._validate_freshness("yesterday")

    def test_safe_parse_json_returns_empty_dict_for_invalid_json(self) -> None:
        self.assertEqual(server_module._safe_parse_json("not-json"), {})
        self.assertEqual(server_module._safe_parse_json('["not", "an", "object"]'), {})


class ServerToolTest(unittest.IsolatedAsyncioTestCase):
    async def test_web_search_returns_validation_error(self) -> None:
        result = await server_module.bocha_web_search("hello", count=0)
        self.assertIn("Invalid input", result)

    async def test_web_search_returns_missing_key_error(self) -> None:
        with patch.dict("os.environ", {}, clear=True):
            result = await server_module.bocha_web_search("hello")

        self.assertIn("BOCHA_API_KEY", result)

    async def test_web_search_formats_results(self) -> None:
        mocked_response = {
            "data": {
                "webPages": {
                    "value": [
                        {
                            "name": "Bocha",
                            "url": "https://bocha.cn",
                            "summary": "AI search engine",
                            "datePublished": "2026-01-01",
                            "siteName": "BochaAI",
                        }
                    ]
                }
            }
        }

        with patch.object(server_module, "_post_json", AsyncMock(return_value=mocked_response)):
            result = await server_module.bocha_web_search("bocha")

        self.assertIn("Title: Bocha", result)
        self.assertIn("URL: https://bocha.cn", result)

    async def test_ai_search_formats_webpage_and_text_messages(self) -> None:
        mocked_response = {
            "messages": [
                {
                    "content_type": "webpage",
                    "content": (
                        '{"value":[{"name":"Bocha AI","url":"https://bocha.cn/",'
                        '"summary":"semantic search","datePublished":"2026-01-02",'
                        '"siteName":"BochaAI"}]}'
                    ),
                },
                {
                    "content_type": "text",
                    "content": "Structured card: weather summary",
                },
                {
                    "content_type": "image",
                    "content": "{}",
                },
            ]
        }

        with patch.object(server_module, "_post_json", AsyncMock(return_value=mocked_response)):
            result = await server_module.bocha_ai_search("weather")

        self.assertIn("Title: Bocha AI", result)
        self.assertIn("Structured card: weather summary", result)

    async def test_ai_search_returns_no_results_when_response_is_empty(self) -> None:
        with patch.object(server_module, "_post_json", AsyncMock(return_value={"messages": []})):
            result = await server_module.bocha_ai_search("empty")

        self.assertEqual(result, "No results found.")
