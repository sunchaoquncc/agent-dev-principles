# M-039 客服质量与成本：模拟教程的适用边界

## 元信息

- 来源链接：[原文](https://developers.openai.com/cookbook/examples/agent_optimization/optimizing_agents_for_cost_and_quality.md)
- 原文快照：[_snapshots_local/batch07/openai_customer_support.md](_snapshots_local/batch07/openai_customer_support.md)；同名.json记录哈希及检索方式。
- 发布日期：2026-09-14；网页标题区日期已另存 *_page.html，不能用正文 Last verified 代替发布日期。
- 主张实质更新日期：未知；正文参考项Last verified为2026-09-14
- 数据/事件观测窗口：合成工单，非生产观察
- 检索日期 / 本次审查日期：2026-10-13 / 2026-10-13
- 作者/机构：Emre Okcular / Lara Rachidi（OpenAI）
- 适用模型：示例GPT-5.4；提及GPT-5.6；不代表GPT-6验证
- 验证日期：未验证（本轮原文核对，不是模型/业务效果复现）
- 当前适用状态：有条件方法建议；效果主张仍为经验断言。
- 证据等级：经验断言；可设计验证，不标已验证。
- 工件/配置/预算及复现范围：本地原文与摘取文本；未调用付费模型，未运行来源应用。
- 利益关系与独立性：厂商教程/营销；与M-041计同组
- 框架落点：评测 / harness治理 / 上下文治理
- 关联条目：M-024/M-011；D10/D11；总纲见[overview](../graph/overview.md)。
- 复核触发器：下一代模型发布、工具/业务政策/评分器变化或目标栈出现反例；最迟在证据超6个月前检查是否有新据。

## 一句话结论

可借用质量先行的比较流程，不能采用模拟收益作为模型选型依据。

## 原文要点与锚点

Success criteria 与 Simulation contract 明示默认模拟：路由和动作来自标签，token/时延/质量含估算或公式；后台移出同步路径仍计费。可选LLM judge只评已有合成答案，非运行真实agent。

定位片段（只用于回查，不是结论证明）：Routing and optimized actions come from the fixture labels

## 适用条件与反证

基线故意低效，关键词检查不足以判断事实，judge错误或缺失还会影响覆盖率。近期文章仍使用旧代示例模型，不采用价格或收益为现行处方。

## 消化与案例应用

[我方推导] 把分组质量门、后台/重试/人工完整成本放入D11。真实系统需换成实际工具状态、真实usage与校准评分，才比较配置。

## 后续动作

- 在具体业务契约下收集正例、拒绝例和故障恢复例；先校准真值再做效果实验。
- 如没有目标业务或真实数据，保留为设计候选，不以模拟补成生产证据。

