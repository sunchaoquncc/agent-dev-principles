# M-040 从失败轨迹到可回退配置

## 元信息

- 来源链接：[原文](https://commandline.microsoft.com/the-agent-optimization-loop-and-how-we-built-it-in-foundry/)
- 原文快照：[_snapshots_local/batch07/microsoft_optimization_loop.web.txt](_snapshots_local/batch07/microsoft_optimization_loop.web.txt)；同名.json记录哈希及检索方式。
- 发布日期：2026-06-02；页面日期核得。
- 主张实质更新日期：未知
- 数据/事件观测窗口：产品经验；差旅例为说明性运行，未公开生产样本窗
- 检索日期 / 本次审查日期：2026-10-13 / 2026-10-13
- 作者/机构：Vivek Bhaduria / Luis Quintanilla / Saket Sathe（Microsoft）
- 适用模型：文中举gpt-4o、gpt-4.1-mini；当前模型未验证
- 验证日期：未验证（本轮原文核对，不是模型/业务效果复现）
- 当前适用状态：有条件方法建议；效果主张仍为经验断言。
- 证据等级：经验断言；可设计验证，不标已验证。
- 工件/配置/预算及复现范围：本地原文与摘取文本；未调用付费模型，未运行来源应用。
- 利益关系与独立性：Foundry产品自述，非独立效果验证
- 框架落点：prompt治理 / harness治理 / 评测
- 关联条目：M-024/M-037；D03/D09/D11/D12；总纲见[overview](../graph/overview.md)。
- 复核触发器：下一代模型发布、工具/业务政策/评分器变化或目标栈出现反例；最迟在证据超6个月前检查是否有新据。

## 一句话结论

有可靠轨迹与评测后，配置改动应跨场景回归，不能只修单例。

## 原文要点与锚点

Optimization loop 描述候选生成、同集多维评分、开发者审阅和版本回退；作者承认集外回归，A/B部署在文中仍为未来工作。

定位片段（只用于回查，不是结论证明）：same dataset, deterministic comparison

## 适用条件与反证

漏预算检查不能直接归因指令；reflector优于执行模型缺公开消融，拒绝采纳其普遍优先级。相同数据不保证生成或评分确定性。

## 消化与案例应用

[我方推导] 先把故障定位到prompt/事实/工具/权限/基础设施，再决定调配置；D03/D09/D11保留此流程。审批金额强制点放执行端，不能依赖提示遵守。

## 后续动作

- 在具体业务契约下收集正例、拒绝例和故障恢复例；先校准真值再做效果实验。
- 如没有目标业务或真实数据，保留为设计候选，不以模拟补成生产证据。

抓取说明：urllib返回403；保存的是web工具可读正文，不是服务器原始HTML。页内L行号保留，哈希只证明本地工件未变。

