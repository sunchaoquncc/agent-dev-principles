# M-001 Anthropic《Building Effective Agents》

> 当前用途（2026-10-14）：以下保留来源当时的做法与作者主张，仅作历史/自我修订对照；不将旧型号处方或旧“认可”记录作为现行要求。当前原则状态见[证据登记](../principles/07_evidence.md)，效果仍未验证。

## 元信息

- 来源链接：https://www.anthropic.com/engineering/building-effective-agents
- 原文快照（供复核）：https://web.archive.org/web/20241220000000/https://www.anthropic.com/engineering/building-effective-agents（2024-12 原版）
- 发布日期：2024-12-19（页面 meta，2026-10-13 核实）；页面 modified 2026-08-10（正文工具/模型清单已被 Anthropic 更新，见"要点摘录"首条）
- 检索日期：2026-10-13（当日抓取 + 2024-12 原版快照比对，见 docs/06 #2）
- 作者/机构：Anthropic 工程博客（页面未署名）
- 适用模型：泛（成文时示例为 Claude 3.5 系；2026 修订版正文已出现 Claude Sonnet 4.5、Claude Haiku 4.5、SWE-bench Verified 等更新内容）
- 证据等级：经验断言（基于"数十个客户团队项目"的观察归纳，无受控实验；厂商博客同时是营销渠道）
- 框架落点：harness 治理为主；评测横切（measure 原则、evaluator-optimizer 模式）；安全横切（沙箱测试+guardrails+checkpoint 反馈，点到为止）
- 关联条目：M-004、M-005、M-006、M-013；K-001、K-004、K-006；Q-001、Q-002、Q-003
- 修订：2026-10-13 v0.2，依红队审查删除 4 处虚构/错置内容（Cognition 引用、mock/监控/回放、ai-in-the-loop、案例拼装），修正细节归属

## 一句话结论

先从最简单的方案开始（单次调用 → workflow → agent 逐级升复杂度），只有当复杂度带来可度量的改善时才增加复杂度——agents 用延迟与成本换任务表现，是按需租用的自主性，不是默认架构（后半句为本文转述性概括）。

## 要点摘录

（引号内文字为红队复核确认的原文逐字引文；其余为忠实转述。）

### 编者注与修订状态（2026-10-13 检索时观察，经快照比对核实）

- 页面顶部编者注原文："Note: Much of the tooling landscape described in this post has changed since December 2024. For our current approach, see how we built Claude Managed Agents and the Managed Agents documentation."
- 经 2024-12 原版快照比对：原版推荐的框架为 LangGraph、Bedrock 等，现版已改为 "Claude Agent SDK; Strands Agents SDK by AWS; Rivet; Vellum"；模型示例已换为 4.5 系；SWE-bench Verified 为新出现内容。
- 处理：本笔记摘录以当前页面为主、关键处标注两版差异；**差异本身是 Q-001 的行为证据**（见 K-004）。

### 定义与分类学（Q-003 核心，正文部分）

- 构建层级（原文三层）：增强型 LLM（augmented LLM：retrieval、tools、memory）→ workflows → agents。原文并指出多数场景"optimizing single LLM calls with retrieval and in-context examples is usually enough"。
- workflows：用**预定义代码路径**编排 LLM（"orchestration of LLMs using predefined code paths"）。
- agents：LLM "dynamically direct their own processes and usage of tools, maintaining control over how it accomplishes tasks"（动态指挥自己的流程与工具使用，保持对任务完成方式的控制）；更宽泛的 agent 描述为 LLM 在循环中基于环境反馈使用工具（"tools based on environmental feedback in a loop"）。
- 五类 workflow 模式（正文展开，初版误标为"附录 1"，已改）：
  1. **Prompt chaining**：串行分步，每步一个 LLM 调用，可加检查门。适用：任务可干净分解、用延迟换精度。
  2. **Routing**：输入分类后进专用子流程；原文示例即客服——简单问询路由给更小/更便宜的模型（Haiku 4.5），困难问题给更强模型（Sonnet 4.5）（初版误写为"更小的提示"，已改）。
  3. **Parallelization**：sectioning（并行分片后合成）与 voting（多次运行取多数）。示例：一个实例处理用户请求、另一个并行筛查不当内容；代码审查用多个不同 prompt 分别查漏洞（初版"安全帽"例子为误记，已删）。
  4. **Orchestrator-workers**：中心 LLM 动态分解任务、分派 worker、综合结果。适用：子任务数量/内容无法预知（如需多源检索的代码修改）。
  5. **Evaluator-optimizer**：一个 LLM 生成、另一个循环打分修正。适用：有明确评价标准、迭代有增益（如文学翻译回炉）。
- agents 何时用：开放式问题、步数难以预知、问题空间需要探索；代价是以延迟与成本换任务表现（"trade latency and cost for better task performance"）。

### "从简单开始"的论证强度

- 原文建议（转述）：先找最简单的可行方案，只在需要时增加复杂度；用 workflow/agent 前先验证单次调用+检索+示例不够用。
- 论证方式：不是实验数据，而是成本-可控性论证——agents 灵活性换错误累积与调试难度；先原型、度量（"implement and measure"式表述），证明改善再升级。
- 评估：论证强度中等偏经验；但与 Amp（2025-04）、Manus（2025-07）"Less structure"的独立方向一致（M-004 状态说明）。

### 框架取舍（初版遗漏的一节）

