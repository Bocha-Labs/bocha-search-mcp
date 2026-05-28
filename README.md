# 博查 MCP Server

![Bocha Search MCP Server](assets/bocha-logo-720x180.png)

博查 MCP Server 为支持 MCP 的 Agent、桌面客户端和自动化工具提供统一的联网搜索能力，包含:

- `bocha_web_search`: 通用网页搜索
- `bocha_ai_search`: 语义增强搜索，返回模态卡等结构化内容

这份仓库经过调整后，重点解决了“必须先手工 clone 到本地、再自己拼路径才能运行”的问题。推荐直接使用 `uvx` 从 Git 仓库拉起，适合 LobeHub、Claude Desktop、Cursor 以及各类自动化 Agent 自助接入。

## 产品简介

博查是一个面向 AI 应用的搜索引擎，让你的 Agent 从近千亿网页和生态内容源中获取高质量世界知识，覆盖新闻、天气、百科、医疗、火车票、图片等多类场景。

服务开通地址:

- [博查 AI 开放平台](https://open.bocha.cn)

鉴权方式:

- `BOCHA_API_KEY`

## Agent 自助使用

### 推荐方式: 直接从 Git 仓库运行

如果你的 MCP 客户端支持 `uvx`，推荐直接使用下面的配置。它不依赖本地源码目录，也不需要先执行手工安装。

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

仓库根目录也提供了可直接复用的示例文件:

- `mcp-config.example.json`

### 本地开发方式

如果你已经拿到了仓库源码，适合本地调试或二次开发:

```bash
uv run bocha-search-mcp
```

也可以直接使用模块方式启动:

```bash
uv run python -m bocha_search_mcp
```

## 在常见客户端中使用

### LobeHub Desktop

在自定义 MCP 或 JSON 快速导入中使用:

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

macOS 配置文件:

- `~/Library/Application Support/Claude/claude_desktop_config.json`

Windows 配置文件:

- `%APPDATA%/Claude/claude_desktop_config.json`

配置内容:

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

可将同样的配置写入 Cursor 使用的 MCP 配置文件中:

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

## 环境准备

### 必需项

- 已安装 `uv`
- 已获取博查 API Key

### 环境变量

可复制 `.env.example` 为 `.env`:

```bash
cp .env.example .env
```

然后填入:

```dotenv
BOCHA_API_KEY="your-api-key"
```

## 工具说明

### `bocha_web_search`

从博查搜索全网网页信息，返回网页标题、链接、摘要、发布时间、站点名称等。

输入参数:

- `query`: 搜索词，必填
- `freshness`: 时间范围，可选值 `YYYY-MM-DD`、`YYYY-MM-DD..YYYY-MM-DD`、`noLimit`、`oneYear`、`oneMonth`、`oneWeek`、`oneDay`
- `count`: 返回结果条数，范围 `1-50`

### `bocha_ai_search`

在网页搜索基础上返回更丰富的语义理解结果与模态卡内容。

输入参数:

- `query`: 搜索词，必填
- `freshness`: 时间范围，可选值 `YYYY-MM-DD`、`YYYY-MM-DD..YYYY-MM-DD`、`noLimit`、`oneYear`、`oneMonth`、`oneWeek`、`oneDay`
- `count`: 返回结果条数，范围 `1-50`

注意:

- `bocha_ai_search` 可能需要单独开通接口权限
- 如果返回 `401` 且 message 为“无接口调用权限”，说明当前 API Key 尚未加入对应白名单

## 调试

如果需要使用 MCP Inspector 调试本地仓库:

```bash
npx @modelcontextprotocol/inspector uv run bocha-search-mcp
```

如果希望调试远端 Git 拉起方式:

```bash
npx @modelcontextprotocol/inspector uvx --from git+https://github.com/Bocha-Labs/bocha-search-mcp bocha-search-mcp
```

## 测试

当前仓库保留了一组小而关键的回归测试，重点覆盖:

- 启动入口在缺少 `BOCHA_API_KEY` 时的行为
- 关键参数校验
- Web Search / AI Search 的结果解析

运行方式:

```bash
uv run python -m unittest discover -s tests -v
```

对于这类 MCP 仓库，优先建议提交可执行的测试代码，而不是额外维护一份冗长的测试文档。README 中保留运行命令与覆盖范围说明即可。

## 使用示例

![示例: alibaba 2024 esg report](assets/alibaba-2024-esg-report.png)

## 常见问题

### 常见错误码

调用博查 API 时，常见错误及处理方式如下:

| HTTP 状态码 | 示例 message                         | 常见原因                   | 建议处理方式                                                                   |
| ----------- | ------------------------------------ | -------------------------- | ------------------------------------------------------------------------------ |
| 400         | `Missing parameter query`            | 请求参数缺失               | 检查 `query` 是否已正确传入                                                    |
| 400         | `The API KEY is missing`             | 未传入鉴权信息             | 检查 `BOCHA_API_KEY` 是否已正确配置，并确认 MCP 客户端已将环境变量传入服务进程 |
| 401         | `Invalid API KEY`                    | API Key 无效               | 检查 API Key 是否填写错误、已过期，或使用了错误环境的 Key                      |
| 401         | `无接口调用权限`                     | 当前账号未开通对应接口权限 | `bocha_ai_search` 可能需要额外白名单，请按博查官方指引联系技术人员开通         |
| 403         | `You do not have enough money`       | 账户余额不足               | 前往 [博查 AI 开放平台](https://open.bocha.cn) 充值                            |
| 429         | `You have reached the request limit` | 请求频率达到限制           | 降低请求频率，或根据 API 定价与额度规则提升可用额度                            |
| 500         | `xxxx`                               | 服务端内部异常             | 稍后重试，并结合响应中的 `log_id` 联系官方支持排查                             |

如果返回错误，请优先关注响应中的 `log_id`，便于向博查技术支持定位问题。

### 为什么不再推荐 `uv --directory /path/to/repo run ...`?

这种方式依赖人工提前下载源码并填入本地绝对路径，不适合市场安装、自动化导入和 Agent 自助使用。改成 `uvx --from git+https://...` 后，客户端可直接按标准命令拉起。

### 为什么推荐 `uvx`?

`uvx` 更适合“一次配置，随处运行”的 MCP 接入方式。对于市场、Agent、桌面客户端和 CI 环境，它比手工 clone 本地仓库更稳定，也更容易自动化。

### 将来发布到 PyPI 后还需要改配置吗?

如果后续发布到 PyPI，可以进一步简化为:

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

## 项目说明

目前博查已累计服务大量企业与开发者用户，并持续为各类 AI 应用提供联网搜索能力。这个 MCP Server 的目标，是让 Agent 以最少的人为干预接入博查搜索。

## License

本项目使用 `MIT` License，见 [LICENSE](LICENSE)。
