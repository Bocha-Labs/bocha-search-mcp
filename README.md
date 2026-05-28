<p align="center">
  <img src="./assets/bocha-logo-square.png" alt="Bocha Search" width="96" height="96" />
</p>

<h1 align="center">Bocha Search MCP Server</h1>

<p align="center">
  <a href="./README.md">English</a> · <a href="./README.zh-CN.md">简体中文</a>
</p>

<p align="center">
  Bocha MCP server for Web Search and AI Search, built for Claude Desktop,
  Cursor, and other MCP clients.
</p>

## Overview

`bocha-search-mcp` provides two MCP tools:

- `bocha_web_search`: general web retrieval with citations
- `bocha_ai_search`: semantic search with richer structured results

This repository is optimized for self-serve MCP usage. It no longer depends on
manual local source checkout or `uv --directory /path/to/repo run ...`.

## Highlights

- Works with `uvx --from git+https://github.com/Bocha-Labs/bocha-search-mcp`
- Suitable for Claude Desktop, Cursor, and automation agents
- Includes `README`, `LICENSE`, `.env.example`, tests, and GitHub Actions CI
- Verified with real API calls and real Claude Desktop installation

## Open Platform

- Product: [Bocha AI Search](https://bochaai.com/)
- API access: [Bocha Open Platform](https://open.bocha.cn)
- Auth env: `BOCHA_API_KEY`

## Quick Start

### Recommended

```json
{
  "mcpServers": {
    "bocha-search-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/Bocha-Labs/bocha-search-mcp",
        "bocha-search-mcp"
      ],
      "env": {
        "BOCHA_API_KEY": "your-api-key"
      }
    }
  }
}
```

Reusable example:

- `mcp-config.example.json`

### Local Development

```bash
uv run bocha-search-mcp
```

or:

```bash
uv run python -m bocha_search_mcp
```

## Recommended Metadata

If your MCP client lets you fill custom metadata manually, the following values
work well for Bocha:

- Title: `Bocha Search`
- Description: `Bocha MCP server for Web Search and AI Search in MCP clients.`
- Avatar URL: `https://cdn.jsdelivr.net/gh/Bocha-Labs/bocha-search-mcp@v0.1.1/assets/bocha-logo-square.png`

Note: current MCP quick-import flows usually parse connection config only. Title,
description, and avatar may still need to be filled in manually by the client UI.

## Client Setup

### LobeHub Desktop

Use `Custom MCP` or `JSON Quick Import`:

```json
{
  "mcpServers": {
    "bocha-search-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/Bocha-Labs/bocha-search-mcp",
        "bocha-search-mcp"
      ],
      "env": {
        "BOCHA_API_KEY": "your-api-key"
      }
    }
  }
}
```

### Claude Desktop

macOS config:

- `~/Library/Application Support/Claude/claude_desktop_config.json`

Windows config:

- `%APPDATA%/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "bocha-search-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/Bocha-Labs/bocha-search-mcp",
        "bocha-search-mcp"
      ],
      "env": {
        "BOCHA_API_KEY": "your-api-key"
      }
    }
  }
}
```

### Cursor

Use the same MCP config in Cursor:

```json
{
  "mcpServers": {
    "bocha-search-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/Bocha-Labs/bocha-search-mcp",
        "bocha-search-mcp"
      ],
      "env": {
        "BOCHA_API_KEY": "your-api-key"
      }
    }
  }
}
```

## Environment

### Requirements

- `uv`
- a valid Bocha API key

### `.env`

```bash
cp .env.example .env
```

```dotenv
BOCHA_API_KEY="your-api-key"
```

## Tools

### `bocha_web_search`

General web search with title, URL, description, published date, and site name.

Parameters:

- `query`: required search term
- `freshness`: `YYYY-MM-DD`, `YYYY-MM-DD..YYYY-MM-DD`, `noLimit`, `oneYear`, `oneMonth`, `oneWeek`, `oneDay`
- `count`: `1-50`

### `bocha_ai_search`

Semantic search with richer vertical-domain results and structured cards.

Parameters:

- `query`: required search term
- `freshness`: `YYYY-MM-DD`, `YYYY-MM-DD..YYYY-MM-DD`, `noLimit`, `oneYear`, `oneMonth`, `oneWeek`, `oneDay`
- `count`: `1-50`

Notes:

- `bocha_ai_search` may require separate API permission
- if the response is `401` with `无接口调用权限`, your API key is not yet in the required whitelist

## Debugging

Local repository:

```bash
npx @modelcontextprotocol/inspector uv run bocha-search-mcp
```

Remote Git startup:

```bash
npx @modelcontextprotocol/inspector uvx --from git+https://github.com/Bocha-Labs/bocha-search-mcp bocha-search-mcp
```

## Testing

This repository keeps a focused regression test suite for:

- startup behavior without `BOCHA_API_KEY`
- input validation
- Web Search and AI Search result parsing

Run:

```bash
uv run python -m unittest discover -s tests -v
```

## Example

![Example: Alibaba 2024 ESG report](./assets/alibaba-2024-esg-report.png)

## Common Errors

| HTTP status | Example message                      | Reason                    | Suggested action                                                            |
| ----------- | ------------------------------------ | ------------------------- | --------------------------------------------------------------------------- |
| 400         | `Missing parameter query`            | Missing request parameter | Check whether `query` is provided                                           |
| 400         | `The API KEY is missing`             | Missing auth header       | Check whether `BOCHA_API_KEY` is configured and passed into the MCP process |
| 401         | `Invalid API KEY`                    | Invalid API key           | Check whether the key is wrong, expired, or from the wrong environment      |
| 401         | `无接口调用权限`                     | Missing API permission    | `bocha_ai_search` may require extra whitelist access                        |
| 403         | `You do not have enough money`       | Insufficient balance      | Recharge in [Bocha Open Platform](https://open.bocha.cn)                    |
| 429         | `You have reached the request limit` | Rate limit reached        | Reduce request frequency or upgrade quota                                   |
| 500         | `xxxx`                               | Server-side error         | Retry later and use `log_id` for support investigation                      |

Prioritize the upstream `log_id` when reporting issues to Bocha support.

## FAQ

### Why not use `uv --directory /path/to/repo run ...`?

Because it depends on a local checkout and a manual absolute path. That is not
ideal for marketplace installation, automated import, or self-serve MCP usage.

### Why is `uvx` recommended?

`uvx` is more suitable for one-time configuration and repeated MCP startup across
desktop apps, agents, and CI environments.

### Will the config become shorter after publishing to PyPI?

Yes. After PyPI release, it can be simplified to:

```json
{
  "mcpServers": {
    "bocha-search-mcp": {
      "command": "uvx",
      "args": ["bocha-search-mcp"],
      "env": {
        "BOCHA_API_KEY": "your-api-key"
      }
    }
  }
}
```

## License

This project is licensed under the `MIT` License. See [LICENSE](./LICENSE).
