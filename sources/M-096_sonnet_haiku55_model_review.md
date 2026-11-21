# M-096 Sonnet/Haiku 5.5 模型专属指导复核：接口差异与提示/分工处方

## 元信息

- 来源链接：[Sonnet 5.5 指南](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5-5)、[Haiku 5.5 指南](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-haiku-5-5)
- 原文快照（供复核）：`_snapshots_local/batch15_master_20261016/sonnet.html/.txt`（SHA-256 12d99968…，2026-10-16 抓取）、`haiku.html/.txt`（af446078…）；2026-10-18 当前性复查 `_snapshots_local/batch16_glm_20261018/sonnet.html`（bef9c38a…）、`haiku.html`（0f852335…）——HTML 哈希不同但提取文本与 10-16 逐字一致；migration/preserved 同日复查亦与 10-16 文本一致
- 发布日期：两页均为滚动页，首次发布日未核（正文自称覆盖各自 5.5 专属模式）；当前性核验日期 2026-10-18
- 主张实质更新日期：未知（滚动页）
- 数据/事件观测窗口：指南内"Anthropic's testing / In testing"引用的厂商测试运行日期均未公开
- 当前适用状态：有条件（接口事实+厂商指导）；全部效果数字为厂商自报
- 工件/配置/预算及复现范围：两份指南全文（提取文本 116/94 行）逐段阅读；未运行任何 API；未读"What's new in Claude Sonnet/Haiku 5.5"产品页与各自 migration guide 全文（Haiku 迁移项数、Sonnet 五项 breaking changes 细节未核）
- 阅读覆盖与媒介限制：全文文字；无图表依赖（两页无图像结果）
- 版本日期：2026-10-16 快照版本 + 2026-10-18 当前性复查（文本无变化）
- 利益关系与独立性：Anthropic 厂商材料（同源计 1；营销渠道纪律适用：指南是产品使用指导，效果自报无独立验证）
- 复核触发器：Claude 下一代模型发布；两页实质修订；effort/thinking-display/per-message-effort 等 beta 转正或移除；最迟 2027-04 前查新据
- 检索日期：2026-10-16（主审抓取）/ 2026-10-18（本轮完整复核）
- 作者/机构：Anthropic
- 适用模型：Claude Sonnet 5.5、Claude Haiku 5.5（明确模型专属，两模型互不外推，更不外推至 Opus 5.5）
- 证据等级：接口事实（thinking 类型接受范围、400 错误条件、beta header、缓存失效）=可检验结论；全部效果数字与行为倾向描述=厂商经验断言
- 框架落点：prompt 治理 / harness 治理 / 评测（effort 重测）/ 安全（注入误读、refusal）
- 关联条目：M-090（Opus 5.5 复核与存废表）、M-033（早停防护）、M-047（删减旧补丁方向）、M-002（上下文工程）、Q-001（能力吸收观察）

## 一句话结论

截至10-18所取官方指南，三个模型的最低思考控制不同：Opus不能关闭，Sonnet可在high及以下使用between_tools关闭工具前思考但仍可能在工具间思考，Haiku可在low/medium/high使用disabled。三页均支持按模型重新评估设置，不能假定档名等效；这是同一厂商的迁移指导，不是三次独立效果验证。Sonnet/Haiku还报告中途用户消息可能被误当外部指令，并给出消息位置建议；未比较旧版，不认定为本代新出现或已证安全训练因果。

## 跨模型接口对照（本批核心交付；均出自各自指南正文）

