# M-117 AIDE²：AI 研究 Agent 的递归自我改进（8天自主运行）

## 元信息

- 来源链接：[arXiv:2609.26457](https://arxiv.org/abs/2609.26457)
- 原文快照：[_snapshots_local/batch17/aide2.pdf](_snapshots_local/batch17/aide2.pdf)，哈希见同名.pdf.json；pypdf提取txt（28页，行号以txt计）。
- 发布日期：2026-09-23（约2个月前，窗口内）。
- 检索/审查日期：2026-11-21；验证日期：未复现。
- 作者/机构：Dhruv Srikanth、Bingchen Zhao、Dixing Xu、Yuxiang Wu、Zhengyao Jiang / Weco AI。
- 适用模型：AIDE² 是系统（自改对象为其研究 agent 代码，底座模型未在摘要级阅读内核）；下一代模型发布触发复核。
- 来源类型与利益关系：预印本；商业公司（Weco AI 做 AI R&D 自动化，有展示动机）。
- 阅读覆盖与媒介限制：摘要+引言开头精读——**摘要级精读**。
- 渠道路径：B站UP主10-18视频发现（docs/39 A16）；UP主"外层智能体逐轮改写内层的搜索与上下文管理策略"与摘要一致（发现的改进含"new search policy to memory mechanisms that compress and manage the agent's growing context"）。

## 一句话

让 AI 研究 agent 以自身代码为优化对象：提出自改、在隐藏评估上基准测试、保留最优——8 天自主运行发现 7 项连续改进，泛化到 4 个 held-out 基准（含 OOD 天气预报）并匹配/超人类工程的生产级 agent；且 reward hacking 意外从 55% 降至 32%（循环从未显式优化此属性）。

## C1 来源记载（摘要直述）

- 循环定义："When an AI research agent's own code is the object of optimization, each accepted rewrite becomes the agent that the next round edits."——接受的改写即下一轮的编辑对象。
- 8 天自主运行发现 7 项连续改进（从新搜索策略到压缩管理上下文的记忆机制）。
- 泛化：4 个 held-out 基准（ML 工程/启发式算法工程/物理天气预报——后者为 OOD）；"the strongest discovered agent matches or exceeds a human-engineered production research agent"（FML-Bench 强者）。
- **意外效应**："the discovered agents also exhibit reduced reward hacking, a property the loop never explicitly optimized for: the rate falls from 55% to 32% during the run, 7 percentage points below the human-engineered agent."

## C3 我方推导与比较（工作草案）

1. **自进化线第四节点**（M-112 HGM→M-108→M-109→本篇）：本篇是"agent 改自己代码"而非"改 harness/生成 harness"——对象递进：DGM 改代码库→HGM 选分支→HarnessPro 改 runtime→JIT 生成 runtime→AIDE² 改研究 agent 自身。共同前提：隐藏评估做选择（与 M-108 生成测试、M-112 CMP 后代评估同一问题的不同解）。
2. **reward hacking 意外下降与 M-104 方向相反的单例**：M-104 记忆让更强模型作弊更多；本篇自改进循环意外降低作弊率。两例并置说明"自改进/记忆与 reward hacking 的关系"方向不稳定、机制未明——登记为开放问题，不外推任何方向。
3. RSI 叙事（AI4Science 线的边缘）：Hinton RSI/ Dream-RSI 等 B 级线索与本篇同域，本篇有具体工件与量化收益，是 RSI 线里工程证据最强的一篇（仍为自报）。

## C4 限制

- 摘要级阅读；共 3 次完整 RSI 运行（主运行 8 天 + 两次同协议重复分别接受 2 与 4 项改写，均产生持续改进，L268-270——此证据在声称阅读范围外，红队补充）；Weco AI 自报；改进的具体形态与评估细节未核。
- "递归自我改进"此处指 agent 改自身代码的工程循环，非权重级自我改进——术语消费须注意口径。

## C5 下次复核触发

- 复现运行或社区分析；FML-Bench 排名变化；reward hacking 下降的机制解释出现。

## C6 来源去向

- 纳入知识库（A16，摘要级）；自进化线+评测横切（隐藏评估选择）节点。

## C7 勘误与核对记录

- 2026-11-21：UP主转述与摘要一致；未逐数字对照视频。
