<p align="center">
  <img src="./assets/bocha-logo-square.png" alt="Bocha Search" width="96" height="96" />
</p>

<h1 align="center">博查联网搜索 MCP Server</h1>

<p align="center">
  简体中文 · <a href="./README.en.md">English</a>
</p>

<p align="center">
  面向 AI Agent 和各类 MCP 客户端的联网搜索服务，提供 Web Search 与
  AI Search 两类能力，覆盖近千亿网页和生态内容源。
</p>

## 产品简介

博查联网搜索 MCP Server 将博查的联网搜索能力接入到 Claude Desktop、Cursor 以及其他支持 MCP 的客户端和运行时中。

当前仓库提供两个 MCP 工具：

- `bocha_web_search`：网页搜索与引用结果返回
- `bocha_ai_search`：语义增强搜索与结构化模态卡返回

## 关键信息

- 产品主页：[博查](https://bocha.cn/)
- 开放平台：[https://open.bocha.cn](https://open.bocha.cn)
- MCP 包版本：`0.1.1`
- 鉴权方式：API Key
- 必需环境变量：`BOCHA_API_KEY`
- 适配平台：Claude Desktop、Cursor、支持 MCP 的 Python 与 Agent Runtime

## 产品特点

- 面向 AI 应用优化的联网搜索能力
- 支持自然语言搜索与语义排序
- 返回网页标题、链接、摘要、发布时间、站点名称等结果
- 支持天气、百科、医疗、日历、股票等结构化模态卡
- 适合时效信息检索、外部来源引用与 Agent 知识补全

## 安装方式

### 推荐 MCP 配置

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

### `stdio` 可直接导入配置

上面的配置本质上就是 `stdio` 方式，适合 LobeHub、Claude Desktop、Cursor 等
MCP 客户端直接导入：

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

## 客户端接入

### LobeHub Desktop

在“自定义 MCP”或“JSON 快速导入”中直接使用上面的推荐配置。

### Claude Desktop

macOS 配置路径：

- `~/Library/Application Support/Claude/claude_desktop_config.json`

Windows 配置路径：

- `%APPDATA%/Claude/claude_desktop_config.json`

使用与上文一致的 MCP 配置即可。

### Cursor

将同样的 MCP 配置写入 Cursor 使用的 MCP 配置文件即可。

## 工具说明

### `bocha_web_search`

从博查搜索全网信息和网页链接，返回适合 AI 使用的网页结果，包括标题、URL、
摘要、发布时间、站点名称等信息。

适用场景：

- 查询最新新闻与时效信息
- 为 AI 回答补充外部来源与引用
- 进行开放问题的联网检索

输入参数：

- `query`：必填搜索词
- `freshness`：`YYYY-MM-DD`、`YYYY-MM-DD..YYYY-MM-DD`、`noLimit`、`oneYear`、`oneMonth`、`oneWeek`、`oneDay`
- `count`：`1-50`，默认 `10`

输出内容：

- 网页标题
- 网页链接
- 网页摘要和正文
- 发布时间
- 网站名称

### `bocha_ai_search`

在 Web Search 的基础上，AI 识别搜索词语义，并额外返回更丰富的垂直领域结构化
模态卡内容，例如天气卡、百科卡、医疗卡、日历卡、股票卡等。

适用场景：

- 获取天气、百科、医疗、日历等结构化信息
- 提升 AI 对时效性问题和垂直领域问题的回答质量
- 在网页结果之外，为 Agent 提供更丰富的补充上下文

输入参数：

- `query`：必填搜索词
- `freshness`：`YYYY-MM-DD`、`YYYY-MM-DD..YYYY-MM-DD`、`noLimit`、`oneYear`、`oneMonth`、`oneWeek`、`oneDay`
- `count`：`1-50`，默认 `10`

输出内容：

- 网页标题
- 网页链接
- 网页摘要和正文
- 发布时间
- 网站名称
- 结构化模态卡内容

说明：

- `bocha_ai_search` 可能需要单独开通接口权限
- 如果返回 `401` 且 message 为 `无接口调用权限`，说明当前 API Key 尚未进入所需白名单

## 推荐展示元信息

如果你的 MCP 客户端支持手动填写展示信息，推荐使用下面这些值：

- 标题：`Bocha Search`
- 描述：`博查联网搜索 MCP 服务，提供 Web Search 与 AI Search 两类能力。`
- 图标地址：`https://cdn.jsdelivr.net/gh/Bocha-Labs/bocha-search-mcp@v0.1.1/assets/bocha-logo-square.png`

注意：当前不少 MCP 导入流程只会解析连接配置，标题、描述和图标通常仍需要在客户端界面中手动补充。

## 服务开通

请前往 [博查开放平台](https://open.bocha.cn) 获取 API Key。

`.env` 示例：

```bash
cp .env.example .env
```

```dotenv
BOCHA_API_KEY="your-api-key"
```

## 使用示例

![示例：阿里巴巴 2024 ESG 报告](./assets/alibaba-2024-esg-report.png)

## 客户案例与能力说明

根据博查产品资料，博查目前已累计服务：

- `60000+` 泛企业客户
- DeepSeek 官方联网搜索供应方
- 阿里、腾讯、字节官方推荐的搜索 API

博查搜索内容源包括全网近千亿个网页，以及生态合作内容，覆盖短视频、新闻、百科、
天气、医疗、火车票、酒店、餐厅、景点、企业、学术等多个领域。

## 常见错误

| HTTP 状态码 | 示例 message                         | 常见原因               | 建议处理方式                                                         |
| ----------- | ------------------------------------ | ---------------------- | -------------------------------------------------------------------- |
| 400         | `Missing parameter query`            | 请求参数缺失           | 检查 `query` 是否已正确传入                                          |
| 400         | `The API KEY is missing`             | 缺少鉴权信息           | 检查 `BOCHA_API_KEY` 是否已正确配置，并确认客户端已将其传入 MCP 进程 |
| 401         | `Invalid API KEY`                    | API Key 无效           | 检查 Key 是否填写错误、已过期，或使用了错误环境的 Key                |
| 401         | `无接口调用权限`                     | 当前账号未开通对应接口 | `bocha_ai_search` 可能需要额外白名单权限                             |
| 403         | `You do not have enough money`       | 余额不足               | 前往 [博查开放平台](https://open.bocha.cn) 充值                      |
| 429         | `You have reached the request limit` | 请求频率超限           | 降低调用频率，或根据额度规则提升可用配额                             |
| 500         | `xxxx`                               | 服务端异常             | 稍后重试，并结合 `log_id` 联系官方支持排查                           |

如果需要向博查技术支持反馈问题，请优先保留上游响应中的 `log_id`。

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



## License

本项目采用 `MIT` License，见 [LICENSE](./LICENSE)。