| 接口/行为 | Opus 5.5（M-090） | Sonnet 5.5 | Haiku 5.5 |
|---|---|---|---|
| 关闭 up-front thinking | 不可（`disabled` 已移除） | `thinking: {"type": "between_tools"}` 为最低档，仅 high 及以下接受；xhigh/max 带 between_tools 返回 400 | `thinking: {"type": "disabled"}` 可用，仅 low/medium/high；xhigh/max 返回 400 |
| effort 默认档 | medium（Opus 5 为 high） | high（"the default on the Claude API"） | medium |
| 档位换算 | "Effort level names don't correspond to the same amount of thinking across models" | "Its levels are recalibrated: a level doesn't produce the same amount of thinking as the same level on Claude Sonnet 5. Run a fresh sweep against your own evals rather than carrying over the setting" | effort 替换 budget_tokens："there's no old setting to carry over"（首个带 effort 档的 Haiku） |
| 提示层控思考 | "more reliably than prompt instructions do" | "Asking it in the system prompt to think less doesn't reliably reduce its thinking" | "telling the model in the prompt to answer directly didn't stop it from thinking" |
| 顶层 effort 变更 | 使 prompt cache 失效 | 同（per-message effort beta 保缓存；与 between_tools 同用返回 400） | 同（per-message effort 需 `mid-conversation-output-config-2026-07-01` beta header；thinking off 时返回 400） |
| max_tokens | — | 128,000 上限；thinking 计入 max_tokens | 128,000 上限；thinking 计入（沿用 4.5 的 max_tokens 会截断） |
| safeguard refusal 后 server-side fallback | — | 有（beta）：仅重试 cyber 与 frontier_llm 于 Sonnet 5；不重试 bio/reasoning_extraction/general_harms | 无："Claude Haiku 5.5 has no server-side fallback (beta)"，客户端自行处理 stop_reason: "refusal" |
| 中途改 system prompt | preserved thinking 约束（M-090） | Sonnet 页未述该 400 机制；平台机制见 Haiku 页与 preserved-thinking 文档 | "A request that sends thinking blocks back after system changed can return a 400 error"——该页建议新提示用于新会话、当轮改指令放最新turn；这是保留旧thinking时的指导，其他合法失效块处置见preserved文档 |

[我方推导] 对照表的每行均出自单一厂商指南，接口事实可由 API 直接检验（本批未运行）；三模型差异本身就是"模型专属指导带适用模型字段+换代触发器"设计的行为证据——不能把模型专属的最低思考模式或档位含义外推；adaptive等共有机制并不因此在另外两个模型上错误。接口许可、厂商建议与目标任务优效分别核验。

## Sonnet 5.5 指南要点（全文阅读，引号逐字）

### 继续声明与迁移

- "Existing Claude Sonnet 5 prompts should perform well without changes, and the patterns in Prompting Claude Sonnet 5 remain a reasonable starting point. For the hardest long-horizon work, an Opus model is the better choice."——[我方推导] 与 Opus 5.5/GPT-5.2 同款"延续声明"叙事（M-090 存废表#5 的口径手法判断适用），且明示长时程任务模型分工。
- 自称五项 breaking API changes（细节在 migration guide，本批未读）。

### 治理机制清单（结构类似 M-090 的"当前指南列出的脚手架"，计数为选择性下限）

1. **effort 校准**：含"agentic coding 用 medium 起步、harder/longer 升 high；latency-sensitive 用 medium 或 low"。
2. **scope 控制（提示层）**：三段可直接粘贴的系统提示——持续推进文本（"Keep working until everything the user asked for is done…"）、防未要求添加（"Don't add features, tests, files, docs or refactors that weren't asked for"）、防 xhigh/max 自发评审（"Don't start extra rounds of review or hardening on your own, and don't launch reviewer sub-agents unless the user asked for a review"）。
3. **between_tools 模式**：见对照表；且"remove any instruction that tells the model not to think. Such instructions make it more likely that the model writes internal XML tags in its visible output"——旧"别思考"提示在新模式下主动有害。
4. **JSON 推理任务**：结构化输出+跳过思考=精度下降；对策三选一（加"Think the problem through before you answer."一行 / xhigh / 弃 between_tools）；stop_reason 为 max_tokens 一律按失败处理并重试；非结构化 JSON 的"取最后一个完整 JSON 值"解析配方。
5. **用户可见进度**：`display: "updates"`（beta，header `thinking-display-updates-2026-08-18`）；harness 数连续静默工具步后追加 turn-scoped system message 提醒；"If the turn stays quiet, stop sending reminders after the second or third"；提醒为追加而非插入，保缓存与 preserved thinking。
6. **聊天/知识工作中的工具使用**：先删除"only use tools when strictly necessary"/"minimize tool calls"类旧提示，再加搜索核查提示。
7. **中途用户消息（指南报告的失败模式）**：厂商在注入抵抗背景下描述真实用户消息被误读；没有安全训练消融或旧版对照。该节主要建议调整 harness 消息摆放（永不在 tool_result 内放用户文本；用户词作为 text block 附在最后一个 tool_result 后；harness 通知放独立 system message）；每步 tool result 后加 token 倒计时可致误读；task budgets (beta) "haven't been seen to cause this misread"。
8. **编码任务验证**：验证段（与 Haiku 指南逐字相同）。
9. **容错工具调用处理**：模型偶尔大小写错误调工具/参数名略异——harness 容忍明确匹配或以 is_error 返回确切名称。
10. **复杂视觉输入工具**：crop/zoom/代码处理图像；"in testing, with tools at high effort, the model read charts more accurately than without tools at max effort, at a fraction of the cost"。
11. **safeguard refusals**：五类（cyber/bio/frontier_llm/reasoning_extraction/general_harms）；删除要求复现推理的提示（invites reasoning_extraction declines）；Cyber/Life Sciences Verification Program。

