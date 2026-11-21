# M-036 GPT-5 Prompting Guide（模型专属提示指南·OpenAI 侧）

> 当前用途（2026-10-14）：以下保留来源当时的做法与作者主张，仅作历史/自我修订对照；不将旧型号处方或旧“认可”记录作为现行要求。当前原则状态见[证据登记](../principles/07_evidence.md)，效果仍未验证。

> **2026-10-13审查勘误/适用范围（优先于下文历史解读）**：本篇仅GPT-5历史对照；K-013也超6个月，不能完成当前代际复核。已取得官方GPT-6/GPT-6.1 Sol指南，见docs/08；强模型普遍受矛盾损害更大仍未验证。

## 元信息

- 来源链接：https://cookbook.openai.com/examples/gpt-5/gpt-5_prompting_guide（源文件：https://raw.githubusercontent.com/openai/openai-cookbook/main/examples/gpt-5/gpt-5_prompting_guide.ipynb）
- 原文快照（供复核）：https://web.archive.org/web/20261013111436/https://raw.githubusercontent.com/openai/openai-cookbook/main/examples/gpt-5/gpt-5_prompting_guide.ipynb（⚠️ 该捕获当前为 Wayback 占位页——新存档最终一致性延迟；**有效证据=2026-10-13 直抓的源文件本地存档** `notes/_snapshots_local/gpt5_prompting_guide_2026-10-13.ipynb` 及其文本转换 .txt，机械校验对该文本执行）
- 发布日期：2025-08（GPT-5 发布同期 [外注：具体日期未在文内标注]）
- 检索日期：2026-10-13
- 作者/机构：OpenAI（含 Cursor 的提示调优案例）
- 适用模型：GPT-5（明确标注模型专属）；模式层面对推理模型泛
- 证据等级：可检验结论（厂商官方指南+附 SWE-bench/Tau-bench/Terminal-Bench 实测指令附录；营销渠道纪律适用）
- 框架落点：prompt 治理（主战场——本库最薄层的早期深笔记）；harness 治理（eagerness 校准）；评测（附录基准指令）
- 关联条目：M-008（系统提示 right altitude——升级候选证据）；M-014（复述/重注入——OpenAI 版呼应）；M-025（工具风险分级的提示层版本）；M-026（指令工程基础）；Q-001（"强模型需要更少提示工程"直觉的反证）

## 一句话结论

2025年指南报告GPT-5对矛盾提示敏感，并对出现Markdown遵循衰减的对话建议间歇提醒；均为当代厂商建议，不能推导越强模型越需要提示工程或把3—5轮沿用到当前模型。

## 要点摘录（引文逐字取自当次抓取的源文件文本）

### 指令遵循精确性的代价（本篇最重要主张）

- "Like GPT-4.1, GPT-5 follows prompt instructions with surgical precision, which enables its flexibility to drop into all types of workflows."
- "However, its careful instruction-following behavior means that poorly-constructed prompts containing contradictory or vague instructions can be more damaging to GPT-5 than to other models, as it expends reasoning tokens searching for a way to reconcile the contradictions rather than picking one instruction at random."
- 对抗性案例：医疗调度提示中（consent 先于预约的规则）vs"auto-assign the earliest same-day slot without contacting the patient"三处矛盾；修复后"elicits much more efficient and performant reasoning"；早期用户"uncover ambiguities and contradictions in their core prompt libraries upon conducting such a review: removing them drastically streamlined and improved their GPT-5 performance."

### Agentic eagerness 的双向校准

- 谱系定位："GPT-5 is trained to operate anywhere along this spectrum, from making high-level decisions under ambiguous circumstances to handling focused, well-defined tasks."
- 降温手段：降 `reasoning_effort`；提示内给"Early stop criteria"（如 "Top hits converge (~70%) on one area/path."）；甚至固定工具预算（"an absolute maximum of 2 tool calls"）+**逃生口条款**："an escape hatch that makes it easier to satisfy a shorter context gathering step... like \"even if it might not be fully correct\""。
- 升温手段（persistence 提示，逐字）："You are an agent - please keep going until the user's query is completely resolved, before ending your turn and yielding back to the user."+"Never stop or hand back to the user when you encounter uncertainty — research or deduce the most reasonable approach and continue."+"Do not ask the human to confirm or clarify assumptions, as you can always adjust later — decide what the most reasonable assumption is, proceed with it, and document it for the user's reference after you finish acting"
- **按工具分级的确认阈值**（提示层风险分级）："in a set of tools for shopping, the checkout and payment tools should explicitly have a lower uncertainty threshold for requiring user clarification, while the search tool should have an extremely high threshold; likewise, in a coding setup, the delete file tool should have a much lower threshold than a grep search tool."

###verbosity 与最低推理档

