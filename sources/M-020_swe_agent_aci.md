# M-020 SWE-agent：Agent-Computer Interfaces Enable Automated Software Engineering

> 当前用途（2026-10-14）：以下保留来源当时的做法与作者主张，仅作历史/自我修订对照；不将旧型号处方或旧“认可”记录作为现行要求。当前原则状态见[证据登记](../principles/07_evidence.md)，效果仍未验证。

> **2026-10-13审查勘误/适用范围（优先于下文历史解读）**：Table1 Shell-only11→18差7pp；无demonstration基线7.33。正文10.7与18−7.33数值吻合，不能配11→18，也不能称严格只换接口。2024证据仅作历史基线。

## 元信息

- 来源链接：https://arxiv.org/abs/2405.15793
- 来源链接（正文精读）：https://arxiv.org/html/2405.15793（NeurIPS 2024）
- 原文快照（供复核）：摘要页 https://web.archive.org/web/20261005204247/https://arxiv.org/abs/2405.15793 ；正文 https://arxiv.org/html/2405.15793 （2026-10-13 全文精读，引文逐字取自当日抓取）
- 发布日期：2024-05（arXiv v1；精读为 HTML 最新版 v3）；编号 ✅ 核实（docs/04 原记"编号待核"，已回写）
- 检索日期：2026-10-13（摘要级初读 + 正文级补读，均为当日抓取）
- 作者/机构：John Yang, Carlos E. Jimenez, Alexander Wettig, Kilian Lieret, Shunyu Yao, Karthik Narasimhan, Ofir Press（Princeton 等）
- 适用模型：GPT-4 Turbo（主实验）；Claude 3 Opus（可移植性实验 10.46%）
- 证据等级：可检验结论（同行评审 NeurIPS 2024；SWE-bench 基准、含 Shell-only 对照的消融实验）
- 框架落点：harness 治理（ACI=工具/接口设计）为主；上下文治理（窗口管理消融）；评测横切（SWE-bench 度量）
- 关联条目：M-004、M-006、M-023、M-027；K-010；Q-001（Agentless 反例成对读）
- 备注：v0.3 依全文精读升级（原摘要级 [外注] 三个数字中两个系记忆重建、正文不存在，已按真实正文数字重写——再次验证"数字必须来自抓取文本"纪律）。

## 一句话结论

2024论文把“给agent用的接口”（ACI）作为实验设计空间：Table1同模型跨系统比较11.00%→18.00%，差7.00pp（非严格只换接口的因果消融）；若干组件有消融比较，但不能把四条抽象原则逐一当作已隔离验证的因果命题。

## 要点摘录（摘要级）

- 概念：LM agent 是"一类新型终端用户"，"有自己的需求与能力，会从专门构建的接口中受益"——agent-computer interface（ACI）是与人机接口（HCI）对偶的设计空间。
- 核心主张：ACI 的设计影响 agent 的行为与性能（摘要主张设计空间值得系统性研究）。
- **四条 ACI 设计原则（正文 §2，逐字）**：
  1. "Actions should be simple and easy to understand for agents."（少选项、简文档）
  2. "Actions should be compact and efficient."（高阶操作合并为单动作）
  3. "Environment feedback should be informative but concise."
  4. "Guardrails mitigate error propagation and hasten recovery."