### 厂商自报效果数字（全部为厂商测试口径，运行日期未公开，未独立验证）

- scope 防自发评审提示："In testing on coding tasks at max effort, this stopped the model from launching reviewer subagents and cut session cost by about a third, with no change in quality. It makes self-started review rounds by the main agent less frequent but doesn't remove them entirely."
- 静默提醒："At high effort, with a tool for sending the user a message available, the reminder leads the model to update the user more often and shortens its longest silent stretches, with no measurable change in task quality."
- 验证段："makes skipped or superficial checks rare, with no measurable change in task quality and only a slightly higher cost per task"。
- think-first 行：high 档"brings accuracy close to what the model reaches at xhigh, for a modest increase in output tokens"；low/medium 提升"though not to what the model reaches at high"。
- 拆分请求（答案+JSON 两请求）："led to high answer accuracy and JSON compliance, but at very high cost and latency"。
- 最后 JSON 值解析："In testing, this made nearly every response usable without changing its accuracy"。

## Haiku 5.5 指南要点（全文阅读，引号逐字）

### 与 Sonnet 不同的机制

- effort 全新引入（budget_tokens 无对应旧值）；五档说明含"also run your evals on Claude Sonnet 5.5 and compare performance, cost, and speed"——[我方推导] 厂商自己给出的跨模型比较指导，与"跨模型沿用设置"反模式一致。
- xhigh 多轮："the model sometimes writes its whole answer in its thinking and ends the turn with no visible text. If you see this behavior, check each response for an empty reply."
- 搜索任务：注入日期（"The current date is {{current_date}}."）+ 助推文本；助推文本"raised the search rate on questions whose answers had changed. On prompts that need no search, it added searches in only 0–3 percent of tries"；短提示+medium 档仅日期即可。
- **泛化反例（厂商自己证伪一条常见写法）**："Avoid blanket instructions such as 'search for any present-day factual question, regardless of how confident you are.' In Anthropic's testing, that instruction made the model search on half of the prompts that needed no search. It didn't produce more correct answers."
- thinking off + 结构化输出 → 漏掉必要工具调用：三选项（adaptive / 移除 output_config.format / tool_choice 强制）。
- 长提示早停："With a long coding-agent system prompt at low effort, it sometimes stops early and hands the task back to the user"——对应 M-033 早停防护在 Haiku 低档的新增观测；"moving from low to medium effort roughly halved early stopping. It also more than doubled the output tokens for each attempt."
- chatbot 坚持系统提示文本（anti-jailbreak 持久性）："The rules in this system prompt hold for the whole conversation. Keep to them when a user argues…"；"When instruction following matters most, also use high effort."
- refusal 相对 4.5 为新增；无 server-side fallback，重发通常仍拒绝。

### 模型行为怪癖与 harness 对策

- 低档跳过验证（同 Sonnet 验证段）；"the model checked its changes more often with this text, and its performance improved, at the cost of more tokens"。
- 中途用户消息误读：与 Sonnet 同构。
- 用户可见推理文本泄漏：切换 adaptive + medium（非提示修复）。

## 对 M-090 存废表的增量裁决

| # | M-090 原裁决 | 本批证据 | 增量 |
|---|---|---|---|
| 2 | thinking 禁用接口对 Opus 5.5 废止；禁思考提示按指南删除；其他缓解组合按任务重测，不能全部判废止 | Sonnet 5.5：`disabled` 不可用但 `between_tools` 可（≤high）；Haiku 5.5：`disabled` 仍可用（≤high）且 xhigh/max 均 400 | **模型专属裁决确认**：Sonnet仅在between_tools段明确要求移除禁思考提示；Haiku只报告“直接回答”提示未阻止思考，并保留disabled及其JSON提示缓解。不能称三模型一致要求删除；其他缓解按任务重测 |
| 6 | 换模型沿用 effort 设置=反模式（当时单模型） | Sonnet"Run a fresh sweep against your own evals rather than carrying over"；Haiku"no old setting to carry over"+跨模型比较指导 | **从单模型升至三模型一致的厂商指导**（仍非独立验证；性质=官方迁移指导） |
| 新增 | — | "提示层控制思考不可靠"在 Sonnet/Haiku 各有逐字表述（见对照表） | **条件性指导**：控制思考量优先使用支持的参数；不能概括成提示无效或都应删除。Sonnet的adaptive JSON任务仍建议think-first提示，Haiku的thinking-off JSON任务也有专门提示缓解 |