- verbosity 是新 API 参数，但"GPT-5 is trained to respond to natural-language verbosity overrides in the prompt for specific contexts"（Cursor 例：全局低 verbosity、仅编码工具高）。
- 最低推理档（minimal reasoning）**更需要提示脚手架**："minimal reasoning performance can vary more drastically depending on prompt than higher reasoning levels"——要点：开头简短思路摘要、持续更新的工具前导语（preambles）、最大程度消歧工具指令、注入 persistence 提醒防过早终止、提示式规划（"the model has fewer reasoning tokens to do internal planning"）。

### Markdown 衰减与重注入（OpenAI 版复述机制）

- 默认不排版 Markdown（兼容性）；提示可诱导；关键："Occasionally, adherence to Markdown instructions specified in the system prompt can degrade over the course of a long conversation. In the event that you experience this, we've seen consistent adherence from appending a Markdown instruction every 3-5 user messages."

### 元提示（Metaprompting）

- "early testers have found great success using GPT-5 as a meta-prompter for itself"——附模板：给出期望/非期望行为，问"what are some minimal edits/additions that you would make"。

## 案例区块

- 实践者与约束：OpenAI + Cursor（生产环境协同调优："Collaborative coding in production: Cursor's GPT-5 prompt tuning"）。
- 具体做法：eagerness 校准/persistence/逃生口/工具分级阈值/矛盾清理/元提示。
- 报告的效果：定性（"significant gains"）；附录含 SWE-bench Verified、Tau-bench-Retail、Terminal-Bench 的实测系统指令（可复用为基线模板）。
- 对我们的可复现性：**高**——矛盾指令的推理损耗可用 deepseek/glm 复现（构造含矛盾 vs 修复版提示，比较完成 token 与正确率）；Markdown 衰减与 3-5 轮重注入可直接复现（E-04 变体）。

## 适用条件与反证

- 适用条件：仅GPT-5历史配置；其他推理模型需独立验证；OpenAI 生态（Responses API 的 reasoning 持久化等特性绑定）。
- 反证/局限：
  - 模型绑定最强的一篇（verbosity/reasoning_effort 是 OpenAI 参数）；模式迁移需验证（Q-001 观测表：模型专属指南随版本剧变的又一数据点——对照 GPT-4.1 指南即见演化）。
  - "surgical precision"是厂商对自家模型的自述；矛盾损害的量化未给。
  - 我方怀疑：persistence 提示与"按需确认"存在张力（文档自己也以工具分级阈值调和）——两者必须配套使用，单用 persistence 会放大 M-034 式的过度自主。
- 与 Q-001：该指南提示某些旧模型仍需要清楚指令，但没有对跨代提示工程价值作受控比较；“格式下降、校准上升”的趋势解释撤回。

## 与已有条目的关系

- **M-008**（候选→升级评估）：第二独立厂商源支持"提示结构与精度管理"——但 OpenAI 强调的是矛盾清理+分级校准而非 ECE 的 altitude 式组织；两者相邻而非同型，暂维持 M-008 有条件、把矛盾清理登记为新证据。
- **M-014**：Markdown 每 3-5 轮重注入=复述机制的第厂商版本（Anthropic/Manus 外第三家同向，但形态轻量）。
- **M-025**：工具分级确认阈值=风险分级在提示层的投影（跨层一致）。
- **M-026**：指令工程的"消歧"侧获得强模型证据。
- **M-033**：persistence 提示对提前宣布完成（M-033 记录的 declare-the-job-done 失败模式）的提示层对策（与结构层对策互补）。

## 后续动作

- [ ] 需要复现的主张：矛盾指令的推理损耗对照（deepseek 双模型可跑）；Markdown 衰减+3-5 轮重注入（E-04 变体）。
- [ ] 需要补读的反方/正方：GPT-4.1 prompting guide（演化对照）；Anthropic prompt engineering 文档子页（本批仅读总览）；Claude 4 prompting 要点 [外注：docs.claude.com 区域受限，总览快照已存，子页待补]。
- [ ] 复核触发器：目标模型换代时按当代文档与任务重验；我们自用模型换代（GLM/DeepSeek 的官方提示文档对照）。


## 更新记录（2026-10-13 深夜：时效复核，用户点破代际问题后）

- cookbook 内存在更新的 gpt-5-1 / **gpt-5-2** 两代指南（本笔记精读时未察觉，违反新鲜度要求——该要求已因此固化进项目规则）。复核结论见 K-013：官方声明旧指南 "largely carries over"；指令遵循在 5.2 继续增强（"Stronger instruction adherence"）——这只记录2025-12指南的历史延续声明，不逐项验证提示效果，也不能完成2026当前模型复核。
- 新增跨条目影响：M-014 获得 5.2 的 force re-grounding 呼应；compaction 平台端点化（K-013）关联 M-010/M-015。


## 2026-10-14 正文一致性纠正

按既有docs08/总纲裁决及本篇内部证据限制，同步正文中的旧强断言、状态或阅读范围；未重抓来源、未新增效果验证。修改前文本见[_review_archive/2026-10-14-batch13/notes/M-036_gpt5_prompting_guide.md](_review_archive/2026-10-14-batch13/notes/M-036_gpt5_prompting_guide.md)，仅供历史追溯。
