# M-105 SKILL.state：以显式执行状态替代追加式对话历史

## 元信息

- 来源链接：[arXiv:2608.26263v3](https://arxiv.org/abs/2608.26263)
- 原文快照：[_snapshots_local/batch17/skill_state.pdf](_snapshots_local/batch17/skill_state.pdf)，哈希见同名.pdf.json；pypdf提取txt（16页，行号以txt计）。
- 发布日期：arXiv v3 2026-09-02（页眉）；主张实质更新日期：v1→v3 修订未逐版对比。
- 检索/审查日期：2026-11-20；验证日期：未复现（自建基准 SkillExecBench 无第三方结果）。
- 作者/机构：Sanket Badhe、Jonghyun Chung（Google LLC）、Priyanka Tiwari（Purdue）。
- 适用模型：Gemini-3-Flash（主实验）、Gemma-4-31B-it、Qwen-3-8B-it（temperature 0.0, top-p 1.0）；下一代模型发布触发复核。
- 来源类型与利益关系：预印本（B站UP主标注 EMNLP26，PDF内无会议标记，会议归属未核实）；Google 作者，展示 Google 系模型；一手不等于独立验证。
- 阅读覆盖与媒介限制：正文与表1-5全读、局限章全读；附录7 prompt模板与开放权重全量表未逐表核读。
- 渠道路径：B站UP主09-02视频发现（docs/39 A4）；内容全部取自论文原文。

## 一句话

把过程性技能执行重构为显式状态转移：每步只给模型 (P, Σt, Ot) 三件套，推理痕迹在验证后立即丢弃——prompt O(1)、累计 token O(T)，长程准确率反超历史式/摘要式/LangGraph式 runtime，且预算匹配对照证明收益来自结构化状态而非短prompt。

## C1 来源记载（正文直述，引文逐字自txt）

**机制（L187-250）**：At = (P, Σt, Ot)——P 不可变过程规范、Σt 结构化执行状态、Ot 最新观察；"The language model never receives previous observations, previous actions, or previous reasoning traces."（L195-197）步内多步推理完整保留，"once the state transition has been validated and applied, the reasoning trace Rt is discarded permanently"（L240-242）。状态更新 Σt+1 = Σt ⊕ ΔΣt，⊕ 为带 null-删除语义的字典合并。schema 每域一次而非每任务（InterCode CTF 100 例复用单一 5 字段 schema：discovered_flags/tested_hypotheses/active_files/working_dir/cmd_summary，L212-216）。验证在确定性 runtime：invalid patch 触发 rollback-retry，模型输出不能破坏持久状态（L620-626）。

**复杂度（L252-270）**：对话式 runtime 累计 token O(T²)；SKILL.state 每步 prompt O(|P|+|Σ|+|O|) 与已执行步数无关，累计 O(T)。

**长程扩展（Table 1，Warehouse，Gemini-3-Flash，5种子均值±样本SD）**：
- T=100：SKILL.state 0.94±0.01 / 65,408 tokens；Stateful(LangGraph) 0.91±0.02 / 1,062,387（16.2×差距）；Memory(摘要) 0.87；Prompt(ReAct) 0.84。
- T=200：SKILL.state 0.94±0.02 / 122,384；Prompt 0.74 / 2.6M；Memory 0.84 / 6.2M；Stateful 0.88 / 5.0M。
- 差异在 T≥50 显著（paired t-test, p<0.01，L409-411）。

**噪声鲁棒（Table 2，T=50）**：每轮注入 5/20/50 条干扰事件，Prompt 从 0.68 降至 0.53；SKILL.state 保持 0.97-1.00，"because distractors are filtered out during state patch generation and never enter subsequent prompts"（L442-444）。

**状态恢复（Table 3）**：外部静默修改世界状态（秘密审计/条码/移库）后，三个历史基线均幻觉 5-8 轮才恢复；SKILL.state 零恢复步（"the state is updated immediately upon receiving the corrective alert"，L499-502）。场景D（取消订单）所有 runtime 均失败。

**公开基准（Table 4）**：InterCode CTF pass@1 54.2%（最强基线 Memory 46.4%，+7.8pp；比 Stateful +12.4pp），token 比 ReAct 省 60.4%；τ-Bench Retail 58.3% / Airline 32.4% 均领先，Airline 基线 prompt 峰值超 11,000 tokens/步而 SKILL.state 平坦 ~2,800。

**预算匹配对照（Table 5，T=100，预算~1,800 tokens）**：滑窗截断 0.18（早期关键库存分配被逐出）；LLMLingua 0.22（熵过滤删掉语义关键的槽位标识符）；Summary-capped 0.52；SKILL.state 0.94——"structured state maintenance preserves exact relational dependencies that statistical compressors destroy"（L559-562）。**收益来自结构化状态表示，不是 prompt 变短。**

**开放权重误差分类（L563-578）**：Gemma-4-31B @T=100 得 0.42，失败分解：68% 过早覆盖/删除状态键（未原地合并）、20% schema/类型混淆、12% JSON 语法——"small-model degradation stems from structured output adherence rather than reasoning capacity"。

## C2 作者解释（局限自述，L591-629）

sufficient statistic 假设（凡影响未来行动的过去信息都能在知晓时投入结构化状态）在三种情况失效：①无固定 schema、状态结构需执行中动态发现；②"a correct state update depends on an earlier observation whose relevance was not recognized when first observed"（未识别相关性→未入状态→不可恢复）；③任务目标定义在历史轨迹本身（审计/调试溯源/解释过去行为）。另：单agent设置，多agent并发写需 ⊕ 的确定性冲突解决语义，未测。

## C3 我方推导与比较（工作草案）

1. **与 M-046（上下文文件对照）互补升级**：M-046 检出的是"加上下文文件 vs 无"无正解率差异；本篇检出的是"结构化状态 vs 历史/摘要/压缩"的显著差异，且预算匹配控制排除了"短prompt即收益"。两篇合并：上下文管理的收益形态取决于**状态能否枚举为 schema**——能枚举的过程性任务收益大且可测，开放式任务（M-046 场景）未必。
2. **与 M-103/M-104 的 transcript 立场冲突（重要，登记总纲）**：M-103 把原始会话记录当作 dreaming 修正的 ground truth（"The transcript gave Claude a ground truth to validate its memory against"）；本篇在 sufficient statistic 成立时丢弃历史"无损"。调和点恰是本篇局限③：**transcript 的价值取决于任务目标是否定义在轨迹上（审计/修正/溯源）**。跨会话记忆系统（M-103/104）目标常在轨迹上，过程执行（本篇）目标在终态——两类系统不可互相套用"可丢/不可丢"结论。
3. **压缩不是状态管理的替代品**：摘要式 Memory 基线在 T=200 上 0.84 且 6.2M tokens；预算匹配下 Summary-capped 仅 0.52。与 M-048 的 compaction 分工（M-103 L12 把 compaction 与 agent memory 划界）共同支持：**摘要保连贯、状态保事实，二者不互替**。
4. **模型代际边界**：结构化输出遵循是小模型的主要失败模式（68%+20%+12% 全是 patch 格式/语义错误）——该架构对小模型有门槛，适合带"适用模型"字段的原则候选；作者建议 grammar-constrained decoding。
5. **与 Q-001 关系**：runtime 侧的结构化状态是"外部脚手架"未被模型能力吸收的反例候选（模型再强也不自带 Σt 持久化）；但局限①（动态 schema 发现）恰是模型能力可逐步接管的部分。

## C4 限制与反证

- 自建基准（SkillExecBench 两个环境）由作者设计实现，无第三方复现；InterCode CTF/τ-Bench 为公开基准但 runtime 包装自研。
- 主实验单一强模型（Gemini-3-Flash）；开放权重只报误差分类未报全量对照（附录未逐表核）。
- 场景D（取消订单）所有 runtime 失败，作者未展开（保守信号：状态化不解决全部外部变更）。
- EMNLP26 接收状态未核实（UP主标注，PDF无标记）。
- [我方推导] 预算匹配对照中 LLMLingua 等压缩器为通用配置，不排除调优后差距缩小；"统计压缩破坏关系依赖"的结论以该配置为限。

## C5 下次复核触发

- 第三方复现 SkillExecBench 或反例结果出现。
- 下一代 Gemini/Gemma/Qwen 发布（结构化输出遵循门槛是否消失）。
- 多 agent 并发写语义（⊕ 冲突解决）的后续论文。
- 与 M-103 dreaming 的正面对比研究（transcript 保留 vs 状态化）若出现。

## C6 来源去向

- 纳入知识库（A4精读）；上下文治理线核心证据；与 M-046/M-048/M-103/M-104 构成"历史vs状态vs摘要"三方比较。

## C7 勘误与核对记录

- 2026-11-20：UP主标题转述"从追加消息到只保留所需状态"与论文机制一致；其"EMNLP26"归属未在PDF中核实，登记待查。
