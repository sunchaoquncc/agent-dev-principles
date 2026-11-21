# M-019 OpenAI《A Practical Guide to Building Agents》

> 当前用途（2026-10-14）：以下保留来源当时的做法与作者主张，仅作历史/自我修订对照；不将旧型号处方或旧“认可”记录作为现行要求。当前原则状态见[证据登记](../principles/07_evidence.md)，效果仍未验证。

## 元信息

- 来源链接：https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf（HTML 版 openai.com/business-guides-and-resources/a-practical-guide-to-building-agents/ 于 2026-10-13 返回 404，已记冲突）
- 原文快照（供复核）：http://web.archive.org/web/20260923205316/https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf （PDF 二进制无法机械抽文本；引文经红队 2026-10-13 活页逐字核验）
- 发布日期：PDF 未标注日期（待核；不引用外部记忆断言）
- 检索日期：2026-10-13
- 作者/机构：OpenAI
- 适用模型：GPT 系（示例 o3、gpt-4o；指南按 OpenAI 生态写）
- 证据等级：经验断言（厂商指南；无受控实验；营销渠道属性同 Anthropic）
- 框架落点：harness 治理（编排模式、guardrails）为主；prompt 治理（指令最佳实践）；评测横切（evals 先行）；安全横切（guardrails 分层+工具风险评级）
- 关联条目：M-004、M-005、M-008、M-023、M-024、M-025；K-001；Q-003

## 一句话结论

OpenAI 侧与 Anthropic BEA 高度收敛（单 agent 起步、增量升级、evals 先行），增量贡献在 guardrails 工程化：分层防御 + 工具风险评级 + 人审触发条件。

## 要点摘录

（引号内为 PDF 原文逐字引文。）

### 定义（与 BEA 对照）

- "Agents are systems that independently accomplish tasks on your behalf."（agent=独立代表你完成任务的系统）
- 判别轴：LLM 是否指挥工作流执行——"If they integrate LLMs but don't use them to control workflow execution，they are not agents"（不指挥执行就不是 agent），只是 workflow（workflow 泛指达成目标的步骤序列，比 BEA 的"预定义代码路径"用词宽）。
- agent 核心特征：管理执行与决策、识别完成、主动纠错、失败时停止并移交控制（halt & transfer control）；工具访问；guardrails。

### 何时建 agent

- 判断复杂度：难以维护的规则、大量边缘案例、非结构化数据——满足其一再考虑 agent；确定性方案够用就不上。

### 三组件：model / tools / instructions

- 模型选择三步（**评测先行的官方表述**）："01 Set up evals to establish a performance baseline（先建 evals 定基线）02 Focus on meeting your accuracy target with the best models available 03 Optimize for cost and latency by replacing larger models with smaller ones where possible"——先用最强模型调通，再降档换小。
- 工具三类：Data（检索）、Actions（写）、Orchestration（把其他 agent 当工具调用）。
- 工具治理：标准化定义、文档化、可测试、可复用；**工具过载的判定不在数量在重叠度**："The issue isn't solely the number of tools, but their similarity or overlap. Some implementations successfully manage more than 15 well-defined, distinct tools while others struggle with fewer than 10 overlapping tools."
- 指令（prompt 层）最佳实践：从既有操作文档出发写指令、要求 agent 分解任务、每个场景明确边界行动、显式覆盖边缘案例。

### 编排：单 agent 优先

- 官方推荐："Our general recommendation is to maximize a single agent's capabilities first. More agents can provide intuitive separation of concepts, but can introduce additional complexity and overhead, so often a single agent with tools is sufficient."（先把单 agent 能力用满；多 agent 带来概念切分的同时带来复杂度与开销。）
- 客户经验："Most successful teams start with a single agent and incrementally add complexity as needs arise."（v0.2 勘误：初版引作 "customers typically achieve greater success with an incremental approach"，非原文。）
- 编排层工程细节（v0.2 补录，红队指出的遗漏增量）：orchestrator 作为用户唯一接口（隔离复杂度，子 agent 不直接暴露给用户）；orchestrator使用privileged model + privileged instructions（来源设计描述，不据此保证worker输出不会污染决策）；final escalation prompt 模式（给用户三个开放问题+兜底话术再转人工）；"request human input"作为显式工具、与 escalation（转人工接管）相区分；工具随 agent 演进需要持续维护（"as your agents evolve, their tools require maintenance"）。
- 拆分信号：条件分支过多（on the order of ten rules 的经验量级）、工具重叠/过载。
- 两模式：Manager（agents-as-tools，中心化）与 Decentralized（handoffs 对等传递）；无论哪种："keep components flexible, composable, and driven by clear, well-structured prompts."
- 边栏（框架观）：声明式图框架（预先定义每个分支）"can quickly become cumbersome"且要学 DSL——与 BEA"直接用 API 起步"同向。