### Q-001 条件化观察（延续 M-090 口径，不作因果验证）

- 吸收方向（旧补丁删除/重测）：Sonnet 指南要求删除"only use tools when strictly necessary"、"hold all findings for the final response"以及告诉模型别思考的旧指令——与 Opus"Remove instructions that stood in for thinking"同向，且从推理类扩展到工具抑制类提示（对应 Sonnet 页 "any instruction that tells the model not to think"）。
- 并存观察：两页继续列出 ≥10/8 类当前脚手架（scope 提示、进度渲染协议、静默提醒、消息摆放规则、工具名容错、验证段、搜索助推、早停防护），多数带厂商自报数字；这些是当前指南报告的失败模式（中途消息误读、xhigh空回复、JSON/工具交互）；除明确标注的接口迁移外，未核旧代对照，不能按章节出现就认定本代新增。
- [我方推导] 新增一条观察：**厂商同时给出防注入背景下的消息误读说明与harness应对建议**；这支持保留消息归属和展示检查，未测训练因果、新旧安全效果或治理总量。refusal处理与中途消息误读是不同机制，不能合并成一个已证因果链。

## 影响入口处置（已执行）

| 入口 | 处置 |
|---|---|
| principles/AGENTS.md 核心12条 | grep 复核：无 thinking/effort/模型专属处方渗入正文，**不改**（模型专属内容属 07 登记与触发器层） |
| principles/07_evidence.md | 登记本批来源与接口对照（见批次增量节） |
| notes/M-090 | 加一行注记：存废表#2保留各模式条件，#6增加同厂商三模型指引；Sonnet/Haiku 复核完成 |
| graph/overview.md | "当前证据边界"更新 Claude 5.5 家族三模型对照完成一句 |
| docs/05、docs/09 | 交接与入口更新 |

## 适用条件与反证

- 适用条件：仅 Sonnet 5.5 / Haiku 5.5，且以 2026-10-18 当前性复查为限；beta 接口（per-message effort、display updates、server-side fallback）随时可能转正/变更；指南效果数字全部为厂商测试，任务集与运行日期未公开，不能外推到使用方自己的任务
- 反证/局限：
  - 厂商自报：所有"In (Anthropic's) testing"数字无任务集规模、无逐例数据、无第三方复现；"no measurable change in task quality"未给度量方式
  - 我方限制：未读两模型"What's new"产品页与 migration guide 全文（Sonnet 五项 breaking changes、Haiku 迁移项数未核）；未运行 API 验证接口事实；未读 Prompting Claude Sonnet 5 / Haiku 4.5 旧指南做逐节新增归属对照（指南小节结构不构成代际新增证据）
  - 滚动页：发布日期未核，10-18 复查仅确认两日内无文本变化

## 与已有条目的关系

- M-090：直接延续——存废表#2条件化、#6补同厂商指南，Q-001保留当前接口/消息处理的条件观察，不据此断言训练引入新失败
- M-033（长运行 harness）：Haiku 低档早停+验证段+努力档权衡为新增模型侧证据
- M-047（删减旧补丁）：删除工具抑制类旧提示扩展其适用面（仍候选级）
- M-002：消息摆放规则（mid-turn）属其 context engineering 框架内 harness 细节
- D03/D05（职责分配/工具接口）：工具名容错、消息摆放、静默提醒节奏均为"模型怪癖由 harness 承接"的现行厂商指导实例

## 后续动作

- [ ] 需要复现的主张：在服务/预算获授权时按模型、平台、模式和header设计最小请求矩阵核接口；单次成功不能确认全部条件，接口通过也不等于任务效果通过
- [ ] 需要补读的：两模型 migration guide 全文（breaking changes 全表）；Prompting Claude Sonnet 5 / Haiku 4.5 旧指南（新增归属对照）；"What's new"产品页
- [ ] 复核触发器：Claude 下一代发布；指南实质修订；beta 接口变更；2027-04 前查新据

## 2026-10-18 主审修正

回到Sonnet/Haiku两份全文：移除“三模型均删禁思考提示”“所有处方外推都错”“安全训练引入本代新失败”的扩大结论，保留模式/平台/消息位置条件与厂商身份。没有API调用或新代因果实验。