- 原文立场："start by using LLM APIs directly"——直接用 LLM API 起步；框架的代价是加抽象层、遮蔽 prompt 与响应、妨碍调试（原文列举的常见框架局限）。
- 与 Q-001 相关：该节推荐的第三方框架清单在 2026-08 修订中被厂商自家方案（Claude Agent SDK 等）替换——这记录厂商产品推荐与托管路线变化，不能仅凭清单改写证明模型已吸收外部脚手架。

### Agents 的成功因素与生产化

- 成功三因素（原文措辞）：**Maintain simplicity**（保持简单，分解要直观）/ **Prioritize transparency**（优先透明，显式展示 agent 的规划步骤）/ **Carefully craft your ACI**（精心打磨 agent-computer interface）。（初版将第一条改写为 "Straightforwardness" 并附加解释，已按原文改回。）
- 生产化（原文实际内容）：在沙箱环境充分测试、配合理理的 guardrails，并在 checkpoint 处引入人工反馈。
- ⚠️ 勘误记录（v0.2）：初版写"mock 执行/实时监控/会话回放、错误纠正三形态（引 Cognition 2025-06）"——两版原文均无；且 BEA 成文（2024-12-19）早于 Cognition 文（2025-06）半年，时间上不可能引用。已删。
- 成熟 agent 的标志之一是从错误中恢复（"recovering from errors"）——三源汇合证据之一（K-006）。

### 附录 1：两个实践案例（初版漏了 1B、拼装了 1A，已改）

- **1A 客服支持**：初始对话分类决定后续流；工具拉取用户历史、执行动作（办退款、更新工单）；能处理时直接办，不能时收集澄清信息并转人工。正文 Routing 节的客服例（按难度分流到不同成本模型）与这里的对话流是两处内容，初版被拼在一起。
- **1B 编码 agent 域**：agent 负责按文件系统与运行时检查的输出来定位和修复 bug；能力主张对标 SWE-bench Verified；商业模式按解决计费（"usage-based pricing…only for successful resolutions"）——市场侧可度量性的直接证据（评测横切）。

### 附录 2：ACI 设计要点

- 保持 token 高效（信息密度、格式贴合模型）；
- 工具应可自省：名称、描述、参数与整体接口构成完整的自我描述；
- poka-yoke（防呆）：给工具加参数默认值、类型约束、校验，把常见错误挡在调用前——例：传入代码用绝对路径，保证引用正确；
- 沙箱：filesystem、runtime、credentials 环境隔离，配合搜索/备份类工具让 agent 安全试错。

## 案例区块

- 实践者与约束：Anthropic 观察的（未具名）客户团队与自家系统；客服（成本敏感、可审计）与编码（按效果计费）两域。
- 具体做法：客服=workflow+分级路由+human-in-the-loop 收尾；编码=agent 循环+沙箱+按解决计费。
- 报告的效果：作者自述（含 SWE-bench Verified 能力主张）；无第三方数据。
- 对我们的可复现性：分类学可本地复现——同一任务分别以单次调用/workflow/agent 三档实现，对比成功率、成本、延迟（E-01）。

## 适用条件与反证

- 适用条件：泛模型；任务域可定义"何时需要自主性"的判据；对延迟/成本敏感的生产环境。
- 反证/局限：
  - 作者自认：agents 用延迟与成本换任务表现，错误累积、难调试（原文即以此为限）。
  - 我方怀疑：Anthropic 卖 agent 基础设施，有动机先降低使用者门槛再卖复杂度；"从简单开始"需跨厂商验证（OpenAI Practical Guide、Amp已在M019/M018对读，但相邻观点不等于同一效果独立验证）。
  - 结构性局限：把 memory/retrieval 列为构建块但**无任何治理方法展开**（无 rot/compaction/缓存/位置概念）——治理方法论出现在 9 个月后的 M-002；2026-08 修订只补了工具清单，未补上下文层。
- 与 Q-001 的关系：编者注承认"工具环境剧变"；框架节推荐清单改写为平台产品化线索，不是模型能力吸收的测量。

## 与已有条目的关系

- 支撑 Q-003（workflows vs agents）的原始出处；orchestrator-workers 模式是 Q-002（多 vs 单 agent）的最简形态。
- 与 M-002（ECE）同厂商互补：本篇管"结构怎么搭"（harness），M-002 管"窗口里放什么"（context）；两篇按规则计 1 源。
- 与 M-003（Manus）方向一致处：都反对过度工程；分歧处：本篇未讨论 KV-cache 经济学与上下文压缩；工具治理处方相反（最小工具集 vs mask 管理膨胀，docs/07 D5）。

## 后续动作

- [ ] 需要复现的主张：E-01 复杂度递增收益曲线（同一任务三档实现对比）。
- [ ] 需要补读的反方/正方：OpenAI指南已记M019（相邻对读，非效果验证）；Claude Managed Agents 文档（编者注指向的新方案）。
- [ ] 复核触发器：Claude Managed Agents 正式文档发布；模型大版本；6 个月例行。


## 2026-10-14 正文一致性纠正

按既有docs08/总纲裁决及本篇内部证据限制，同步正文中的旧强断言、状态或阅读范围；未重抓来源、未新增效果验证。修改前文本见[_review_archive/2026-10-14-batch13/notes/M-001_building_effective_agents.md](_review_archive/2026-10-14-batch13/notes/M-001_building_effective_agents.md)，仅供历史追溯。
