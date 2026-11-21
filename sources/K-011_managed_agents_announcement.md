# K-011 Claude Managed Agents 产品公告（Q-001 行为证据）

> 当前用途（2026-10-14）：以下保留来源当时的做法与作者主张，仅作历史/自我修订对照；不将旧型号处方或旧“认可”记录作为现行要求。当前原则状态见[证据登记](../principles/07_evidence.md)，效果仍未验证。

## 元信息

- 来源链接：https://claude.com/resources/articles/claude-managed-agents
- 原文快照（供复核）：https://web.archive.org/web/20261013080600/https://claude.com/resources/articles/claude-managed-agents
- 发布日期：2026-04-08
- 检索日期：2026-10-13
- 作者/机构：Anthropic（产品公告）
- 适用模型：Claude 平台服务（非模型特定）
- 证据等级：经验断言（厂商产品公告=营销渠道，所有数字未经第三方验证）
- 框架落点：harness 治理（厂商内置化）；安全（托管沙箱/权限）
- 关联条目：Q-001（平台产品化的直接观测，不是模型吸收测量，DevDay 2025 AgentKit 为其已知证据清单中的同类动作）；M-029（同日工程博客，本篇的技术背书）

## 一句话结论

Anthropic 把 agent 循环、上下文管理、错误恢复、状态/记忆/权限基础设施整体内置为云服务（"A built-in orchestration harness decides when to call tools, how to manage context, and how to recover from errors"）——harness功能于2026年产品化托管的历史事件，与 OpenAI AgentKit 构成跨厂商同向证据。

## 要点摘录（引文逐字取自当次抓取）

- 定义："Claude Managed Agents is a suite of composable APIs for building and deploying cloud-hosted agents at scale. It pairs an Anthropic-managed harness with production infrastructure for state, memory, permissions, and scheduled execution."
- 吸收范围（harness 治理的核心职能逐项内置）："A built-in orchestration harness decides when to call tools, how to manage context, and how to recover from errors."
- 自评目标机制（研究预览）："you define outcomes and success criteria, and Claude self-evaluates and iterates until it gets there"
- 内部测试数字（营销渠道纪律：无方法学细节、无第三方验证）："In internal testing around structured file generation, Managed Agents improved outcome task success by up to 10 points over a standard prompting loop, with the largest gains on the hardest problems."
- 功能清单：沙箱化执行、数小时级长会话（断连后进度与产出持久）、多 agent 协调（研究预览）、scoped permissions/身份管理/执行追踪。
- 状态：public beta（发布当日）。
- 客户引语（Atlassian/Sentry/Notion/Rakuten 等）：页面自身以"10x"为主张框架（标题即"get to production 10x faster"）；客户引语中含"weeks instead of months"（如 Sentry 段）——按信源纪律不作为证据登记。

## 案例区块

- 实践者与约束：Anthropic 商业化团队；面向不愿自建 agent 基础设施的开发者/企业。
- 具体做法：托管 harness+生产基础设施组合 API；按 token 与 session 运行时计费 [外注：计费维度来自 platform.claude.com 文档检索摘要，公告正文未展开]。
- 报告的效果：作者自述（见上）；无第三方数据。
- 对我们的可复现性：本轮未复现托管实现；仍可另设计目标任务验证，不把不可取得服务端源码等同无法评测。可作为 Q-001 观测的定期盘点对象（功能边界变化仅为平台托管记录，不是模型吸收进度）。

## 适用条件与反证

- 适用条件：不适用"原则"——本条目是**事件记录**，不是方法主张。
- 反证/局限：纯营销文本；"10 points""10x"类数字一律按信源纪律标经验断言；真实能力边界看 M-029 工程文与后续用户反馈。
- 与 Q-001 的关系：平台托管的事件证据，非模型能力吸收证据——此前观测多为"厂商逐步内置单点功能"（compaction、memory tool），本事件是整层 harness 治理的打包内置。

## 与已有条目的关系

- Q-001 观测表新增一行（2026-04-08，整层产品化托管）。
- 与 OpenAI AgentKit（Q-001 已知证据：DevDay 2025-10-06）跨厂商同向：两家先后把 agent 编排内置为产品——这说明多厂商提供托管编排，不说明外部工程已消失。
- M-029 提供其工程实质，避免只看营销叙事。

## 后续动作

- [ ] 需要复现的主张：无。
- [ ] 需要补读的反方/正方：HN 讨论（社区对命名/锁定/营销的质疑）；Cloudflare 集成公告 [外注：WebSearch 检索结果示 blog.cloudflare.com 2026-05-19，未抓取核验]；正式 GA 时的范围变化。
- [ ] 复核触发器：GA/定价/范围变更时更新本条；6 个月例行。


## 2026-10-14 正文一致性纠正

按既有docs08/总纲裁决及本篇内部证据限制，同步正文中的旧强断言、状态或阅读范围；未重抓来源、未新增效果验证。修改前文本见[_review_archive/2026-10-14-batch13/notes/K-011_managed_agents_announcement.md](_review_archive/2026-10-14-batch13/notes/K-011_managed_agents_announcement.md)，仅供历史追溯。
