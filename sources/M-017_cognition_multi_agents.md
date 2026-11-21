# M-017 Cognition《Don't Build Multi-Agents》+《Multi-Agents: What's Actually Working》（自我修订样本）

## 元信息

- 来源链接（原文）：https://cognition.com/blog/dont-build-multi-agents（发布 2025-06-12，作者 Walden Yan）
- 来源链接（修订）：https://cognition.com/blog/multi-agents-working（发布 2026-04-22，Walden Yan）
- 原文快照（供复核）：原文 https://web.archive.org/web/20261013060943/https://cognition.com/blog/dont-build-multi-agents ；修订版 http://web.archive.org/web/20260923043733/https://cognition.com/blog/multi-agents-working 。引文以 2026-10-13 红队三重抓取核验（webReader 全文 + WebFetch 定点 + Wayback 交叉）为准，核验记录见 docs/06 #3
- 检索日期：2026-10-13
- 作者/机构：Walden Yan，Cognition（Devin）
- 适用模型：泛（案例绑定 Devin 内部系统与 SWE-1.5/Sonnet 4.5 组合）
- 证据等级：经验断言（生产教训；修订版自报数据：2 bugs/PR、58% severe、用量约 8x）
- 框架落点：harness 治理（编排/多 agent 结构）为主；上下文治理（上下文连续性）
- 关联条目：M-005、M-010、M-023；K-008、K-009；Q-001、Q-002
- 修订：2026-10-13 v0.3，依红队第二轮审查清除 ≥10 处虚构数字/引文/方向反转（勘误清单见文末）
- 说明：两篇成对精读——docs/04 #4 的提取目标就是"十个月自我修订改了什么、为什么"。

## 一句话结论

原文（2025-06）：多 agent 的根本代价是上下文切割与隐含决策冲突，别建；修订版（2026-04）：更窄的一类成立了——**agent 贡献智能，写保持单线程**（转述自贯穿句，原文全句见"要点摘录"）。

## 要点摘录：原文（2025-06-12）

（引号内为红队核验过的原文逐字引文；无引号为忠实转述。）

- 开篇（页面 meta 描述，逐字）："Frameworks for LLM Agents have been surprisingly disappointing. I want to offer some principles for building agents based on our own trial & error, and explain why some tempting ideas are actually quite bad in practice."
- 原则 1（原文措辞）："Share context, and share full agent traces, not just individual messages"——共享上下文，且共享完整 agent 轨迹而非单条消息（修订版将其重述为 "Share as much context as possible between the agents"）。
- 原则 2："Actions carry implicit decisions"——每个动作（如一次代码修改）携带无数未写下的隐含决策（风格、模式、边界处理）；并行 agent 的隐含决策互相冲突。
- Flappy Bird 示例（真实情节）：两个 agent 分头做游戏组件——一个做背景、一个做小鸟；因上下文不共享，背景被做成了 Super Mario 风格，与小鸟互不匹配——风格不一致是上下文切割的直接后果。
- 并行子任务再由 LLM 调用合并的方案："With multi-agent systems, errors compound in unpredictable ways, producing results that are worse than if a single agent had worked alone."
- 替代方案：需要扩展时**顺序**添加 agent 而非并行——上下文连续前向流动。
- 压缩实践：微调更小的模型做上下文压缩（他们在 Cognition 做过的事）；edit-apply 模型是 2024 年常见且易错的做法，如今强模型可一次完成——**这是"具体脚手架被模型吸收"的厂商自述实例（Q-001 数据点）**。

## 要点摘录：修订版（2026-04-22，重点=改了什么）

- 核心修订（贯穿句，逐字核验）："a narrower class works, where agents contribute intelligence while writes stay single-threaded"（读侧智能并行+写侧单线程）。
- 脚注声明：截至 2025-06，Anthropic 与 Cognition **各自独立**得出"只读检索子 agent 是第一个适用域"——Q-002 的罕见双厂商汇合点。
- 模式讨论（转述，按修订版行文）：
  1. **子 agent**：主循环发起检索子 agent；r/w 可接受（隔离的主要是读侧）；单工具；用上下文护栏防止 query 诱导跑偏。
  2. **Manager pattern**：**已在 Devin 上线**（"This is live in Devin today"）——manager Devin 把大任务拆给多个 Devin。
  3. **Devins Review（干净上下文评审）**：评审 agent 开新会话、用自包含 prompt、被鼓励给出与作者不同的方案；效果（自报）：均值 2 bugs/PR、约 58% 为严重；**不共享生成者上下文更利于发现问题**（无倍数/速度数据）。
  4. **Smart friend**：小模型（SWE-1.5）当主 agent，把强模型（如 Sonnet 4.5）作为可调用的"聪明朋友"工具；原文明说 SWE-1.5 单独主控 "was not good enough at being the primary model for this setup to really work"；作者自述该模式在所试前沿模型有效，未公开系统对照——是 **capability router（能力路由）而非 difficulty escalator（难度升级器）**。
