<p align="center">
  <img src="./assets/bocha-logo-square.png" alt="Bocha Search" width="96" height="96" />
</p>

<h1 align="center">博查 MCP Server</h1>

<p align="center">
  <a href="./README.md">English</a> · <a href="./README.zh-CN.md">简体中文</a>
</p>

<p align="center">
  面向 Claude Desktop、Cursor 以及各类 MCP 客户端的博查联网搜索服务。
</p>

## 概览

`bocha-search-mcp` 提供两个 MCP 工具：

- `bocha_web_search`：通用网页检索与引用
- `bocha_ai_search`：语义增强搜索与结构化结果

当前仓库已经针对自助接入做过规范化改造，不再依赖手工 clone 本地源码再拼接
`uv --directory /path/to/repo run ...`。

## 特性

- 支持 `uvx --from git+https://github.com/Bocha-Labs/bocha-search-mcp`
- 适合 Claude Desktop、Cursor 和自动化 Agent
- 补齐了 `README`、`LICENSE`、`.env.example`、测试与 GitHub Actions CI
- 已通过真实 API 请求与真实 MCP 客户端安装验证

## 开放平台

- 产品主页：[博查 AI 搜索](https://bochaai.com/)
- 接口开通：[博查开放平台](https://open.bocha.cn)
- 鉴权环境变量：`BOCHA_API_KEY`

## 快速开始

### 推荐方式

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

仓库根目录提供了可直接复用的示例文件：

- `mcp-config.example.json`

### 本地开发

```bash
uv run bocha-search-mcp
```

或：

```bash
uv run python -m bocha_search_mcp
```

## 推荐元信息

如果你的 MCP 客户端支持手动填写展示信息，推荐使用下面这些值：

- 标题：`Bocha Search`
- 描述：`Bocha MCP server for Web Search and AI Search in MCP clients.`
- 图标地址：`https://cdn.jsdelivr.net/gh/Bocha-Labs/bocha-search-mcp@v0.1.1/assets/bocha-logo-square.png`

注意：当前大多数 MCP 快速导入流程只会解析连接配置，标题、描述和图标通常仍需要在客户端界面中手动补充。

## 客户端接入

### LobeHub Desktop

在“自定义 MCP”或“JSON 快速导入”中使用：

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

macOS 配置路径：

- `~/Library/Application Support/Claude/claude_desktop_config.json`

Windows 配置路径：

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

将同样的配置写入 Cursor 使用的 MCP 配置文件即可：

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
- 已获取可用的博查 API Key

### `.env`

```bash
cp .env.example .env
```

```dotenv
BOCHA_API_KEY="your-api-key"
```

## 工具说明

### `bocha_web_search`

通用网页搜索，返回标题、链接、摘要、发布时间和站点名称。

参数：

- `query`：必填搜索词
- `freshness`：`YYYY-MM-DD`、`YYYY-MM-DD..YYYY-MM-DD`、`noLimit`、`oneYear`、`oneMonth`、`oneWeek`、`oneDay`
- `count`：`1-50`

### `bocha_ai_search`

语义增强搜索，可返回更丰富的垂类信息和结构化结果。

参数：

- `query`：必填搜索词
- `freshness`：`YYYY-MM-DD`、`YYYY-MM-DD..YYYY-MM-DD`、`noLimit`、`oneYear`、`oneMonth`、`oneWeek`、`oneDay`
- `count`：`1-50`

说明：

- `bocha_ai_search` 可能需要单独开通接口权限
- 如果返回 `401` 且 message 为 `无接口调用权限`，说明当前 API Key 尚未进入所需白名单

## 调试

调试本地仓库：

```bash
npx @modelcontextprotocol/inspector uv run bocha-search-mcp
```

调试远端 Git 拉起方式：

```bash
npx @modelcontextprotocol/inspector uvx --from git+https://github.com/Bocha-Labs/bocha-search-mcp bocha-search-mcp
```

## 测试

当前保留了一组小而关键的回归测试，主要覆盖：

- 缺少 `BOCHA_API_KEY` 时的启动行为
- 输入参数校验
- Web Search / AI Search 的结果解析

运行方式：

```bash
uv run python -m unittest discover -s tests -v
```

## 使用示例

![示例：阿里巴巴 2024 ESG 报告](./assets/alibaba-2024-esg-report.png)

## 常见错误

| HTTP 状态码 | 示例 message | 常见原因 | 建议处理方式 |
| --- | --- | --- | --- |
| 400 | `Missing parameter query` | 请求参数缺失 | 检查 `query` 是否已正确传入 |
| 400 | `The API KEY is missing` | 缺少鉴权信息 | 检查 `BOCHA_API_KEY` 是否已正确配置，并确认客户端已将其传入 MCP 进程 |
| 401 | `Invalid API KEY` | API Key 无效 | 检查 Key 是否填写错误、已过期，或使用了错误环境的 Key |
| 401 | `无接口调用权限` | 当前账号未开通对应接口 | `bocha_ai_search` 可能需要额外白名单权限 |
| 403 | `You do not have enough money` | 余额不足 | 前往 [博查开放平台](https://open.bocha.cn) 充值 |
| 429 | `You have reached the request limit` | 请求频率超限 | 降低调用频率，或根据额度规则提升可用配额 |
| 500 | `xxxx` | 服务端异常 | 稍后重试，并结合 `log_id` 联系官方支持排查 |

如果需要向博查技术支持反馈问题，请优先保留上游响应中的 `log_id`。

## FAQ

### 为什么不再推荐 `uv --directory /path/to/repo run ...`？

因为这种方式依赖本地源码目录与人工维护的绝对路径，不适合市场安装、自动化导入和 Agent 自助使用。

### 为什么推荐 `uvx`？

`uvx` 更适合“一次配置，多处运行”的 MCP 场景，在桌面客户端、自动化 Agent 和 CI 环境中都更稳定。

### 后续发布到 PyPI 后配置会更短吗？

会。发布到 PyPI 后，可以进一步简化为：

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

本项目采用 `MIT` License，见 [LICENSE](./LICENSE)。
