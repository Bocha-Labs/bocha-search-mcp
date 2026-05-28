import io
import unittest
from unittest.mock import patch

import bocha_search_mcp
from bocha_search_mcp import main


class EntrypointTest(unittest.TestCase):
    def test_main_exits_without_api_key(self) -> None:
        stderr = io.StringIO()

        with (
            patch.dict("os.environ", {}, clear=True),
            patch("sys.stderr", stderr),
            self.assertRaises(SystemExit) as error,
        ):
            main()

        self.assertEqual(error.exception.code, 1)
        output = stderr.getvalue()
        self.assertIn("BOCHA_API_KEY", output)
        self.assertIn("https://open.bocha.cn", output)

    def test_main_runs_server_when_api_key_exists(self) -> None:
        with (
            patch.dict("os.environ", {"BOCHA_API_KEY": "test-key"}, clear=True),
            patch.object(bocha_search_mcp.server, "run") as run_mock,
        ):
            main()

        run_mock.assert_called_once_with(transport="stdio")
