# Draft: oh-my-opencode 配额与并发配置

## 原始需求
- 目标：依据官方文档（README.md）与本地 `@models.md`（可用模型说明），给出“如何配额、如何配置并发度比较合理”的建议。
- 关注点：
  - 配额/限流：每分钟请求数、并发请求数、令牌/计费预算、重试策略
  - 并发度：不同模型/提供商的并发上限、队列策略、批处理/合并请求

## 已知信息
- 官方文档：`https://github.com/code-yeongyu/oh-my-opencode/blob/dev/README.md`
- 需要结合：本地 `@models.md`（用户可用的模型清单/限制）

## 研究发现（已确认）

### 1) 你的本地模型与额度特性（/home/trydying/.config/opencode/models.md）
- GitHub Copilot 提供的模型：上下文上限按该平台能力计（示例：`github-copilot/gpt-5.2` 实际只有 128K）。
- OpenAI 订阅提供的模型：更接近模型原生上下文能力；同场景下套餐额度也更充足。
- 额度消耗倍率（你整理的表）：
  - 低倍率：`github-copilot/claude-haiku-4.5` 0.33x、`github-copilot/gemini-3-flash-preview` 0.33x、`github-copilot/gpt-5.1-codex-mini` 0.33x
  - 1x：`github-copilot/gpt-5.2`、`openai/gpt-5.2`、`openai/gpt-5.2-codex` 等
  - 高倍率：`github-copilot/claude-opus-4.5` 3x（并发时最容易“烧额度”）

### 2) OpenCode 主配置里的“limit”是 token 容量，不是并发（/home/trydying/.config/opencode/opencode.jsonc）
- `provider.openai.models.<model>.limit.context/output`：用于声明该模型可用的 context/output token 上限。
- 这里没有“每分钟请求数/并发数”的 rate limit 配置。

### 3) oh-my-opencode 的并发控制点（官方配置文档）
- 配置文件位置（优先级）：
  1. `.opencode/oh-my-opencode.json`（项目级）
  2. `~/.config/opencode/oh-my-opencode.json`（用户级）
  - 若同名存在 `.jsonc` 与 `.json`：`.jsonc` 优先。
- 并发相关 key 都在 `background_task` 下：
  - `defaultConcurrency`：默认并发；未配置时运行时默认回退到 5。
  - `providerConcurrency`：按 provider 限制并发（例如 openai/anthropic/google/github-copilot）。
  - `modelConcurrency`：按具体 model 限制并发（例如 `openai/gpt-5.2`）。
  - `staleTimeoutMs`：后台任务“过期/失活”超时（文档示例默认 180000ms，最小 60000ms）。
  - 优先级：`modelConcurrency` > `providerConcurrency` > `defaultConcurrency`。
- 配额/rate-limit：schema 中没有专门的 `quota`/`rateLimit` 键；主要通过并发上限“间接”尊重提供商限流。

### 4) 你的本地 oh-my-opencode.jsonc 当前状态（/home/trydying/.config/opencode/oh-my-opencode.jsonc）
- 已做了“成本分层”：
  - 主力执行/规划：`openai/gpt-5.2` / `openai/gpt-5.2-codex`
  - 轻量探索：`explore` 用 `github-copilot/gpt-5-mini`
  - `quick` 类别路由到 `github-copilot/claude-haiku-4.5`（0.33x）
- 目前未配置 `background_task` 并发，因此会走默认并发（推测 5）。


## 待确认（可能影响建议）
- 你使用的提供商/计费方式（OpenAI/Anthropic/本地模型/聚合网关等）
- 你的典型使用场景：交互式（单人）vs 团队共享、是否跑并行 Agent、是否跑大批量任务
- 你的“硬约束”：预算上限、可接受的延迟、是否需要强稳定性（少报错）

## 研究计划
- 读取 README：找出配额/并发/限流/队列相关配置项与推荐实践
- 定位 `@models.md`：确认你当前可用模型、上下文长度、速率限制提示等
- 输出：
  - 一套默认的保守配置（稳定优先）
  - 一套激进配置（吞吐优先）
  - 选择矩阵：根据场景/预算如何调参

## 新增需求：提速（用户反馈）
- 现状：从用户描述的真实任务看，规划阶段耗时 ~13m+，瓶颈主要在 subagent（Librarian/Explore）耗时。
- 观察/假设：`~/.config/opencode/oh-my-opencode.jsonc` 中 OpenAI 路由占比高且 variant 偏高（prometheus=high, sisyphus=xhigh），导致规划链路偏慢。
- 目标：
  - 略微降低 variant（优先降低规划链路：prometheus、metis、librarian、momus）
  - 将部分 OpenAI 模型替换为 GitHub Copilot 模型（牺牲部分上下文，换取速度）
  - 保留“重任务/长上下文”走 OpenAI 的兜底路径（避免质量/上下文崩溃）
