# M-090 Claude Opus 5.5 代际复核：旧指导存废与 Q-001 条件化观察

## 元信息

- 来源链接：[官方提示指南](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5-5)、[发布文](https://www.anthropic.com/claude-opus-5-5)、[METR预部署评估](https://metr.org/blog/2026-09-22-claude-opus-5-5/)
- 原文快照（供复核）：`_snapshots_local/batch15/anthropic_opus55_guide.md/.html/.txt`、`anthropic_opus55_announce.md/.html/.txt`、`metr_opus55_eval.md/.html/.txt`；HTML SHA-256 见 capture 输出（75735a4d…、b908645a…、967b02a0…），txt 为有损检索稿
- 发布日期：指南为滚动页、首次发布日未核（指南正文自称覆盖 Opus 5.5 专属模式；不沿用发布文日期冒充）；发布文 2026-09-22（正文标注）；METR 2026-09-22（正文标注）
- 主张实质更新日期：未知（滚动页）
- 数据/事件观测窗口：指南与发布文的厂商测试运行日期未公开；METR API 测试为 10 个工作日（文中自述，具体日期未给）
- 当前适用状态：有条件（接口事实+厂商指导）；效果主张均未独立验证
- 工件/配置/预算及复现范围：三份正文全文阅读（发布文含基准表与客户证言全部）；原批未读migration guide/system card/preserved thinking/Gray Swan；主审10-16补读migration的禁用接口段与preserved thinking相关段，system card/Gray Swan仍未读
- 阅读覆盖与媒介限制：正文全文；图表只读文字表格与注释，未核图像像素
- 版本日期：2026-10-14 抓取版本
- 利益关系与独立性：指南+发布文为 Anthropic 厂商材料（同一材料组计 1 源，营销渠道纪律适用）；METR 为独立机构但无偿协议、Anthropic 可审阅编辑文字、METR 最终签署（文中自述）
- 复核触发器：下一代模型发布；Sonnet/Haiku 5.5官方指南截至10-16已可访问，进入各自模型复核；指南实质修订；preserved thinking 政策变化；最迟 2027-04 前查新据
- 检索日期：2026-10-14
- 作者/机构：Anthropic（指南、发布文）；METR（评估）
- 适用模型：Claude Opus 5.5（明确模型专属）；对照涉及 Opus 5、Fable 5.1
- 证据等级：接口事实=可检验结论；能力/效果主张=厂商经验断言；METR 结论=独立机构经验断言（非注入防御证据）
- 框架落点：prompt 治理 / harness 治理 / 安全；Q-001 观测
- 关联条目：M-002/M-036/K-013/M-047（存废对照）；M-021/M-034（注入防御）；M-033（长运行 harness 早停）；K-011（平台化观测）

## 一句话结论

Opus 5.5 官方延续"旧提示基本可用"并记录部分处方需要删除或重测（thinking禁用接口已移除，相关提示补丁分别删除或重测），但同一份指南列有至少六类本批选取的提示/harness模式（本代是否新增未核）——证据支持"部分处方失效或需重测，且平台约束发生变化"（未测过期速度），不支持"脚手架随模型能力消失"的单向叙事。

## 要点摘录

（引号内逐字取自 2026-10-14 抓取正文。）

### 代际延续与 breaking changes

- 指南："Existing Claude Opus 5 prompts should perform well without changes, and the patterns in Prompting Claude Opus 5 remain a reasonable starting point."
- 指南明示 4 项 breaking API changes（细节在 migration guide，本批未读）；本批正文确认其中之一："Claude Opus 5 accepts thinking: {"type": "disabled"} at high effort or below; Claude Opus 5.5 doesn't"
- 发布文确认：thinking 模式不可再关闭（原文 "no longer available with 'thinking' mode switched off"，弯引号为原文形态）

### effort 治理（提示层→设置层迁移）

- "Effort is the main control for how much Claude Opus 5.5 thinks, and because thinking is always on, it's the first setting to adjust when trading off intelligence, latency, and cost."
- "Effort level names don't correspond to the same amount of thinking across models"——同档名跨模型不等思考量；Opus 5.5 默认 medium（Opus 5 默认 high）。
- "Lowering effort reduces thinking, and with it cost and latency, more reliably than prompt instructions do."——[我方推导] 控制权从提示层迁移到 API 参数层的厂商口径。
- 缓存约束："Changing the top-level effort value between requests invalidates the prompt cache. To change the level partway through a conversation, use a per-message effort change (beta) instead"

### 旧补丁的删除与重测（少脚手架主张的精确范围）

- "Remove instructions that stood in for thinking."（推理复述指令；且 pushing 模型在响应中复现推理可能触发 reasoning_extraction refusal）
- "Re-test the thinking-disabled mitigations."（为禁思考加的组合指令：是否仍需要逐项检查）
- chat 场景："removing such a line made replies start sooner, with no clear decline in the quality of the reply"（think carefully 类行）
- 视觉输入："re-test whether you still need scaffolding you built for visual inputs on earlier models"
- [我方推导] 以上均为"模型特定行为补丁"的删除/重测，指南同时要求保留权限类检查（见下）。

### 当前指南列出的脚手架（是否本代新增未核）

1. 早停防护：unattended agent 把 text-only end_turn 误判为完成；对策为 checklist+点名续跑+"stop after two or three automatic continuations on the same task rather than repeating them indefinitely"+完成条件独立检查（可用更小模型）
2. 进度更新渲染：progress-update thinking blocks 需 display: "updates" 才可见；harness 可数连续静默工具步并注入提醒（"The user hasn't heard from you in a while…"）
3. 多 app 探索指令："Before taking any action, explore broadly with tool calls…"——"Claude Opus 5.5 completed noticeably more of them correctly with this instruction, at both medium and max effort, at the cost of slightly more tool calls and tokens"
4. 多 agent 时间信号："elapsed 340s / 1200s"——"The model paces its work to finish inside the budget"；"The budget is advisory and nothing stops the model at the limit, so if you need a hard stop, keep your own timeout"
5. 粘贴内容标记协议：<pasted_content id="…"> 同 ID 包裹+系统提示说明——"The tags are plain text and can be imitated, so treat this as one guardrail alongside other prompt-injection defenses"
6. 前端样式具体禁令（named patterns，替代"avoid a generic AI look"泛指令）

### 指南仍要求权限检查（不据此测量能力吸收）

- 早停防护段落明示："This does not override the need for confirmation on risky or destructive actions."
- "keep your own timeout"（时间预算不替代 harness 硬停）
- "keep untrusted content out of the records it searches"（多 app 探索指令的前提）

### preserved thinking（新平台约束）

- 发布文："It stops API users from editing Claude's prior context in an attempt to extract Claude's reasoning."（反蒸馏 safeguard，原文明示 "It applies to Fable 5.1 and Opus 5.5 for API accounts created on or after August 31, 2026"）
- 指南侧约束：中途改系统提示/工具集会使早期 thinking 块失效（"invalidates the conversation's earlier thinking blocks"）
- [2026-10-16补读纠正] preserved thinking约束的是历史thinking块与前缀的绑定，不是禁止所有历史编辑或压缩。编辑早期system/tools/messages可使后续thinking失效；文档列出drop_block、移除失效thinking和服务端/客户端压缩等处理。具体执行取决于模型、账户、模式、平台及header；补读范围见docs26，未跑API。外部笔记若被重新渲染进旧消息仍可能改变前缀，不能因存储在文件就一概称无影响。

### 厂商能力主张（全部未独立验证）

- 注入防御："It is much less likely than recent models to take hard-to-reverse actions or act outside the boundaries it's been given, and it's more resistant than Opus 5 to prompt injection."；第三方引用："On a benchmark run by the AI security firm Gray Swan, Opus 5.5 ties Fable 5.1 for the lowest prompt injection success rate of any model tested."（Gray Swan 原报告未读）
- 遏制边界（新评测）："Opus 5.5 attempted to circumvent boundaries around 85% less often than Opus 5 or Claude Mythos 5.1, and every attempt it made was low severity and self-reported."
- 评测挑战："We see signs that Opus 5.5 often suspects it is being evaluated"
- 基准表限制自述：safeguard 干预时 cybersecurity 任务由 Opus 4.8 完成、biology 与 frontier LLM development 任务由 Opus 5 完成（原文三项并列）；AutomationBench 由 Zapier 跑且"without fallback models"；WANDR 设置与公开榜不可比；Terminal-Bench 4.0 SE ±2.6pts

### METR 评估的用途边界（重要纠正落实）

- 范围声明（逐字）："our work was oriented around collecting evidence related to AI R&D capabilities but was not meant to verify claims about compliance with any specific threshold from Anthropic's policies. This report summary also does not attempt to assess whether Claude Opus 5.5 has or does not have particular alignment properties."
- 独立性："We drafted the initial summary, and then Anthropic had the opportunity to review and edit the text. We signed off on this final text from the Claude Opus 5.5 system card."
- 结论 A："We believe that acceleration from this model would be slightly higher than for Fable 5.1, but that this model is unlikely to be able to fully automate AI R&D"——"The evidence we have does not suggest"判断/品味（"researcher 'judgement' or 'taste'"）类技能有大幅改进（证据未显示，非证明确实没有）
- 结论 B：开发"at least somewhat accelerated by AI but is unlikely to have been dramatically accelerated"（内引加速报告"~1.5X overall acceleration…perhaps 30% chance of 2X"，期间未指明）
- [我方推导] 该评估不构成提示注入防御、提示方法优效或任何业务效果主张的独立验证；其对本库价值限于：METR在所审AI R&D任务与信息范围内预期加速略高于Fable 5.1、尚不太可能完全自动化AI R&D，现有证据未显示研究判断/品味大幅改进。不能由此确认所有代际能力改进幅度、长时程判断缺口或某项harness对策的必要性。

## 旧指导存废表（本批核心交付）

| # | 旧条目/主张 | 旧适用模型 | Opus 5.5 新证据 | 裁决 |
|---|---|---|---|---|
| 1 | M-047：大幅删减系统提示后内部编码评测无测得损失 | Opus 5 / Fable 5（Claude 5 代） | 官方延续同方向：删推理复述指令（refusal 机制强制）、禁思考补丁重测、think-carefully 行建议删 | **方向延续+范围收窄**：适用于"模型特定行为补丁"；M-047 保持候选级，Opus 5.5 补强其方向但不提供独立复现 |
| 2 | "thinking可禁用"接口，以及禁用模式的提示缓解措施（分项处理） | Opus 5（高 effort 以下） | 接口移除（"Claude Opus 5.5 doesn't"）+ preserved thinking | **接口对Opus 5.5废止**；禁思考提示按指南删除；其他缓解组合按任务重测，不能全部判废止 |
| 3 | M-002：right altitude、最小工具集、hybrid 检索、compaction/笔记/子 agent | 泛 Claude 系 | 无矛盾；多 app 探索指令与 agentic search 同向；preserved thinking限制旧thinking块复用；允许合规压缩，文件加载若改写旧前缀仍受约束 | **保持**（候选级不变） |
| 4 | M-002 作者预测："Smarter models require less prescriptive engineering" | 泛 | 同页建议删/重测部分补丁并列有≥6类当前机制，新增归属未核；控制权从提示层移到 API 层而非消失 | **不支持单向趋势**；Q-001 按条件化记录（见下） |
| 5 | M-036/K-013（OpenAI 侧：矛盾敏感、Markdown 重注入、compaction 端点） | GPT-5/5.2 | 不受影响；注意两家均有官方"延续"声明叙事（GPT-5.2 "largely carries over" ↔ Opus 5.5 "should perform well without changes"）——延续声明是厂商口径手法，不是效果验证 | **保持历史用途**；跨厂商延续声明互不验证 |
| 6 | [新增裁决] 跨模型沿用 effort 设置 | — | 默认档变化（high→medium）+同档名不等思考量+改值失效缓存 | **新增**：换模型须用自家 evals 重测 effort；跨模型沿用为反模式 |

### Q-001 条件化观察（不构成能力吸收的因果验证）

- 吸收方向（补丁过期）：thinking禁用接口（平台行为变更，不等同模型能力吸收）；推理复述指令（refusal 强制）；视觉输入脚手架（能力增强后建议重测）；提示层控思考（不如 effort 参数可靠）；注入抵抗增强（厂商自报+Gray Swan 引用）
- 并存观察（当前指南仍列脚手架，代际新增未核）：早停防护、进度更新渲染协议、多 app 探索指令、多 agent 时间信号、粘贴标记协议、前端具体禁令；preserved thinking 新增历史编辑约束
- [我方推导] 计数口径：六类指指南"Unattended agentic runs / User-facing progress updates / Explore context / Time signals / Mark pasted text / Frontend design defaults"六节的当前模式（本代新增未核）；Safeguard refusals 应对、per-message effort (beta) 等同页机制未计入——六类是选择性下限而非全集。且"新增"归属仅依据指南自称覆盖 "specific to Claude Opus 5.5"，未对照 Prompting Claude Opus 5 旧指南（未读）验证哪些确为本代新增。
- 结论：本批证据形态="部分补丁需重测 + 平台接口/约束改变 + 当前治理机制并存"，未测过期速度或总治理量。不采纳"少脚手架=少治理"；继续维持"模型专属指导带适用模型字段+换代触发器"的既有设计。

## 影响入口处置（已执行）

| 入口 | 处置 |
|---|---|
| principles/ 核心与细则 01-08 | grep 确认无模型专属处方渗入正文（无 thinking/effort/禁思考类引用）；**不改** |
| principles/07_evidence.md | 新增本批来源登记与限制（v0.14 增量节） |
| notes/M-047 | 加 Opus 5.5 复核注记（方向延续+范围收窄+接口变化） |
| notes/M-002 | 加 preserved thinking 边界轻注记（旧thinking复用需匹配前缀，文件笔记加载也须核实际装配） |
| notes/K-013、M-036 | OpenAI 侧不动（不同厂商模型；延续声明对照已在存废表#5 记录） |
| graph/overview.md | "当前证据边界"补 Claude 5.5 代对照复核完成一句 |

## 适用条件与反证

- 适用条件：仅Opus 5.5；2026-10-16已可访问Sonnet/Haiku 5.5官方指南，另需分别复核，不能外推家族；指南为厂商指导，接口事实与效果主张分开对待
- 反证/局限：
  - 作者自认（发布文）：基准由 fallback 模型完成部分任务、第三方跑分设置不可比、"often suspects it is being evaluated"削弱行为评测效度
  - 独立边界（METR）：不评 alignment/注入防御；部分内部加速证据未向评估团队共享；Anthropic 可审阅编辑
  - 我方限制：原批次未读migration guide、system card、Gray Swan、preserved thinking；10-16本轮补读migration的禁用接口段及preserved thinking绑定/编辑/压缩/错误处置相关段，仍未读其余全文；指南首次发布日未核（滚动页）
  - [我方推导]"六类当前机制"是本批计数，不能据此确认本代新增，依据指南小节结构；未来指南重组时须重数，不是稳定统计量

## 与已有条目的关系

- M-047：最强对照——其"删减无测得损失"获同厂商后续方向佐证，但范围被本批收窄为"模型特定补丁"
- M-002：Q-001 预测的同厂商后续材料对照：有补丁重测与接口变化，不能从指南机制计数证明或反证模型吸收总量
- M-033（长运行 harness）：早停现象+harness 对策（checklist、续跑上限、后台任务等待）为直接补充证据
- M-021/M-034（注入/遏制）：粘贴标记协议=提示层防御新工件；"越界尝试少 85%"为遏制主题厂商自报新据（未经独立验证）
- K-011/K-013（平台化观测）：preserved thinking、effort 参数化、进度更新 beta 头均属"治理点进平台"轨迹

## 后续动作

- [ ] 需要复现的主张：早停现象可在本地任一 agent 循环上观察（text-only end_turn 被误判为完成）；无需付费 API 即可审 harness 侧对策逻辑
- [ ] 需要补读的反方/正方：migration guide（4 项 breaking changes 细节）、Opus 5.5 system card（METR 引用源）、Gray Swan 注入基准原文、preserved thinking 文档；Sonnet/Haiku 5.5官方指南已可访问，分别复核其专属建议
- [ ] 复核触发器：Claude 下一代发布；指南实质修订；preserved thinking 范围变化；2027-04 前查新据

## 2026-10-16 主审纠正

原稿把全部禁用缓解处方判废止、把六类写成已证本代新增、把preserved thinking概括为禁止历史编辑，均超出原阅读范围，已同步当前正文/存废表/入口。旧稿见notes/_review_archive/2026-10-16-before-batch15-master。当前指南与接口事实可保留；Q-001仍是参考假设，不作本轮已证实/反证结论。新增原文仅相关段补读，不称整批重采全文。

## 2026-10-18 本地整固纠正

回查已有指南与METR原文相关段：移除一句话结论中的“加速/快速过期”，不再由AI R&D有限评估推总体代际幅度或早停机制必要性。未取新网页或运行API，接口资料仍是10-14/10-16快照；新的当前性核验交下一采集执行单。旧稿已归档。

## 2026-10-18 当前性复查与家族复核完成（M-096）

本页指南/migration/preserved-thinking 三页 2026-10-18 重抓，提取文本与 10-14/10-16 快照逐字一致（HTML 哈希变化为非内容层）；接口事实未见变更。Sonnet 5.5 与 Haiku 5.5 专属指导已由 [M-096](M-096_sonnet_haiku55_model_review.md) 完整复核：存废表 #2（thinking 控制）为三模型三种接口，#6（跨模型沿用 effort=反模式）升至三模型一致厂商指导。保留本页Opus专属范围；#2不能推到三模型均删除思考提示，#6是同厂商指引一致而非三份独立实验。
