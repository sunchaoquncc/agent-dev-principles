# M-110 常驻智能体治理综述：持久状态的六轴生命周期与回滚缺口

## 元信息

- 来源链接：[arXiv:2606.30306](https://arxiv.org/abs/2606.30306)
- 原文快照：[_snapshots_local/batch17/always_on_survey.pdf](_snapshots_local/batch17/always_on_survey.pdf)，哈希见同名.pdf.json；pypdf提取txt（136页，行号以txt计）。
- 发布日期：arXiv 2606（2026-06，版本号未核）；主张实质更新日期：未知。
- 检索/审查日期：2026-11-21；验证日期：未复现（编码语料与方法无法由本库独立重核）。
- 作者/机构：Tianyu Ding、Aditya Nannapaneni、Bingfan Liu、Ling Zhang；机构名不在提取文本首页（B站UP主称亚马逊，按转述登记待核）。
- 适用模型：不针对特定模型（综述+协议设计）；AOEP-v0 为 pilot。
- 来源类型与利益关系：预印本综述；作者自述编码方法与局限（inter-coder 0.82/0.74，盲检236篇）。
- 阅读覆盖与媒介限制：**选读**——摘要/目录/编码语料方法与量化结果（§1.1）、rollback 章节（§4.3.4）、OS 抽象（§4.4）、生命周期保真（§4.5）、AOEP 协议（§9.1-9.3）全读；其余各部分（记忆分类学、多智能体、应用域等）未读。**136页中约读30-40页，非全读**。
- 渠道路径：B站UP主11-04视频发现（docs/39 A10）；内容全部取自论文原文。

## 一句话

把常驻 agent 定义为"持久状态系统"（记忆+任务账本+权限+承诺+审计记录+触发条件+外部已提交效应），用六轴×十阶段生命周期编码435篇文献：前向弧（写入/检索）远厚于回返弧（遗忘66/审计88/回滚27），外部效应回滚几乎无人实现——并给出可确定性评分的 AOEP-v0 治理评估协议原型。

## C1 来源记载（正文直述，引文逐字自txt）

**框架（L7-13, L244）**：operative system 覆盖"retrievable memories, but also task ledgers, permissions, credentials, commitments, provenance and audit records, shared state, trigger conditions, and externally committed effects"。六轴：authority、scope、mutability、provenance、recoverability、actionability。十阶段生命周期：write, validate, organize, retrieve, act, update, forget, audit, rollback（+observe）。五不变量：authority monotonicity（权限单调）、scope non-expansion（范围不扩张）、deletion propagation（删除传播）、provenance preservation（来源保持，正文命名，L250-252/L4122-4123）、rollback traceability（回滚可追溯）。

**语料与量化 skew（摘要 L12-13 + L435-488）**：435 篇编码（摘要"a scoped map rather than an exhaustive census"）。retrieve 269、write 200；authority 最稀缺轴 72/435；audit 88、forget 66、**rollback 仅 27/435，且"none in the corpus reports recovery success or cost after corruption"**。方法自限：编码者间一致性 0.82（阶段）/0.74（轴，盲检236篇）；governance 导向的补充检索使语料扩大超过4倍仅把治理份额从1/6抬到1/3；2024前提交的工作治理份额更低（非新预印本效应）。

**Rollback 三分（§4.3.4，L1862-1887）**：internal-state rollback（回退存储事实/整合决策）、workflow rollback（补偿部分执行的多步任务）、external-effect rollback（撤销已提交的外部副作用如付款/删除）。27 的聚合"conservative for the easiest subclass and almost certainly an overcount for the hardest"；外部效应回滚"the subclass that matters most because irreversible effects cannot be repaired by any internal mechanism, is rarer still"。基准缺口：AppWorld/τ-bench 验证动作是否正确，不验证"whether a wrong action licensed by stale state could be traced and undone"（L1866-1868）。核心论断（L1880-1882）："a field that does not instrument act for consequence cannot implement rollback even in principle"——后果句柄在 act 阶段记录、在 rollback 阶段消费。

**OS 抽象的机制/治理分离（§4.4，L1888-1912）**：MemGPT/MemoryOS/sleep-time 提供分页/调度/检查点原语，但"governs the lifecycle for resource correctness, not state correctness"——逐出策略不连 authority/provenance（低权限记录可因高频访问被提升）。

**AOEP-v0（§9，L3997-4113）**：测"the correctness of a state trajectory under the kinds of perturbations only a persistent agent encounters: restart, conflict, deletion request, permission revocation, shared-scope change, adversarial write, and delayed consequence"。事件携带幂等键、因果边（parent/supersedes/conflicts-with+事务ID）、**permission epoch（权限纪元整数，动作按执行时纪元而非写入时纪元校验）**、信任层级+签名、保留/隐私约束；11 个封闭操作集（read/write/update/delete/tombstone/share/unshare/validate/quarantine/deny/rollback）——"a tombstone that is not reflected in the deletion ledger, or a quarantine that is later promoted to instruction, is a named, locatable violation"（L4089-4092）。**验证器自重算快照、"never trusts a system's claim that it behaved"、"Every AOEP check is deterministic"**（刻意回避 LLM-as-judge，因 position/verbosity/self-enhancement 偏置对治理失败检测是致命的）。记分两分（§9.3 L4114-4119）：obligation pass（义务通过）+ negative-invariant pass（负不变量/无泄漏检查），非单一分数。先行工作印证：Jung et al. 2026 级联/缺席/删除任务上当前系统近全崩（Cascade 3%、Absence 1%）；Kwon 2026 保留过期结论但丢来源的记忆"confidently uncorrectable and strictly worse than empty memory"。

## C2 作者解释

- 核心论题：常驻 agent 与"记忆增强 agent"的区别在回返弧——"The persistent-state lifecycle is not a memory pipeline with two extra boxes. It is a loop whose forward arc is much more developed ... than its return arc"（L1930-1932）；缺回返弧时"accumulated state compounds risk rather than competence"（L1942-1943）。
- 议程连接：数据库、分布式系统、形式化验证、能力安全、机器遗忘（摘要）。

## C3 我方推导与比较（工作草案）

1. **与本批四篇的系统性合流（批次最重要交叉点）**：M-104 证明 scope 不保持导致不安全（write/read 泛化）；本综述的 scope non-expansion 不变量与 93% 笔记宽于原指令（M-104）互为微观/宏观证据。M-106 的 deferred tool calls = permission epoch 思想的工程简化形态（按动作询问≈每动作校验当前纪元）；M-106 的 inbox source of truth+重试 ≈ recoverability 轴的幂等键/事务思想。**综述把本批散点收进统一词汇表**——六轴+十阶段+五不变量是可复用的分析坐标，候选进入知识版图（harness 治理+安全横切的连接框架）。
2. **评测横切的方法论新标杆**：AOEP 的"确定性校验+快照重算+不信任系统自述"与 M-104"按行为而非文本审计"、M-108"LLM生成测试替代LLM判断"三点连成一线：**治理性质的评测必须避开 LLM 主观判断**——三源独立收敛，候选原则素材（评测器形态）。
3. **rollback 三分法**给项目的幂等/持久恢复主题提供工程粒度：内部状态/工作流/外部效应三层的实现难度与稀缺度递增；"act 阶段不记录后果句柄则 rollback 原理上不可实现"是可操作的设计前置条件。
4. **Kwon 2026 登记为高价值线索**（"保留过期结论但丢来源的记忆比无记忆更糟，source-first 写入策略修复"）——与 M-103 dreaming 对照 transcript 修正、M-105 局限②（未识别相关性丢失）三方呼应：**来源链接（provenance）是记忆可修正性的前提**。纳入下一轮候选。
5. 综述的"scoped map not census"自我定位与项目"读过≠验证"的状态纪律同构，方法可借鉴（编码透明+方向性结论不冒充普查）。

## C4 限制与反证

- 编码语料为作者团队单遍编码+盲检抽样，非普查；治理份额结论限定在其 query frame 内（作者自述）。
- AOEP-v0 是参考设计+pilot，无 leaderboard 效度；"不是已部署系统普遍失败的证据"（作者自述 L4010-4011）。
- 本笔记为**选读**（约30-40/136页）：记忆分类学、多智能体共享状态（§11.4 authority-scoped rollback 未读）、失败模式全表、应用域未读——引用限于已读章节。
- 机构归属（亚马逊）按UP主转述登记，未从原文核实。
- 2026-06 发布，距今约5个月，在6个月窗口内但临近；原则层引用时注意时效。

## C5 下次复核触发

- AOEP 被 benchmark 社区采纳或出现实现。
- Jung et al. 2026（Cascade 3%/Absence 1%）与 Kwon 2026 精读后回看综述定位。
- M-106 的 Claude Duet 产品化文档（对照五原语与六轴的映射是否被产品吸收）。
- 综述 v2 或正式发表版本。

## C6 来源去向

- 纳入知识库（A10选读）；harness 治理+安全横切的**连接框架来源**；新线索登记：Jung et al. 2026、Kwon 2026、Orogat & Mansour 2026（状态轨迹形式化不可能结果）。

## C7 勘误与核对记录

- 2026-11-21：UP主称"亚马逊爆火综述…揭示撤销和恢复的研究缺口"，与摘要及§4.3.4一致；"亚马逊"归属待核（见元信息）。
