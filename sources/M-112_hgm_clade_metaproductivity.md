# M-112 HGM：用后代潜力（CMP）指导自修改搜索（超窗·历史对照用途）

## 元信息

- 来源链接：[arXiv:2510.21614v3](https://arxiv.org/abs/2510.21614)
- 原文快照：[_snapshots_local/batch17/hgm.pdf](_snapshots_local/batch17/hgm.pdf)，哈希见同名.pdf.json；pypdf提取txt（30页，行号以txt计）。
- 发布日期：arXiv v3 2025-10-29（**距今13个月，超6个月新鲜度窗口**）。
- 检索/审查日期：2026-11-21；验证日期：未复现。代码公开：github.com/metauto-ai/HGM（未取）。
- 作者/机构：Wenyi Wang、Piotr Piękos 等8人（Wang 与 Piękos 同等贡献）/ KAUST；Schmidhuber 为末位资深作者（快照无通讯作者标记，"通讯"归属不可核）。
- 适用模型：自进化对象 GPT-5-mini（开发），迁移评估 GPT-5a；具体见正文。下一代模型发布触发复核。
- 来源类型与利益关系：预印本（v3）；学术机构。
- 阅读覆盖与媒介限制：摘要/引言/方法定位段全读，结果仅摘要级与定位段数字（相关性表与对比图未逐项核读）——**摘要级+定位段精读，非全文**。
- 渠道路径：B站UP主08-30视频发现（docs/39 A8）；内容取自论文原文。
- **用途限制（按项目新鲜度纪律）**：超窗文献仅作①自进化线时间序列证据/基线快照 ②与 2026 年新方法（M-108/M-109/EvoTest）的对照。**不得充当现行指导，不得支持原则层升级**。

## 一句话

指出"元生产力-性能失配"（当前基准分数高≠后续自修改潜力大），提出以后代基准聚合（CMP，借 Huxley 的 clade 概念）作自修改树的搜索准则，理论上是 Gödel Machine 的近似；在 SWE-bench Verified/Polyglot 上超 Darwin Gödel Machine 且 CPU 时更少。

## C1 来源记载（摘要+定位段直述）

- **失配命题**：自改代码 agent 的扩张策略偏向更高 SWE 基准分，假设这蕴含更有前途的后续自修改；作者识别"Metaproductivity-Performance Mismatch: the divergence between short-term task performance and the long-term capacity for self-improvement, as measured by CMP"，并称实证存在（§4.1，未逐项核）。
- **CMP**："aggregates the benchmark performances of the descendants of an agent as an indicator of its potential for self-improvement"（摘要 L17-19）。
- **理论定位**：在假设1下真 CMP 作准则可模拟 Gödel Machine 行为（定理1，未核证明）。
- **结果（摘要级）**：HGM 在 SWE-bench Verified 与 Polyglot 上超先前自改进方法（含 Darwin Gödel Machine）且"fewer allocated CPU hours"；CMP 估计与真实值加权相关 0.778（SWE-Verified-60，表内数字）；**在 SWE-bench Verified 上以 GPT-5-mini 优化、以 GPT-5a 在 SWE-bench Lite 评估达人类水平**，"matching the best officially checked results of human-engineered coding agents"（摘要）。

## C3 我方推导与比较（限于对照用途）

1. 与 M-108/M-109（2026-09/10）对照构成自进化搜索准则演进线：**DGM 系（基准分导向）→ HGM（后代潜力 CMP）→ HarnessPro（帕累托+生成测试）→ JIT（训练生成器摊销搜索）**——搜索准则从"当前分数"到"后代潜力"到"多目标"到"内化"，方向一致：单一基准分作为中间目标的失配被反复发现。HGM 的 mismatch 命题是 M-108"当前得分误导"（docs/39 A8 主题句）的更早直接表述。
2. "人类水平"主张依赖跨模型迁移（mini 开发→a 评估）与官方核查口径，未复现不外推。

## C4 限制

- 超窗（见元信息用途限制）；摘要级阅读，未核 CMP 估计器实现、定理假设与全部表格。
- 自评口径，无第三方复现。

## C5 下次复核触发

- 若自进化线进入原则层讨论，须以 2026 年 ≤6 个月文献为主证、本篇仅作谱系。

## C6 来源去向

- 纳入知识库（A8，摘要级+定位段）；harness 自进化线历史对照节点。

## C7 勘误与核对记录

- 2026-11-21：**渠道质量教训**——UP主 08-30 视频解读的"爆火论文"实为 2025-10 文献，分级时只查了视频日期未查论文日期，本轮抓取时发现超窗。处理：降级收录+用途限制。后续从该渠道选材须先核论文 arXiv 日期再定级。
