# M-002 Anthropic《Effective context engineering for AI agents》

> 当前用途（2026-10-14）：以下保留来源当时的做法与作者主张，仅作历史/自我修订对照；不将旧型号处方或旧“认可”记录作为现行要求。当前原则状态见[证据登记](../principles/07_evidence.md)，效果仍未验证。

## 元信息

- 来源链接：https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- 原文快照（供复核）：https://web.archive.org/web/20251006000000/https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents（2025-10-05 快照，发布原貌）
- 发布日期：2025-09-29（页面 meta）；页面 modified 2026-01-06（经与 2025-10-05 快照比对，属微调，无内容性修订）
- 检索日期：2026-10-13（当日两次独立抓取 + Wayback 快照交叉核验，见 docs/06 #2）
- 作者/机构：Anthropic 工程博客；文末致谢署名 Applied AI 团队（Prithvi Rajasekaran 等）
- 适用模型：泛（context rot 论证基于注意力机制，跨模型；案例绑定 Claude 系列——Claude Code、Claude playing Pokémon、memory tool 公测绑定 Sonnet 4.5）
- 证据等级：经验断言为主；其中 context rot 子项为可检验结论（引用已发表的 needle-in-a-haystack 研究）
- 框架落点：上下文治理为主；prompt 治理（系统提示"right altitude"、工具描述、少样本）；harness 治理（子 agent 编排、检索工具设计）
- 关联条目：M-006、M-007、M-008、M-009、M-010、M-014；K-002、K-005、K-006；Q-001、Q-002
- 修订：2026-10-13 v0.2，依红队审查修正 6 处虚构引文/案例与 1 处立场反转（引文规则见 _template.md 硬约束）

## 一句话结论

上下文是有限资源（context rot + attention budget），工程师的工作是策划与维持"最优 token 集合"：系统提示取 right altitude、工具少而精、检索 just-in-time、长任务靠 compaction / 外部笔记 / 子 agent 三板斧。

## 要点摘录

（引号内文字为红队复核确认的原文逐字引文；其余为忠实转述。）

### 术语与定义

- 原文对 context engineering 的工作定义："Context engineering refers to the set of strategies for curating and maintaining the optimal set of tokens (information) during LLM inference."（策划并维持推理时的最优 token 集合。）
- 术语迁移：从 prompt engineering（打磨单条指令）演进为 context engineering——管理信息流以适配模型的有限注意力。
- ⚠️ 勘误记录（v0.2）：本笔记初版误将社区流传定义"right information, in the right format, at the right time"（溯源至临床决策支持"五个正确"，见二手源）当作原文定义并加引号。原文无此句。保留此记录作为信源纪律案例。
- agent 定义重申（与 M-001 一致）：LLM 自主在循环中使用工具。

### 核心问题：context rot 与 attention budget

- 观察：随上下文 token 数增长，模型对中置信息的回忆与推理退化（引用 needle-in-a-haystack 研究谱系）。
- 机制解释（作者给的假说）：注意力计算随 token 数呈平方级增长；训练数据以短上下文为主，长上下文上有效分配注意力的能力欠训练。
- 解法总纲：不塞更多，而是策划"最小高信号"集合。
- 边界声明（Q-001 证据）：原文明确"context windows of all sizes will be subject to context pollution"——窗口扩容不豁免上下文治理。
- 类比：作者用人类工作记忆（human working memory）作类比（初版误记为"乘客/飞行员"故事与"UX 之于人类应用"，原文无，已删）。

### 系统提示：right altitude

- 两个失败极端：过于脆（绑定具体格式的详细指令，模型更新即失效）与过于虚（含糊的高层指导，自由度过大）。
- 目标："right altitude"——足够高层以稳定、足够具体以可执行；用工具与数据而非死规则去约束边界行为。
- 组织：系统提示按功能区划分，用分隔标记（XML 或 Markdown 标题）帮助模型定位。
- 最小充分信息：minimal ≠ short——指"无冗余、无离题"，不是物理长度短。

### 工具：常驻上下文的固定开销

