# M-032 Demystifying Evals for AI Agents（评测方法论）

> 当前用途（2026-10-14）：以下保留来源当时的做法与作者主张，仅作历史/自我修订对照；不将旧型号处方或旧“认可”记录作为现行要求。当前原则状态见[证据登记](../principles/07_evidence.md)，效果仍未验证。

> **2026-10-13审查勘误/适用范围（优先于下文历史解读）**：2026-01-09超6个月，仅方法基线。评测缺口未因一篇方法文闭合，需对读近期独立测量研究。

## 元信息

- 来源链接：https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- 原文快照（供复核）：https://web.archive.org/web/20261013095439/https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents
- 发布日期：2026-01-09
- 检索日期：2026-10-13
- 作者/机构：Anthropic（Engineering 博客）
- 适用模型：泛（评测方法论，非模型特定；案例含 Opus 4.5）
- 证据等级：可检验结论（厂商工程方法论+具名案例；营销渠道纪律：其结论服务 Anthropic 生态，但方法学本身可独立检验）
- 框架落点：评测（横切，主战场）；harness（eval harness 与 agent harness 的区分）
- 关联条目：M-024（评测先行——本篇即其缺失的"怎么做"）；K-012（89% vs 52% 缺口的解法）；M-019（OpenAI 三步流程的第 01 步展开）；K-007（METR 任务配置错误案例互证）；M-004（能力评测起步低通过率）

## 一句话结论

历史方法文介绍评分器组合、任务与轨迹审阅；20—50例是作者起步建议，不是通用门槛。它增加方法案例，不意味着评测知识缺口已经闭合；必要行为与安全路径仍须检查。

## 要点摘录（正文级精读，引文逐字取自当次抓取）

### 定义体系（先于方法的贡献）

- 评测对象澄清："When we evaluate \"an agent,\" we're evaluating the harness and the model working together."——评的是 harness+模型组合，不是裸模型。
- **transcript 与 outcome 的区分**："A flight-booking agent might say \"Your flight has been booked\" at the end of the transcript, but the outcome is whether a reservation exists in the environment's SQL database."
- 评测失败的语义风险（创造力案例）："Opus 4.5 solved a 𝜏2-bench problem about booking a flight by discovering a loophole in the policy. It \"failed\" the evaluation as written, but actually came up with a better solution for the user."

### 三类评分器（组合使用）

- 代码类：字符串匹配/二进制测试/静态分析/结果与工具调用验证/transcript 统计——快、廉、客观、可复现（表格原文以列表呈现），但"Brittle to valid variations"。
- 模型类：rubric/自然语言断言/pairwise/参考式/多裁判——灵活但"Requires calibration with human graders for accuracy"。
- 人工类：SME评审/抽查/A-B，用于提供或校准质量判断；专家也可能出错，应保留争议与依据。
- 加权可组合：scoring 可为 weighted（加权过阈值）、binary（全过）、hybrid。

### 能力评测 vs 回归评测（一对必须分开的东西）

- "Capability or \"quality\" evals ask, \"What can this agent do well?\" They should start at a low pass rate, targeting tasks the agent struggles with and giving teams a hill to climb."
- "Regression evals ask, \"Does the agent still handle all the tasks it used to?\" and should have a nearly 100% pass rate."
- 毕业机制："capability evals with high pass rates can \"graduate\" to become a regression suite"。

### 非确定性度量

- pass@k（k 次至少一次成功，随 k 升）/ pass^k（k 次全部成功，随 k 降）："If your agent has a 75% per-trial success rate and you run 3 trials, the probability of passing all three is (0.75)³ ≈ 42%."（该概率乘积需独立且同成功率假设；相关运行不能直接套用。）
- 选型："pass@k for tools where one success matters, pass^k for agents where consistency is essential."

### 路线图 Step 0–8（原文九个标号步骤；下文第 8 条合并了原 Step 7 饱和监控与 Step 8 长期维护）

1. **早开始**："20-50 simple tasks drawn from real failures is a great start"；"Evals get harder to build the longer you wait."
2. 从手动测试/bug 单/support 队列起："Converting user-reported failures into test cases ensures your suite reflects actual usage"（其后原文接 prioritizing by user impact 的分句）。
3. 任务无歧义+参考解："A good task is one where two domain experts would independently reach the same pass/fail verdict."；每个任务配"reference solution: a known working output that passes all graders"；**0% 信号**："a 0% pass rate across many trials (i.e. 0% pass@100) is most often a signal of a broken task, not an incapable agent"。
4. 平衡题集："One-sided evals create one-sided optimization."——web search 案例：该搜的与不该搜的（"who founded Apple?"）双向覆盖，欠触发/过触发调平衡。
5. 稳定隔离的环境："Each trial should be \"isolated\" by starting from a clean environment."；作弊通道案例："we observed Claude gaining an unfair advantage on some tasks by examining the git history from previous trials."
6. 评分器设计："it's often better to grade what the agent produced, not the path it took."（评产出不评路径，防脆）；部分得分；LLM 裁判校准与逃生口："give the LLM a way out, like providing an instruction to return \"Unknown\" when it doesn't have enough information."
7. **读 transcript**："You won't know if your graders are working well unless you read the transcripts and grades from many trials."；"Failures should seem fair: it's clear what the agent got wrong and why."
8. 饱和监控与长期维护："An eval at 100% tracks regressions but provides no signal for improvement."（SWE-bench Verified 30%→>80% 饱和实例）；所有权："dedicated evals teams to own the core infrastructure, while domain experts and product teams contribute most eval tasks"。