- 主结果（正文 §1，逐字/表格）：GPT-4 Turbo 上 SWE-agent 解决 12.47%（286/2294）的 SWE-bench 全测试集，"substantially outperforming the previous best resolve rate of 3.8% by a non-interactive, retrieval-augmented system"；表格基线——RAG w/ GPT-4 Turbo 1.31%（全集）、Shell-only w/ GPT-4 Turbo 11.00%（Lite 子集）；Table1 Shell-only比较差7.00pp；组件消融见Table3，不能合称严格对照。
- 跨模型可移植：换 Claude 3 Opus 解 10.46%（只说明该系统在第二模型上也报告结果，不是该模型的接口增益对照）。
- 消融（SWE-bench Lite，GPT-4 Turbo，逐项）：编辑器去掉 linting 15.0（-3.0）、完全无编辑命令 10.3（-7.7）；迭代式搜索（仿人类 UI 的逐条翻阅）12.0（-6.0）——**比不提供搜索工具（15.7）还差**：agent 会穷尽式翻完每个匹配；文件查看器 30 行 14.3 / 100 行 18.0 / 全文件 12.7——窗口过小或过大都降性能；上下文保留全历史 15.0 vs 仅最近 5 条观察 18.0。
- 上下文管理实现（正文 §3）：最近 5 条观察保留、更早的折叠为一行占位；格式错误的响应重试、成功后错误消息从历史移除（去噪）；空输出时显式告知"Your command ran successfully and did not produce any output"。
- 行为发现（§5.2，逐字小标题）："Agents succeed quickly and fail slowly"——成功实例中位成本 $1.21/12 步，失败均值 $2.52/21 步；93% 已解决实例在预算内主动提交。失败模式：52% 为错误/过度特化实现，23.4% 为编辑失败恢复失败；任意一次编辑的最终成功率 90.5%，一次失败后降至 57.2%。
- 方法论地位：本库早期收集的含组件消融的历史研究（组件消融与Shell-only跨系统比较须分开）。

## 案例区块

- 实践者与约束：普林斯顿等学术团队；SWE-bench（真实 GitHub issue 数据集）；GPT-4 Turbo。
- 具体做法：为代码编辑设计专用接口（简化动作空间、结构化反馈），+简单循环。
- 报告的效果：SWE-bench 全集 12.47%（此前非交互式最好 3.8%）；Table1跨系统比较+7.00pp（11.00%→18.00%，Lite）；Claude 3 Opus 10.46%（同行评审）。
- 对我们的可复现性：SWE-bench 子集跑分成本高（按任务计费）；可做**廉价替代**：同一模型+同一任务，仅改工具接口粒度（粗粒度 vs 细粒度）对比成功率（E-09 候选）。

## 适用条件与反证

- 适用条件：GPT-4 Turbo / Claude 3 Opus 时代（2024）的代码任务；ACI 增益是否随模型换代缩小——正是 Q-001 的直接实验对象（跨代重跑需控制接口、任务与资源条件，不能称最干净的吸收测量，且本文已给 Claude 3 Opus 可移植数据点）。
- 反证/局限：
  - **成对反例**：Agentless（M-027，同期 2024-07）用固定三阶段管线在 SWE-bench Lite 拿到 32.00%@$0.70，高于 SWE-agent 同子集的 18.00%@$1.67——这些是跨论文历史数字，未控制配置、预算和处理流程，不能据此归因固定流程或Agent循环的优劣。
  - 消融对象是自家接口组件，非跨设计空间的全因子实验；SWE-bench 数据集本身有质量问题（Agentless 审计出 Lite-S 变体）。
- 与 Q-001 的关系：组件消融可用于研究特定接口贡献；跨代比较仍需控制任务、配置和预算，不能直接量化Q-001吸收。

## 与已有条目的关系

- M-006关联的特定接口组件获得论文消融结果（组件消融与Shell-only跨系统比较须分开）：BEA、Amp和SWE-agent提供不同层次证据，不能用三源数量直接升级现行原则；旧认可仅历史记录。
- 与 M-004（复杂度阶梯）：本文提供"agent 档"的正面证据，M-027（Agentless）提供固定管线够用的制衡——阶梯两端同基准对读。
- 与 M-027 的关系是 Q-001 的核心对决样本：结构自主性 vs 固定管线，2024历史结果并置，非同条件因果对照。

## 后续动作

- [ ] 需要复现的主张：E-09 接口粒度消融（廉价版 ACI 实验）；Q-001 专用：跨代模型重跑 ACI 消融。
- [ ] 需要补读的反方/正方：ACI正文已补读，若复现须再核实现配置；Agentless正文仍待取（目前仅摘要）；SWE-bench 系列后续（Verified/ multimodal 等）。
- [ ] 复核触发器：SWE-bench 方法论更替；模型大版本（ACI 增益重测点）。


## 2026-10-14 正文一致性纠正

按既有docs08/总纲裁决及本篇内部证据限制，同步正文中的旧强断言、状态或阅读范围；未重抓来源、未新增效果验证。修改前文本见[_review_archive/2026-10-14-batch13/notes/M-020_swe_agent_aci.md](_review_archive/2026-10-14-batch13/notes/M-020_swe_agent_aci.md)，仅供历史追溯。
