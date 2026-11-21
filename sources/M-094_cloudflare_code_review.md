# M-094 Cloudflare AI Code Review：CI 关键路径上的多审阅者编排与职责分工

## 元信息

- 来源链接：[Orchestrating AI code review at scale](https://blog.cloudflare.com/ai-code-review)
- 原文快照（供复核）：`_snapshots_local/batch15/cloudflare_code_review.md/.html/.txt`（HTML SHA-256 65e5e7e8…）
- 发布日期：2026-04-20T13:00Z（页面 schema datePublished，本批从快照原文核验）；修订 2026-07-15T14:34Z（schema dateModified，修订内容未说明）
- 主张实质更新日期：未知（dateModified 与发布差近 3 个月，改了什么未披露）
- 数据/事件观测窗口：**2026-03-10 至 2026-04-09**（正文明示 30 天窗口）——注意：该窗口结束日距今（2026-10-14）已越 6 个月线 5 天；本文按**工程案例（方法+工件）**收录，运行数字不作现行效果主张
- 当前适用状态：历史工程/运行基线快照（一手厂商复盘）；数据期已越六个月，不据此升级现行效果指导
- 工件/配置/预算及复现范围：正文全文（含全部代码片段、表列数据）阅读；系统未开源（内部 GitLab CI component），代码片段为正文节选；无逐 MR 原始数据
- 阅读覆盖与媒介限制：正文全文；示例审查截图未核像素（只有一张"particularly egregious review"示例）
- 版本日期：2026-10-14 抓取版本（含 07-15 修订）
- 利益关系与独立性：Cloudflare 工程博客（Ryan Skidmore，员工一手）；Agents Week 2026 系列之一（产品生态叙事背景）；基于开源 OpenCode（Cloudflare 称已上游 45+ PR）；反面讨论存在（HN 48276152 等，本批经④组筛选 subagent 检索确认线索，未逐帖精读）
- 复核触发器：系统开源或数据公开；dateModified 实质修订披露；第三方复现（如 alexop.dev 250 行复现贴）扩展；同类系统对比出现
- 检索日期：2026-10-14（④组筛选 subagent 先核，主审本批全文复读并逐数核对）
- 作者/机构：Ryan Skidmore / Cloudflare
- 适用模型：Claude Opus 4.7/GPT-5.4（协调者）、Claude Sonnet 4.6/GPT-5.3 Codex（重型子审）、Kimi K2.5（文档/发布/AGENTS.md）；通过 AI Gateway
- 证据等级：经验断言（厂商生产自报；无人工标注准确率/召回率）
- 框架落点：harness 治理（CI 关键路径编排、预算、降级）；prompt 治理（What NOT to Flag、注入边界）；评测（度量管道）；安全（注入防护、break-glass）
- 关联条目：M-017（多 agent 协调）、M-033（长运行/超时/重试）、M-040（可回退配置）、M-067（任务路由）、M-088（工件可审性对照）；D02/D05/D11

## 一句话结论

这是历史工程快照：专项模型提发现并标级，协调模型去重、核实与终判；代码按diff特征选择审查规模并管理超时、熔断、回退和执行接口。作者把低findings量部分归因于负向提示边界，平均费用是另一项整体观察；无前后对照和人工质量标注，不能从1.2 findings/次或$1.19/次推准确率或提示降本。
## 要点摘录

（引号内逐字取自 2026-10-14 抓取正文；数字均经主审对表复核。）

### 失败起点（朴素方案的失败模式）

- "The results were exactly as noisy as you might expect, with a flood of vague suggestions, hallucinated syntax errors, and helpful advice to 'consider adding error handling' on functions that already had it."
- E2BIG 事故：巨型 MR 描述作命令行参数触发 ARG_MAX——改为 stdin 传入（正文代码注释明示）

### 架构与职责分工（本篇核心）

- 最多 7 个专项审阅者（安全/性能/代码质量/文档/发布/合规/AGENTS.md），协调者去重、判级、合并为一条结构化评论；子审阅者独立读文件/grep，"The coordinator doesn't see or control what tools the sub-reviewers use"
- 模型分层按职责：顶配模型只给协调者（读 7 个模型输出+去重+终判），标准级给重型子审，轻量文本类给 K2.5——与 M-067 任务路由同向，且给出"协调比审查更难"的分工理由
- 审批偏置明确："The bias is explicitly toward approval"；rubric 五档（approved→requested_changes）

### 提示层工件（真实片段，非示意）

- 安全审"What NOT to Flag"四条（逐字）："Theoretical risks that require unlikely preconditions / Defense-in-depth suggestions when primary defenses are adequate / Issues in unchanged code that this MR doesn't affect / 'Consider using library X' style suggestions"
- 作者判断："It turns out that telling an LLM what not to do is where the actual prompt engineering value resides."
- 注入防护：剥离用户可控 MR 文本中的边界标签（PROMPT_BOUNDARY_TAGS 正则，9 个标签）——XML 结构拼接下的提示注入防御实例，与 M-093/M-021 同线
- token 分层：diff 写盘传路径（不嵌 prompt）；共享上下文文件一次抽取七审共用（"duplicating even a moderately-sized MR context across seven concurrent reviewers would multiply our token costs by 7x"）

### harness层的资源路由与故障控制（不含协调模型语义终判）

- 风险三档：trivial（≤10 行且≤20 文件，2 agent 且协调者降级 Sonnet）/ lite（≤100 行且≤20 文件，4 agent）/ full（示例代码fallback包含行数>100或文件数>20以及敏感路径；表格只列部分条件，不能把21—50文件的小diff漏掉，7+ agent）——assessRiskTier 函数原文在正文中
- 三级超时（单任务 5min/代码质量 10min、整体 25min、重试预算 2min）+60 秒无输出即杀；熔断器（Hystrix 式三态）+代际回退链（opus-4-7→4-6，**仅 429/503 触发**；Auth/上下文溢出/中止不触发回退——"a different model won't fix bad credentials"）
- 控制面：Workers KV 动态禁用 provider（"every running CI job will route around it within five seconds"）；break glass 逃生阀（人工评论强制通过，开工前检测并计入遥测）
- 心跳日志解决"模型思考被当挂死"（"almost entirely eliminated the problem"）——与 M-090 进度更新渲染同一问题的 CI 版

### AGENTS.md 审阅者（上下文文件维护机制）

- 检测"架构变更但 AI 指令未更新"并按 materiality 三档提示；反模式清单：generic filler、">200 lines that cause context bloat"、无命令的工具名——本库"原则层薄/案例层厚"设计的跨厂商呼应（[我方推导]）

### 度量（30 天窗口，全部厂商自报）

- 5,169 仓库 / 48,095 MR / 131,246 次审查（平均 2.7 次/MR）/ 159,103 findings（≈1.2/次）
- 成本：均值 $1.19、中位 $0.98、P99 $4.45；时长中位 3m39s、P99 10m21s
- 分层成本：trivial $0.20 / lite $0.67 / full $1.68
- token：约 120B 总量、缓存命中 85.7%；分层明细表（顶配 51.8%/标准 46.2%/K2.5 经 Workers AI 计 0% 成本行）
- 逃生阀：288 次（"0.6% of merge requests"）
- findings 分布表：Code Quality 74,898（约半数）、Security 11,985（critical 484，占其 4%）

### 诚实限制段（作者自认）

- "This isn't a replacement for human code review, at least not yet with today's models."：架构感知、跨系统影响、细微并发 bug 三弱项；成本随 diff 规模增长（协调者 prompt 超 50% 上下文窗口时告警）

## 口径审查（本批执行）

- **无准确率/召回率**：159k findings 无人工标注质量数字；"flags real bugs with impressive accuracy"为开篇修辞，无数据支撑——findings 计数≠正确发现数，本笔记不引用该修辞作证据
- **break glass 率的双重解释**：0.6% 可读作"系统可信"也可读作"团队对机器阻塞的容忍度/流程压力"，正文未区分
- **数据窗口越线**：运行数据止于 2026-04-09（按原批10-14基准已超六个月5天，主审10-16为7天）；发布 04-20、修订 07-15 不能刷新数据新鲜度（项目规则）。数字按当时快照登记
- **无失败样本原文**：无被误标 MR 的原文级案例、无改进前后审查输出对比——④组缺口确认，本文是"机制+度量"成套而非"失败输入→变更→前后产物"全链成套
- 模型代际：Opus 4.7/Sonnet 4.6/GPT-5.4/5.3/K2.5——与 M-090 的 Opus 5.5 代际无冲突（写于 4 月），回退链设计（跨代可用）仍可参照，具体型号对照不作现行建议

## 主审发现的跨表冲突（2026-10-16）
findings七类明细合计145,207，与总数159,103差13,896；risk-tier审查次数合计130,698，与总数131,246差548。正文未解释分母/分类遗漏，保留冲突，不自行补齐。系统有度量管道不等于汇总口径完整或准确。
“What NOT to Flag”与低findings量的联系是作者解释；费用是全系统同时报告的观察，两者不能串成已证因果。少发现也可能漏报，无标注不能裁决。

## 案例区块

- 实践者与约束：Cloudflare 内部（5,169 仓库规模、GitLab CI、工程师等待时间是原始痛点——"median wait time for a first review was often measured in hours"）
- 具体做法：专项子审+协调者判级；风险三档路由；熔断/回退/逃生阀；注入边界剥离；共享上下文文件避免重复拼接（各模型实际读入成本未作独立对照）；AGENTS.md 维护审阅者
- 报告的效果：上述 30 天度量（作者自报，度量管道 review-tracker+Prometheus 随文说明）
- 对我们的可复现性：结构化findings、模型协调与代码路由/恢复可作历史设计对照；迁移及验证仍需本地投入，不称零成本或任意场景适用；数字不可复算（无原始数据）；本地可做"What NOT to Flag 式负向边界"对 findings 密度的影响小试验（需模型，不在本批）

## 适用条件与反证

- 适用条件：CI 关键路径、多仓库、有度量管道的工程组织；对"findings 结构化+下游确定性处理"的职责分工模式
- 反证/局限：
  - 作者自认：三弱项+非人类替代+大 MR 成本
  - 本批审查新增：无质量标注；数据窗口越线；无失败原文；单案例单组织；break glass 双读法
  - 反面线索（未精读）：HN 信噪比质疑帖、AI code review bubble 讨论、第三方 250 行复现贴（alexop.dev）——后续可作交叉验证入口
- 与 M-017（Cognition 多 agent 论争）：本文是多 agent 编排在**审阅聚合**场景的生产实例（子审相互独立、协调者裁决），不与"上下文分裂型多 agent"冲突（子审间无共享任务状态）

## 与已有条目的关系

- D02（编排按任务特性）：风险三档+模型分层的生产实例
- D05（工具与副作用）：结构化findings+模型协调判断+执行接口；系统未公开，不能断言approve/block语义判断全由代码实现
- D11（成本口径）：分层成本/缓存/token表可作记录样式，跨表差异保留，不能称成本完整性已核
- M-088/M-087（实务工件对照）：本文给出较多运行度量，但缺同例前后质量工件；不据不同材料的披露量作完整度排名——四项工件标准（失败输入/变更/前后产物/评价依据）中本文强在变更+评价依据、弱在失败输入与前后产物
- M-093：边界标签剥离是防御设计尝试（未独立测防御有效性）；M-090：心跳/进度呈现的 CI 变体

## 后续动作

- [ ] 需要复现的主张：无付费复现立项；"负向边界压低 findings 密度"可列低成本试验候选（10 个真实 diff 对照）
- [ ] 需要补读的反方/正方：HN 48276152 及 bubble 帖逐帖核读；alexop.dev 第三方复现；dateModified 07-15 修订内容（若 Wayback 有 04-20 原版可比对修订实质）
- [ ] 复核触发器：系统开源/数据公开/实质修订披露/第三方复现扩展；同类系统对比

## 2026-10-16 主审纠正

原稿将协调模型的去重/判级错归确定性代码、把负向边界归因扩为成本、称完整度量，均已纠正并同步细则。保留历史机制案例；失败输入→同例变更→前后产物→质量标注的完整工件缺口仍未补齐。数据截至10-14越线5天，截至本轮10-16越线7天，不因07-15页面dateModified刷新。