- 在作者讨论的工具常驻配置中，工具定义形成输入开销；是否最大、是否每轮常驻取决于实际请求与加载机制，不能泛化为所有系统。
- 最小工具集：先验证最小集合能跑通，再按需添加。
- 原文提及的 Claude Code 工具面：Bash（head/tail 读文件）、glob、grep、CLAUDE.md 预置文档、to-do list（完整工具枚举见 Claude Code 文档 [外注]，原文未全列）。

### 少样本：curated canonical examples

- 建议：给模型精选的 canonical few-shot examples——少量、多样、覆盖预期输入范围。
- 反模式：作者提醒示例会影响行为；“任何行为必然放大/示例即宪法”是旧笔记过强概括，撤回。
- ⚠️ 勘误记录（v0.2）：初版写"从 1,000 个正确摘要中选 10 个 canonical examples"，原文无任何数字，已删。

### 检索：agentic search 与 hybrid（初版立场反转，已修正）

- 推荐 agentic search：工具让模型交互式、按需取信息，而非预先计算塞满上下文（轻量标识符如文件路径/查询先行，运行时再取全量）。
- 渐进披露：按需读取更大分页；grep/glob 让模型自行决定暴露什么细节。
- metadata 即信号：目录结构、命名、时间戳本身是高信息密度上下文（对比向量库把语义埋进 embeddings）。
- **代价与混合策略（初版遗漏的另一半）**：原文明确写了 agentic search 的代价——更慢、可能浪费上下文追死胡同、需要引导；并推荐 hybrid："The hybrid strategy might be better suited for contexts with less dynamic content"（CLAUDE.md 预置文档 + glob/grep 即时检索并用，按上下文动态性取舍）。
- ⚠️ 勘误记录（v0.2）：初版写成"Claude Code 测试发现 agentic search 常优于预计算 RAG"，是对原文平衡论述的单边化，且反证节批评了一个原文没做过的主张。已按原文改为上述双向呈现。

### 长时程三种技术（含原文给的适用条件，初版遗漏）

1. **Compaction（摘要压缩）**：把对话摘要替换原历史；Claude Code 实现保留最近使用的 5 个文件。
   - 作者自己的警告："overly aggressive compaction can result in the loss of subtle but critical context"；调参法：compaction 提示先调 recall 再调 precision。
   - 适用条件（原文）：需要大量来回的对话流任务。
2. **Structured note-taking（结构化笔记）**：让 agent 把中间状态写成外部 note 文件，跨 compaction 存活、可跨会话复用。
   - 适用条件（原文）：有清晰里程碑的迭代任务。
3. **Sub-agent architectures（子 agent）**：任务分解给隔离上下文的子 agent。原文原话："the detailed search context remains isolated within sub-agents"。
   - 适用条件（原文）：并行探索有红利的研究型任务。
   - 量化结果（原文引）：其多 agent 研究系统 "showed a substantial improvement over single-agent systems on complex research tasks"；子 agent 间传递的是约 1,000—2,000 token 的压缩摘要。
- 平台内置化信号（Q-001 证据，K-005）：compaction 的最轻形式 tool result clearing 已上线 Claude Developer Platform；memory tool（跨会话持久记忆）随 Sonnet 4.5 进入公测。

### 案例：Claude playing Pokémon（初版失实，已修正）

- 原文实际内容：成功运行中，agent 用 memory/笔记记录进程（大意："for the last 1,234 steps…Pikachu has gained 8 levels"）；上下文重置后 agent 读取自己的笔记继续（"After context resets, the agent reads its own notes"）。
- ⚠️ 勘误记录（v0.2）：初版把案例写成"成功/失败运行对照实验"并附引文"context isn't just what's included…"——原文无此对照、无此引文。该案例只展示一次外置笔记后继续任务的作者报告，不能证明所有长任务都必须采用这一机制。

### 结论与作者自认的时效（引文经红队逐字核验）

- "As model capabilities improve, agentic design will trend towards letting intelligent models act intelligently, with progressively less human curation."
- "Smarter models require less prescriptive engineering, allowing agents to operate with more autonomy."（作者对未来人工策划需求的预测，不证明提示格式价值已普遍下降。）