- 用量与动机（逐字核验）：六个月用量约 8x（最大企业客群段）→ "This explosion of usage has led to both a push and a pull to multi-agents."
- Q-001 证据（声明，逐字核验）："models have become way more naturally 'agentic'. They intuitively understand tool use, their own context limits, and how to distill their context"。
- 未解问题（逐字核验）："The open problems are all communication problems."——原文列举的真实三类通信问题（转述）：弱模型何时该升级主控、兄弟 agent 的发现如何上报、上下文传递如何不淹没对端。

## 案例区块

- 实践者与约束：Cognition/Devin（生产编码 agent；多用户、长任务、模型成本敏感）。
- 具体做法：子 agent/manager（已上线）/干净上下文评审/small-model+smart-friend 四类形态。
- 报告的效果：2 bugs/PR、58% severe、用量 8x——全部作者自述，无第三方复现。
- 对我们的可复现性：干净上下文评审可另设计同任务对照；既有E-07用了虚构错误先验和无效关键词评分，不是有效的共享/干净上下文复现，不能用其分数背书。

## 适用条件与反证

- 适用条件：编码类长任务（全部证据来自 Devin 场景）；"写单线程"对写作/分析类任务需转译。
- 反证/局限：
  - 作者自认：模式间有权衡（并行度 vs token），未给出系统的权衡数据；通信问题未解。
  - 我方怀疑：自报数据无人类评审基线（人类评审均值多少？）；与 ECE 多 agent 研究系统（研究型任务 substantial improvement，自报）任务域不同，两方结论不互斥但均未给失败边界。
- 与 Q-001 的关系：自我修订本身是"反向更新"行为样本（K-009）；edit-apply 模型被吸收是支持方向的厂商自述；用量 8x 推动多 agent 工程是反向证据（能力/用量增长≠工程量下降）。

## 与已有条目的关系

- Q-002 的核心对决方：原文=反方基石；修订版=中间结论（与 ECE 子 agent、OpenAI 单 agent 优先**相邻收敛**——注意：核心表述"写单线程"仅此一家明说，M-023 按相邻收敛降为有条件）。
- 压缩实践与 M-010（长时程三技术）互补：厂商自述微调小模型压缩的实践，未独立复现。
- 与 M-003（Manus）：同为"单 agent+循环"实践派；todo.md/复述正是"上下文连续前向流动"的具体机制。

## 后续动作

- [ ] 需要复现的主张：干净上下文评审须先重新定义契约与评分；旧E-07无效，不自动重跑。
- [ ] 需要补读的反方/正方：Anthropic 多 agent 研究系统原文；Claude Code 子 agent 文档；本文快照存档（引文复核依赖）。
- [ ] 复核触发器：Devin 公开架构更新；Claude Agent SDK 子 agent 语义变更；6 个月例行。

## ⚠️ 勘误记录（v0.3，红队第二轮审查发现，留痕不删）

初版（v0.1）与 v0.2 存在与第一批同型的记忆重建失真，全部清除：
1. 虚构数字：2x throughput/2x token、最激进 10x、子 agent 数<逻辑核数、1.5—2x 推理开销——原文均无。
2. 虚构引文："context starvation is the killer"、"agent parallelism has become a first-order engineering concern"、"at Cognition, we use production-grade compression models"、"unless you're building Devin..."、"the techniques and practices..."、修订版副题 "How I Learned to Stop Worrying..."、"Do build multi-agents — as long as you're careful"——均无。
3. 方向反转：manager pattern 实为**已上线 Devin**（初版写反）；smart friend 实为**小模型主控+强模型当工具**（初版写反）。
4. 情节失真：Flappy Bird 实为"背景被建成 Super Mario 风、与小鸟不匹配"（初版的"分控按钮/乒乓混乱/随机关卡"为虚构）。
5. 遗漏：原文原则 1 的原措辞（share full agent traces）；修订版真实的三类通信问题；edit-apply 模型被吸收的 Q-001 数据点。
6. "2 bugs/PR"是均值 2 个，不是倍数；"更快"无数据。


## 2026-10-14 正文一致性纠正

按docs08裁决区分作者自述与独立验证，并同步E-07测量无效状态。原版已归档于_review_archive/2026-10-14-batch13/notes/，未新增来源事实。
