<p align="center">
  <img src="./assets/bocha-logo-square.png" alt="Bocha Search" width="96" height="96" />
</p>

<h1 align="center">Bocha Search MCP Server</h1>

<p align="center">
  <a href="./README.md">简体中文</a> · English
</p>

<p align="center">
  MCP search service for AI agents and desktop clients, with Web Search and AI
  Search across nearly one hundred billion web pages and ecosystem content
  sources.
</p>

## Product Overview

Bocha Search MCP Server brings Bocha's network search capability into MCP
clients such as Claude Desktop, Cursor, and other agent runtimes.

It exposes two tools:

- `bocha_web_search` for general web retrieval with citations
- `bocha_ai_search` for semantic search with richer structured cards

## Key Information

- Product: [Bocha](https://bocha.cn/)
- Open platform: [https://open.bocha.cn](https://open.bocha.cn)
- MCP package version: `0.1.1`
- Auth method: API Key
- Required env: `BOCHA_API_KEY`
- Recommended clients: Claude Desktop, Cursor, Python-based MCP runtimes

## Why Bocha

- Designed for AI use cases instead of ad-driven search ranking
- Supports natural-language search and semantic ranking
- Returns titles, URLs, snippets, publish time, site names, and other web details
- Can provide structured vertical cards such as weather, encyclopedia, calendar, medical, and stocks
- Suitable for time-sensitive retrieval, external citations, and knowledge grounding in agents

## Installation

### Recommended MCP config

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

### Direct `stdio` import config

The config above already uses `stdio`, and can be directly imported into MCP
clients such as LobeHub, Claude Desktop, and Cursor:

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

### Local development

```bash
uv run bocha-search-mcp
```

or:

```bash
uv run python -m bocha_search_mcp
```

## Client Setup

### LobeHub Desktop

Use `Custom MCP` or `JSON Quick Import` with the recommended config above.

### Claude Desktop

macOS config:

- `~/Library/Application Support/Claude/claude_desktop_config.json`

Windows config:

- `%APPDATA%/Claude/claude_desktop_config.json`

Use the same MCP config as shown above.

### Cursor

Use the same MCP config in Cursor.

## Tools

### `bocha_web_search`

General web search for titles, URLs, snippets, publish time, site names, and
other web result details.

Use cases:

- latest news and current events
- external citations for AI answers
- general fact lookup from the open web

Parameters:

- `query`: required search term
- `freshness`: `YYYY-MM-DD`, `YYYY-MM-DD..YYYY-MM-DD`, `noLimit`, `oneYear`, `oneMonth`, `oneWeek`, `oneDay`
- `count`: `1-50`, default `10`

Returns:

- title
- URL
- snippet
- published date
- site name

### `bocha_ai_search`

Semantic search built on top of Bocha Web Search. In addition to web results, it
can return richer structured cards for vertical scenarios such as weather,
calendar, encyclopedia, medical, stocks, and more.

Use cases:

- structured answers for time-sensitive topics
- vertical search results beyond plain web snippets
- richer grounding context for agents

Parameters:

- `query`: required search term
- `freshness`: `YYYY-MM-DD`, `YYYY-MM-DD..YYYY-MM-DD`, `noLimit`, `oneYear`, `oneMonth`, `oneWeek`, `oneDay`
- `count`: `1-50`, default `10`

Returns:

- title
- URL
- snippet
- published date
- site name
- structured cards when available

Notes:

- `bocha_ai_search` may require separate API permission
- if the response is `401` with `无接口调用权限`, your API key is not yet in the required whitelist

## Recommended Marketplace Metadata

If your MCP client allows manual display metadata, the following values work
well for Bocha:

- Title: `Bocha Search`
- Description: `Bocha MCP server for Web Search and AI Search in MCP clients.`
- Avatar URL: `https://cdn.jsdelivr.net/gh/Bocha-Labs/bocha-search-mcp@v0.1.1/assets/bocha-logo-square.png`

Note: many MCP import flows only parse connection config. Title, description,
and avatar may still need to be filled manually in client UI.

## API Access

Get your API key from [Bocha Open Platform](https://open.bocha.cn).

`.env` example:

```bash
cp .env.example .env
```

```dotenv
BOCHA_API_KEY="your-api-key"
```

## Example

![Example: Alibaba 2024 ESG report](./assets/alibaba-2024-esg-report.png)

## Customer Adoption

According to Bocha product materials, Bocha has served:

- `60000+` enterprise customers
- DeepSeek official web search supplier
- officially recommended search API by Alibaba, Tencent, and ByteDance

Bocha content sources include nearly one hundred billion web pages plus
ecosystem data such as short videos, news, encyclopedia, weather, healthcare,
train tickets, hotels, restaurants, attractions, enterprises, and academic
content.

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

## License

This project is licensed under the `MIT` License. See [LICENSE](./LICENSE).
