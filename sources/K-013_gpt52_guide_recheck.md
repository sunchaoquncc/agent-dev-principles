# K-013 GPT-5.2 Prompting Guide（代际复核 + compaction 平台化）

> 当前用途（2026-10-14）：以下保留来源当时的做法与作者主张，仅作历史/自我修订对照；不将旧型号处方或旧“认可”记录作为现行要求。当前原则状态见[证据登记](../principles/07_evidence.md)，效果仍未验证。

> **2026-10-13审查勘误/适用范围（优先于下文历史解读）**：2025-12指南超新鲜度线，不能逐项背书当前模型。此前未找到GPT-6/6.1是检索遗漏，不可推断未公开；当日官方正文已列GPT-6.1 Sol，见docs/08及快照。

## 元信息

- 来源链接：https://cookbook.openai.com/examples/gpt-5/gpt-5-2_prompting_guide（源文件：https://raw.githubusercontent.com/openai/openai-cookbook/main/examples/gpt-5/gpt-5-2_prompting_guide.ipynb）
- 原文快照（供复核）：Wayback 登记中；**有效证据=2026-10-13 直抓源文件本地存档** `notes/_snapshots_local/gpt52_prompting_guide_2026-10-13.ipynb/.txt`（提交历史经 GitHub API 核：2025-12-11 创建、2025-12-12 最后修订）
- 发布日期：2025-12-11~12（GitHub 提交历史核实）
- 检索日期：2026-10-13
- 作者/机构：OpenAI
- 适用模型：GPT-5.2（明确模型专属）
- 证据等级：可检验结论（官方指南）
- 框架落点：prompt/上下文治理（compaction 平台化）；Q-001 观测
- 关联条目：M-036（上一代指南——本篇为其复核触发）；M-037/规则 26；M-014；M-010/M-015；K-002

## 一句话结论

用户点破时效问题后的代际复核：官方声明 GPT-5/5.1 指南"largely carries over"，指令遵循在 5.2 继续增强（这是作者当代能力描述，未量化矛盾损害）；最大新事物是 **compaction 成为平台端点**（/responses/compact，有损感知压缩，不透明加密项）——上下文治理被吸收进 OpenAI 平台的 Q-001 标记事件。

## 要点摘录（引文逐字取自当次抓取）

### 代际延续性（对 M-036/M-037 的复核结论）

- "Existing GPT-5 / GPT-5.1 prompting guidance largely carries over and remains applicable."
- 行为变化："**Stronger instruction adherence:** Less drift from user intent; improved formatting and rationale presentation."——这是作者对GPT-5.2的描述，不构成普遍跨代趋势或矛盾损害对照。
- 另有："**More deliberate scaffolding:** Builds clearer plans and intermediate structure by default"；"**Conservative grounding bias**"；"**Generally lower verbosity**"。

### 长上下文：该旧指南的摘要与重扎根建议

- "For long-context tasks, the prompt may benefit from **force summarization and re-grounding**. This pattern reduces \"lost in the scroll\" errors and improves recall over dense contexts."
- 模板要点：先列相关节内提纲；"Re-state the user's constraints explicitly (e.g., jurisdiction, date range, product, team) before answering"；答案锚定到具体章节。

### Compaction 平台化（Q-001 观测）

- "GPT-5.2 with Reasoning supports response compaction via the /responses/compact endpoint. Compaction performs a loss-aware compression pass over prior conversation state, returning encrypted, opaque items that preserve task-relevant information while dramatically reducing token footprint."
- 性质："Designed for continuation, not inspection"；"Treat compacted items as opaque; don't parse or depend on internals"
- 最佳实践："Compact after major milestones (e.g., tool-heavy phases), not every turn"；"Keep prompts functionally identical when resuming to avoid behavior drift"——与 M-015（过激压缩警告）、M-033（里程碑节点）跨厂商同向。

### 歧义与幻觉风险（提示层缓解）

- 不确定时（原文两行列表项）："Ask up to 1–3 precise clarifying questions, OR
  Present 2–3 plausible interpretations with clearly labeled assumptions."；"Never fabricate exact figures... when you are uncertain."（省略号为我方截断）
- 高风险自检模板：法律/财务/合规场景收尾前重扫自己的答案（未声明假设/无锚定数字/过强措辞）。

## 适用条件与反证

- 模型绑定 GPT-5.2（2025-12 代际）；本笔记在库内的首要用途=**M-036/M-037 的复核证据**与新观测登记，不是现行通用指导。
- 我方渠道未找到 GPT-6/6.1 官方提示指南（cookbook 最新目录即 gpt-5；GitHub 提交活跃至 2026-10）；此为旧检索遗漏，不可推测未公开；当前官方已取得GPT-6页面——本条适用模型字段与"下一代发布"触发器照常生效。
- 局限：指南未量化各主张；compaction 端点细节看 Conversation State 文档（未读）。

## 与已有条目的关系

- **M-036**：记录2025-12的延续声明；不是逐项效果验证或当前模型复核通过。
- **M-037/规则 26**：旧候选的历史关联；2026-10-13仅文献审查日，不能更新模型效果验证日期。
- **M-014**：OpenAI旧代指南的复述相关建议（与其他OpenAI来源不重复计独立方）（force re-grounding + re-state constraints）。
- **M-010/M-015**：compaction 里程碑式触发+恢复时提示不变的官方建议。
- **Q-001**：观测表 +1——compaction 平台端点化（OpenAI 侧，与 Anthropic tool result clearing/memory tool 同轨迹）。

## 后续动作

- [ ] 需要复现的主张：无（指南类）。
- [ ] 需要补读的反方/正方：Conversation State/Compact API 文档；gpt-5-1 指南（演化中点）；当前GPT-6/6.1指南已取得见docs08，实际目标模型仍须按任务检查。
- [ ] 复核触发器：旧指南已超六个月，只作历史；目标模型换代或取得实质新据时检查，不从检索日顺延至2027-04。


## 2026-10-14 正文一致性纠正

按既有docs08/总纲裁决及本篇内部证据限制，同步正文中的旧强断言、状态或阅读范围；未重抓来源、未新增效果验证。修改前文本见[_review_archive/2026-10-14-batch13/notes/K-013_gpt52_guide_recheck.md](_review_archive/2026-10-14-batch13/notes/K-013_gpt52_guide_recheck.md)，仅供历史追溯。