### Guardrails（安全层，本篇最大增量）

- 总则：分层防御（LLM 分类器 + 规则/正则 + moderation API 并用），"Guardrails are a critical component of any LLM-based deployment, but should be coupled with robust authentication and authorization protocols, strict access controls, and standard software security measures."——guardrails 不替代传统安全。
- 分类器类型：相关性、安全（越狱/提示注入）、PII 过滤、moderation。
- **工具风险评级**（按低/中/高）考量维度：只读 vs 写、可逆性、权限范围、财务影响——高风险（不可逆/高权限/财务后果）→ 强制 pause for check 或升级人工。
- 人机干预触发：失败率阈值、高风险动作、高成本操作、敏感数据场景。
- 来源描述的执行策略：guardrail与主任务并行以降低串行延迟；这不保证敏感副作用前已通过检查，实际执行仍须设相应门闸（现版 PDF 相应小节名为 Parallelization；"optimistic execution"一词现版未见，疑出自 Agents SDK 文档语境 [外注·待核]）。

## 案例区块

- 实践者与约束：OpenAI 面向企业客户的部署经验总结（销售/支持场景示例）。
- 具体做法：三组件+两编排模式+guardrails 分层矩阵。
- 报告的效果：作者偏好增量部署方法，未提供可复算客户成功率对照；无第三方数据。
- 对我们的可复现性：guardrail 分层与工具风险评级可直接在本地 harness 实现（规则层零成本；分类器层需模型调用）；工具重叠度阈值（15 vs 10）可用 E-01 框架顺带测。

## 适用条件与反证

- 适用条件：GPT 生态；企业级部署（guardrails 章节明显面向合规环境）。
- 反证/局限：
  - 作者自认：多 agent 是"can provide intuitive separation"的权衡表述，非禁令——与 Cognition 原文比立场温和。
  - 我方怀疑：无任何上下文治理内容（KV-cache、compaction、context rot 全无）——OpenAI 侧对上下文治理的沉默与 Anthropic/Manus 形成版图差异（或因分发渠道为企业指南）；evals 只讲了"要做"没讲"怎么做"（Hamel/METR 谱系待补）。
  - 发布日期未标注，时效待核后回写。
- 与 Q-001 关系：AgentKit/Evals/RFT（2025-10-06 DevDay ✅ 已在观测表）是该指南体系化的产品化延续。

## 与已有条目的关系

- 与M-001在渐进增加复杂度等方面相邻收敛，术语差异保留；旧M-004/005认可仅历史记录，不等于效果独立验证。
- 单 agent 优先 + agents-as-tools 与 Cognition 修订版（M-017）、ECE 子 agent 三方收敛 → M-023。
- evals建议与BEA相邻；M-024旧认可已由现行有条件指导取代。
- guardrails与Willison历史威胁分析互补，不足以证明M-025各种实现普遍有效。
- 工具重叠度判定与 M-006/M-012 相关：给"最小工具集 vs 管理膨胀"（docs/07 D5）提供了 OpenAI 侧的中间立场（重叠是因素之一，不能排除数量、说明开销和任务分布的影响）。

## 后续动作

- [ ] 需要复现的主张：工具重叠度阈值（并入 E-01）；guardrail 分层的误报率（规则层可离线测）。
- [ ] 需要补读的反方/正方：发布日期核实（OpenAI 官方渠道/新闻稿）；OpenAI evals 产品文档（"怎么做"部分）。
- [ ] 复核触发器：AgentKit/Evals 产品迭代；GPT 旗舰版本发布；6 个月例行。


## 2026-10-14 正文一致性纠正

按既有docs08/总纲裁决及本篇内部证据限制，同步正文中的旧强断言、状态或阅读范围；未重抓来源、未新增效果验证。修改前文本见[_review_archive/2026-10-14-batch13/notes/M-019_openai_practical_guide.md](_review_archive/2026-10-14-batch13/notes/M-019_openai_practical_guide.md)，仅供历史追溯。
