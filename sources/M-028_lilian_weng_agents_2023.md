# M-028 LLM Powered Autonomous Agents（2023 奠基性综述）

## 元信息

- 来源链接：https://lilianweng.github.io/posts/2023-06-23-agent/
- 原文快照（供复核）：https://web.archive.org/web/20261010032638/https://lilianweng.github.io/posts/2023-06-23-agent/
- 发布日期：2023-06-23
- 检索日期：2026-10-13
- 作者/机构：Lilian Weng（OpenAI 研究者个人博客，行业公认综述）
- 适用模型：GPT-3.5/4 时代模型（文内案例 AutoGPT、BabyAGI 等均基于此）
- 证据等级：可检验结论（综述汇编，非原始实验；其引用的 ReAct/Reflexion 等各有论文）
- 框架落点：harness 治理（规划/工具）+ 上下文治理（记忆映射）——三层框架的 2023 前身
- 关联条目：Q-001（本文=吸收假设的"起点快照"）；M-001（workflows vs agents 之前的分类学）；K-002（有限上下文挑战的最早表述之一）；M-014（外部记忆）

## 一句话结论

2023 年的学科起点文档：agent = 规划 + 记忆 + 工具使用三组件（LLM 为核心控制器），而其"挑战"清单（有限上下文、长程规划脆弱、自然语言接口不可靠）恰好是此后三年 prompt/上下文/harness 三层治理要解决的问题——本文是 Q-001 观测的**基线快照**。

## 要点摘录（引文逐字取自当次抓取）

### 三组件分类学

- 开篇定位："Building agents with LLM (large language model) as its core controller is a cool concept."，LLM "can be framed as a powerful general problem solver."
- 任务分解三途径（原文列举，逗号前空格为原文标点风格）："(1) by LLM with simple prompting like \"Steps for XYZ.\\n1.\", \"What are the subgoals for achieving XYZ?\" , (2) by using task-specific instructions; e.g. \"Write a story outline.\" for writing a novel, or (3) with human inputs."
- ReAct（推理+行动耦合）："In both experiments on knowledge-intensive tasks and decision-making tasks, ReAct works better than the Act-only baseline where Thought: … step is removed."（"Act" 在原文为 code 元素，渲染无空格）
- Reflexion 的启发式：失败轨迹（低效规划/幻觉循环）触发自省，反思"are added into the agent's working memory, up to three, to be used as context for querying LLM."

### 记忆映射（上下文治理的 2023 话语）

- "Short-term memory as in-context learning. It is short and finite, as it is restricted by the finite context window length of Transformer."
- "Long-term memory as the external vector store that the agent can attend to at query time, accessible via fast retrieval."
- "The external memory can alleviate the restriction of finite attention span."

### 挑战清单（Q-001 基线观测点）

- 有限上下文："The restricted context capacity limits the inclusion of historical information, detailed instructions, API call context, and responses."；即便有检索，"their representation power is not as powerful as full attention."
- 规划脆弱："LLMs struggle to adjust plans when faced with unexpected errors, making them less robust compared to humans who learn from trial and error."
- **自然语言接口不可靠（2023→2026 变化最剧烈的一项）**："the reliability of model outputs is questionable, as LLMs may make formatting errors and occasionally exhibit rebellious behavior (e.g. refuse to follow an instruction). Consequently, much of the agent demo code focuses on parsing model output."

## 案例区块

- 实践者与约束：2023 年语境——无原生工具调用（function calling 2023-06 才随 GPT-3.5-turbo-0613 推出 [外注：发布时间属外部知识]）、上下文窗口 4k~32k 量级 [外注：2023 年主流模型窗口量级，属外部知识，原文无此数字]。
- 具体做法：综述汇编（AutoGPT/BabyAGI 案例研究、科学发现 agent、Generative Agents）。
- 报告的效果：N/A（综述）。
- 对我们的可复现性：作为**历史基线**使用：把挑战清单与 2026 年现状逐项对照（区分模型行为变化、平台托管和问题仍存在；不计量吸收进度）。

## 适用条件与反证

- 适用条件：仅作历史文档引用；任何方法论引用须先核对 2026 年模型是否已改变前提。
- 反证/局限：
  - 三组件分类学是描述性框架，非机制理论；2025-2026 的工程文献（M-001 等）已转向 workflows/agents 与治理分层话语。
  - 向量检索≈长期记忆的映射被后续实践修正（M-002/M-014：结构化笔记+文件系统替代纯向量检索的潮流）。
  - 我方怀疑：文内自述记忆一节由 ChatGPT 协助起草（作者自己注明），引用该节时按二手综述对待。

## 与已有条目的关系

- **Q-001**：登记为**基线快照**——挑战清单的每一条都可用 2026 现状复测（格式错误→原生 JSON/工具调用；上下文焦虑→M-029 记录的跨代消失）。这是历史问题清单对照，不能比受控实验更直接地测量吸收，也不能由平台功能存在证明工程需求消失。
- **M-001**：三组件是 agent 内部解剖，M-001 是外部结构选择，互补不冲突。
- **K-002**：有限上下文挑战的早期清晰表述之一。
- 与 docs/01 时间线的 2022—2023 思想源头节点对齐（本条补齐该节点的一手笔记）。

## 后续动作

- [ ] 需要复现的主张：无（历史文档）。
- [ ] 需要补读的反方/正方：所引 ReAct/Reflexion/Tree of Thoughts 原论文（如需引用其数字）。
- [ ] 复核触发器：仅作基线，无需复核；Q-001 年度观测时引用本文对照。


## 2026-10-14 正文一致性纠正

撤回“比跑分更干净”和直接度量吸收进度的解释；只保留历史问题清单。依据既有docs08/总纲Q001裁决，未新增来源验证；旧版已归档于_review_archive/2026-10-14-batch13/notes/。
