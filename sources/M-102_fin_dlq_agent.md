# M-102 Fin DLQ Agent：单提示五职责失败与确定性控制层+两个有界判断的重构

## 元信息

- 来源链接：[When should skills become Agents?](https://fin.ai/blog/when-should-skills-become-agents)
- 原文快照（供复核）：`_snapshots_local/batch16_glm_20261018/fin_dlq.html`（SHA-256 e2c7e13a…，见同名 .json）、提取文本 `fin_dlq.txt`（104 行全文）
- 发布日期：2026-10-15（正文 "15 October 2026"）；主张实质更新日期：无
- 数据/事件观测窗口：技能构建于 2026-04 内部探索日；agent 2026-08 上线；41%/4% 数字为 2026-10 发布时点状态（"Five weeks ago, it stood at 4%"）
- 当前适用状态：候选（厂商工程一手叙述，含产品导流）
- 工件/配置/预算及复现范围：博文全文阅读（架构描述、数字、决策原则）；提示原文、回测语料（63 次告警→33 形态）、PR 样例、EMS/Buzz/Ruby gate 代码均未公开；未运行
- 阅读覆盖与媒介限制：全文文字；无图像依赖
- 版本日期：2026-10-18 抓取版本
- 利益关系与独立性：Fin（客服 AI 公司，Intercom 系）官方博客"Building Fin"栏目；文末推广其 Evals and Releases 产品——41% 等数字为厂商自报，营销渠道纪律适用
- 复核触发器：DLQ agent 后续数据（41% 变化/撤回）；第三方或员工独立复盘；架构修订
- 检索日期：2026-10-18（A 类筛选子代理发现，主审读原文）
- 作者/机构：Oisin Hurley / Fin（内部 Infra Platform 团队视角）
- 适用模型：Claude（版本未给；内部 Claude skill 起源）
- 证据等级：经验断言/厂商自报（41% 按 merged PR 计的口径已给，但无原始数据）
- 框架落点：harness 治理（职责分配/动作门控）；评测（回测/每失败成测试）；C 类核心
- 关联条目：M-066（客服运行时）、M-067（任务路由）、M-069（有限决策）、D02/D03/D05/D10

## 一句话结论

Fin 把 DLQ 告警处理从"一个提示做五份工作"（收集证据/判断相关性/推断原因/推荐修复/向人解释——错了不知道哪环错、改提示无法度量改善）重构为"确定性控制层供事实+隔离容器里两个有界判断（错误能否解释告警？故障是瞬态/非瞬态/基础设施？）+类型化工件+Ruby 门选恰好一条动作车道"，以 63 次历史告警去重成 33 形态做回测、每个失败变成新测试，agent 修复占比从 4%（五周前）到 41%（按 merged PR）；该时间变化不是隔离v1/v2的对照，也不证明质量或人力净收益。作者的设计主张是："The model should never be asked to guess a fact it could have been handed."

## 要点摘录

（引号内逐字取自 2026-10-18 抓取正文。）

### 失败的 v1 与归因

- "Our first attempt at a DLQ Agent was not good."——每个告警产长报告、无法核实准确性；"it frequently missed critical details or presented plausible yet inaccurate analysis"；工程师弃用。
- **层归因（A 类核心表述）**："The first version of the Agent failed because we asked one prompt to do five jobs. A single skill was expected to gather evidence, decide which evidence mattered, infer a cause, recommend a fix, and explain everything to an engineer. When its answer was wrong, we could not tell which part had failed. When we changed the prompt, we could not measure whether the system had improved. A system you cannot measure is a system you cannot improve."

### 选题判据（skill vs agent）

- 四条件：frequent / bounded / measurable / actionable（约 1,400 队列×600 worker 类×三区；每周 50 新告警/325 含重触发；占二级 on-call 寻呼 ~80%）。
- 两个先问："Could you deliver 80% of the impact by running the skill manually?" 与模型频繁换代时"When the model changes… does the value of autonomous action justify the additional evaluations, monitoring, and safeguards required to maintain quality?"
- 拒绝通用 AI SRE agent 的理由：内部系统集成不成熟+每家告警流程不同。

### v2 架构（职责分配清单）

- 出口收敛为三结果之一：安全重投 / 针对责任代码的可审修复 PR / 有据升级给人（"says what we know and what we do not"）。
- EMS（事件管理系统）=确定性控制面，先行解析"模型不该猜的事实"：队列/区域、重试配置、积压深度与趋势、worker fleet、近期生产变更、重投历史。
- Buzz 在隔离容器跑调查：先取 Honeycomb/Datadog 错误分布，再调用**两个有界调查判断步骤**（后续动作车道内部的完整模型调用未披露）（错误是否解释告警；故障分类 transient/non-transient/infrastructure）。
- 结果存为类型化工件回传 EMS；Ruby 门验证交接、去重、选恰好一条动作车道（重试车道/代码修复车道/基础设施车道）；"Insufficient or contradictory evidence results in no automatic action. The uncertainty is reported explicitly to a human."；所有结果回贴原告警的 Slack 线程。
- 回测："The initial correlation corpus began with 63 alarm fires, reduced to 33 distinct scenario shapes"；代码修复回测对"人修之前"的仓库状态重放调查（缺陷在、答案不可得）。
- 每失败成测试："If correlation was wrong, we could add the case to the correlation suite. If classification was wrong, we could test that decision without rerunning the entire workflow."

### 结果与边界

- "Currently, 41% of DLQ fixes each week are completed by the Agent when measured by merged PRs. Five weeks ago, it stood at 4%."
- "Not all skills should be Agents… DLQs worked because the problem was frequent, bounded, measurable and actionable."

## 主张卡

| 主张ID | 归属 | 主张与环境范围 | 原文位置与短锚点 | 局限/缺失信息 | 与既有知识的关系 |
|---|---|---|---|---|---|
| FN-1 | 来源记载 | 单提示五职责→错误不可定位+改动不可度量；拆分后各部件可独立测 | "asked one prompt to do five jobs"；"Every failure becomes a test" | v1/v2 无并行数字；厂商叙述 | C 类核心一手例：D03 职责分配的直接对应 |
| FN-2 | 来源记载 | 调查阶段包含两个有界判断；已知运行事实由确定性层供给；动作由代码门控 | "never be asked to guess a fact it could have been handed" | 判断步骤的提示未公开 | D03/D05职责分配的厂商架构叙述，非公开完整实现 |
| FN-3 | 来源记载 | 41% 周修复（merged PR 口径），五周前 4% | "measured by merged PRs" | 无原始数据/置信区间；自报 | 报告自动修复占比的口径样例；未证明质量、节省或总投入收益 |
| FN-4 | 来源记载 | skill→agent 的升级判据四条件+两个先问 | §Picking the right problem | 判据为该公司原则，非验证结论 | D02"增加组件说明修复什么"的操作化清单 |
| FN-5 | 来源记载 | 证据不足→不自动动作+显式升级人类 | "no automatic action" | 升级质量未披露 | D08 退出路径的生产实例 |

## 案例区块

- 实践者与约束：Fin 内部 Infra 平台团队；告警洪泛压垮二级 on-call 的真实运维约束
- 具体做法：如上架构；回测语料+代码修复前状态重放
- 报告的效果：41%（自报，merged PR 口径）
- 对我们的可复现性：可据叙述设计本地候选，但未取得代码、提示、回测语料或逐例输出，不能原样复现；适配和效果均待目标任务验证

## 适用条件与反证

- 适用条件：高频/有界/可测/可动作的内部运维任务；有历史告警语料可回测；动作可门控（PR/重投均可审）
- 反证/局限：厂商博客自报全部数字；无 v1 时期量化基线（只有定性失败描述）；"41%"不含被门控拒绝/升级案例的分母细节；导流 Evals and Releases 产品；单一公司单任务
- [我方审查] 该文与 M-099（Shreya 编排塌缩）互补：Fin提供单提示多职责失败的作者解释，Shreya提供某种多agent尝试的失败观察；它们不构成同任务方案比较，不能合并证明“有界判断单元+确定性胶水”普遍最优

## 与已有条目的关系

- M-066（Snyk 客服共享运行时）：同"确定性层供事实"模式的不同公司实例
- M-069（开放生成与有限决策分开）：本文提供其有限决策侧的一份架构叙述，不作跨来源完整度排名
- M-099：见上——单提示多职责 vs 自由多 agent 两极失败的对照
- M-100：Fin 的"每失败成测试"与 M-100"点修复→扫描器"同为机制化收敛，规模与开放度不同
- D02/D03/D05/D08/D10/D11：六条核心原则在此单一案例中全部有对应实现（候选级证据）

## 后续动作

- [ ] 需要复现的主张：判断本地任务是否有可供给事实、可核验决策和可门控动作，再决定是否试两个有界判断/动作车道；不外推任意内部任务
- [ ] 需要补读的：Fin 的 Evals and Releases 产品文档（判断其评测主张边界）；社区/员工对该文的反馈
- [ ] 复核触发器：41% 后续变化或撤回；架构修订；2027-04 前查新据

## 2026-10-18 主审修正

原文给出调查阶段两项判断，不足限定整个修复流程只有两次模型判断；代码/提示/前后产物缺失，改称架构叙述。41%对4%是两时点merged-PR占比，未给同期分母、任务难度及v1/v2受控比较，不能把比例变化归因职责拆分或等同减轻人工负担。