### 评分器出错的真实代价（对基准审计的方法论）

- CORE-Bench 案例："Opus 4.5 initially scored 42% on CORE-Bench, until an Anthropic researcher found multiple issues: rigid grading that penalized \"96.12\" when expecting \"96.124991…\", ambiguous task specs, and stochastic tasks that were impossible to reproduce exactly. After fixing bugs and using a less constrained scaffold, Opus 4.5's score jumped to 95%."
- METR 互证："METR discovered several misconfigured tasks in their time horizon benchmark that asked agents to optimize to a stated score threshold, but the grading required exceeding that threshold."
- 总则："we do not take eval scores at face value until someone digs into the details of the eval and reads some transcripts."

### 与其他方法的组合（瑞士奶酪模型）

- "Like the Swiss Cheese Model from safety engineering, no single evaluation layer catches every issue."
- 六法各就位：automated evals（pre-launch/CI）、production monitoring（post-launch）、A/B（有流量后）、user feedback（持续分诊）、transcript review（每周抽样）、systematic human studies（校准 LLM 裁判时）。

## 案例区块

- 实践者与约束：Anthropic 内部（Claude Code、Claude.ai web search、Claude for Chrome）+ 客户（Descript 三维评测、Bolt 三个月建评测体系）。
- 具体做法：见八步路线图。
- 报告的效果：无系统数字（方法论文）；具名案例（CORE-Bench 42%→95%、Qodo 一次性评测失真）为作者自述。
- 对我们的可复现性：**高**——E-02 系列与 E-04/E-07 可直接套用其规约：多 trial 记 pass@k/pass^k、参考解、0% 即查任务、读 transcript。我们的E-04 v4-pro截断混淆正是读 transcript 才能发现 grader/预算问题的实例。

## 适用条件与反证

- 适用条件：已过原型期的生产 agent 团队（作者明言早期原型可以靠手动+直觉）；方法学对模型/厂商泛用。
- 反证/局限：
  - 厂商营销渠道：文末隐含 Claude Code/Agent SDK 工作流推销；方法建议可被独立检验，不能因此称其效果已成立。
  - 案例数字（42%→95%）未经第三方复核。
  - 我方怀疑：八步路线图无成本估计——"20-50 任务"对小团队仍是数周投入；对 evals 的投入回报依赖迭代频率（高频迭代团队回报最大）。
  - "评产出不评路径"有反例压力：安全/合规场景恰恰要审路径（工具调用序列）——作者自己在 grader 清单里也保留 tool_calls 验证，按场景取舍。
- 与 K-012 的关系：观测性 89% vs 评测 52% 的行业缺口 [外注：K-012 调查数据，非本源]，本篇是补齐路径的一手方案。

## 与已有条目的关系

- **M-024**：从"评测先行"（要不要）扩展出完整操作层（怎么做）——旧“认可/缺口关账”判断撤回；本篇仅历史方法线索，现行指导与近期证据另见07_evidence。
- **M-019**：OpenAI 模型选择流程第 01 步（先建 evals）的深度展开，两厂商同向（Anthropic 更系统）。
- **K-007**：METR 基准也有配置错误——"先审基准再比方法"（M-027 同款纪律）获第三方互证。
- **M-004**：能力评测"起步低通过率"与复杂度递增的升级判据同构。
- 评测层缺口清单更新：仍需近期来源、真实失败与评分校准材料，不能由一篇文献宣布主缺口闭合。

## 后续动作

- [ ] 需要复现的主张：无强制；是否采用pass@k/pass^k等度量应按实验问题与重复设计决定，不作为所有实验的固定报告要求。
- [ ] 需要补读的反方/正方：OpenAI Evals 文档（交叉验证 LLM 裁判校准建议）；τ2-bench 论文（模拟用户法细节）。
- [ ] 复核触发器：评测工具大版本（CI 集成形态变化）；6 个月例行。


## 2026-10-14 正文一致性纠正

按既有docs08/总纲裁决及本篇内部证据限制，同步正文中的旧强断言、状态或阅读范围；未重抓来源、未新增效果验证。修改前文本见[_review_archive/2026-10-14-batch13/notes/M-032_demystifying_evals.md](_review_archive/2026-10-14-batch13/notes/M-032_demystifying_evals.md)，仅供历史追溯。