## 案例区块

- 实践者与约束：Anthropic（Claude Code 与 Claude playing Pokémon；生产级编码 agent 与长时程游戏 agent）。
- 具体做法：hybrid 检索（预置+即时）、compaction（摘要+保留最近 5 文件）、外部笔记、子 agent 隔离+千 token 级摘要传递。
- 报告的效果：多 agent 研究系统对单 agent 有实质提升（作者自述其内部研究系统）；agentic search 与 hybrid 的取舍为定性建议；均无第三方复现。
- 对我们的可复现性：①context rot 本地复现（长上下文中置关键信息测回忆，E-02）；②compaction 保真复现（摘要替换历史后继续任务 vs 基线，E-03，可直接用原文 recall→precision 调参法）；③todo.md/外部笔记可另设计对照；现有E-04只测要求位置，不验证笔记或重复注入。

## 适用条件与反证

- 适用条件：长任务/多步 agent；上下文窗口与缓存计费构成真实约束的生产环境；检索型任务（hybrid 结论绑定文件系统类环境）。
- 反证/局限：
  - 作者自认：agentic search 有代价（慢、可能浪费上下文）；compaction 过激会丢关键细节；内容随模型版本演进快，作者预测人工策划需求可能下降，不能作为已观测的跨代通用趋势。
  - 我方怀疑：多 agent 提升的量化结果出自 Anthropic 自家研究系统，无第三方复现、无失败边界（Q-002 仍开放）；hybrid 取舍绑定代码任务域，对话式/非文件域未必成立。
  - 全文对 KV-cache 经济学只字未提——与 Manus（M-003）形成视角盲区互补。
- 与 Q-001 的关系：四条行为证据（见 overview 观测表）+ 边界声明"窗口扩容不豁免治理"。

## 与已有条目的关系

- 与 M-001 同厂商互补（harness ↔ context）；两篇同厂商按规则计 1 源（docs/03 v0.2 补则）。
- 与 M-003（Manus）汇合点：外部笔记（structured note-taking ↔ todo.md 复述，M-014）、"少而高信号"（M-007）、"窗口扩容解决不了上下文治理"（Q-001 反边界）。
- 与 M-003 分歧点：工具结果取舍（ECE 把清除旧工具结果视为低垂果实并已平台化 tool result clearing；Manus 要求失败动作的 stack trace 留在上下文）——同对象反向处方，见 docs/07 D1。
- 对 Q-002：正方证据（子 agent 隔离 + 多 agent 研究系统量化结果）。

## 后续动作

- [ ] 需要复现的主张：E-02 context rot、E-03 compaction 保真（用原文 recall→precision 调参法）、外部笔记须另设计实验（现有E-04不验证它）。
- [ ] 需要补读的反方/正方：Lost in the Middle（2023）原文；Cognition《Don't Build Multi-Agents》；Writing tools for agents（工具设计展开）；Anthropic 多 agent 研究系统原文（量化结果的出处与条件）。
- [ ] 复核触发器：memory tool 转正式版/范围扩大；Claude 大版本发布；6 个月例行。


## 2026-10-14 正文一致性纠正

按既有docs08/总纲裁决及本篇内部证据限制，同步正文中的旧强断言、状态或阅读范围；未重抓来源、未新增效果验证。修改前文本见[_review_archive/2026-10-14-batch13/notes/M-002_effective_context_engineering.md](_review_archive/2026-10-14-batch13/notes/M-002_effective_context_engineering.md)，仅供历史追溯。

## 2026-10-14 Opus 5.5 对照轻注记

2026-10-16主审纠正：preserved thinking限制旧thinking块与前缀的绑定，不是一律禁止历史编辑/压缩。改写前缀后需按模型/账户/API契约丢弃或移除失效thinking，服务端压缩等另有受支持路径；文件侧笔记若被写回旧消息也可能影响绑定。旧稿“外部文件一律不受影响”和“补丁层证实/脚手架层反证”均过强。M-090只提供后续材料对照，Q-001仍是参考假设，不能从接口变化量化模型吸收。旧稿已归档。
