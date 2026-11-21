# M-113 TokenPilot：缓存友好的上下文管理（文本稀疏 vs 前缀连续权衡）

## 元信息

- 来源链接：[arXiv:2606.17016v2](https://arxiv.org/abs/2606.17016)
- 原文快照：[_snapshots_local/batch17/tokenpilot.pdf](_snapshots_local/batch17/tokenpilot.pdf)，哈希见同名.pdf.json；pypdf提取txt（16页，行号以txt计）。
- 发布日期：v1 2026-06（v2 2026-08-28）；主张实质更新日期：v1→v2 未对比。
- 检索/审查日期：2026-11-21；验证日期：未复现。已集成进开源 LightRSI（github.com/zjunlp/LightRSI，未取）。
- 作者/机构：Buqiang Xu、Zirui Xue 等15人，末位 Ningyu Zhang / 浙江大学（zjunlp）、电子科大、西电、HomologyAI。
- 适用模型：基准 PinchBench 与 Claw-Eval（模型构成未逐项核）；下一代模型发布触发复核。
- 来源类型与利益关系：预印本；学术+公司（HomologyAI）。
- 阅读覆盖与媒介限制：摘要/引言全读；方法与实验为定位段+关键数字精读（未逐表核）——**摘要级+定位段精读**。
- 渠道路径：B站UP主09-04视频发现（docs/39 A9）；内容取自论文原文。UP主转述"长会话成本降87%"对应 continuous 模式 Claw-Eval 数字（87%），一致。

## 一句话

指出文本剪枝/记忆逐出的"无约束序列变异"会打乱布局造成前缀失配与缓存失效——**上下文缩减与 prompt 缓存连续性存在关键权衡**；TokenPilot 双粒度管理（入口端压缩稳定前缀 + 生命周期感知逐出）在两基准上成本降 56-87% 且性能保持。

## C1 来源记载（摘要+定位段直述）

- 核心权衡命名："a critical trade-off between text sparsity and prompt cache continuity"（摘要）。
- 双粒度：全局 Ingestion-Aware Compaction（"acts as a framework harness to stabilize prompt prefixes and eliminate open-world environmental noise at the ingestion gate"）+ 局部 Lifecycle-Aware Eviction（"enforcing a conservative batch-turn schedule to offload content segments only when task relevance expires"）。
- 结果：PinchBench/Claw-Eval isolated 模式成本降 61%/56%，continuous 模式 61%/87%，性能与先前系统相当（摘要）；一处组件消融报 cache hit tokens 从 26.716M 降 65.0% 至 8.551M——论文将其作为正面证据（"demonstrating that TokenPilot tightly caps the active memory footprint"，L571-575，未逐项核）。

## C3 我方推导与比较（工作草案）

1. **"缓存前缀稳定"主题第三源强化**：M-108（hooks 附工具结果后保前缀，作为机制副作用出现）→ M-111（EoCC 重开会话天然重置前缀，未讨论缓存）→ 本篇把前缀连续性上升为**核心设计目标**并量化权衡——主题从实践惯例→显式约束的演进，登记为上下文治理线候选原则素材（工程实践类，非效果主张）。
2. 与 M-105/M-111 构成上下文管理三方：结构化状态（schema 强制）/ 自然语言压缩态（EoCC）/ 缓存感知剪枝（本篇）——三者正交可组合；本篇与 M-111 的压缩路线区别在"何时剪、剪哪、如何不破前缀"。
3. 入口端降噪（ingestion gate）与 M-105"干扰在状态补丁生成时被过滤"同构：**在写入时过滤而非在读取时容忍**。

## C4 限制

- 摘要级阅读；两基准均非主流 SWE/终端基准，与 M-105/M-108/M-111 的基准不重叠，数字不可横向比较。
- 模型构成与部署假设（缓存计价）未核；已集成 LightRSI 但无第三方评测。

## C5 下次复核触发

- LightRSI 集成的独立评测；缓存计价模型变化。

## C6 来源去向

- 纳入知识库（A9，摘要级+定位段）；上下文治理"缓存连续性"主题证据。

## C7 勘误与核对记录

- 2026-11-21：UP主"缓存友好…成本降87%"与摘要一致（87% 为 continuous 模式 Claw-Eval 单点）。
