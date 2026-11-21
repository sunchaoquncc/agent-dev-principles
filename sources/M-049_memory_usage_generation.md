# M-049 记忆使用与记忆生成需要分别观察

## 元信息

- 来源链接：[原文](https://www.letta.com/blog/evaluating-memory-in-production-agents/)
- 原文快照：[_snapshots_local/batch09/letta_memory.html](_snapshots_local/batch09/letta_memory.html)，哈希/检索时间见同名.html.json；txt仅定位辅助。
- 发布日期：2026-07-28；主张实质更新日期：未知。
- 检索/审查日期：2026-10-13；验证日期：未验证效果。
- 作者/机构：Letta
- 适用模型：文中含Opus-5/Fable-5、GPT-5.6系列、Kimi-K3等；用户模拟Sonnet-5，评分GPT-5.6-Sol
- 来源类型与利益关系：记忆产品厂商私有基准报告；一手不等于独立验证。
- 数据/事件观测窗口：生产轨迹启发的合成任务；生产轨迹采集日期未提供。
- 工件检查范围：正文方法、失败案例与局限；未读取图片中的精确跑分，未复现。
- 证据等级：经验断言/作者报告；当前状态：候选，原则升级为零。
- 复核触发器：下一代模型发布、原文修订、反例或新工件出现；超六个月补新据，不刷新旧数据日期。
- 框架落点：prompt / 上下文 / harness及评测安全；关联[总纲](../graph/overview.md)。

## 主张提取

### C1 来源记载

作者分别观察记忆使用中的遵循/检索，以及记忆生成中的泛化/清理，并以原始与清理后的记忆档案构造场景。

范围与位置：Creating Realistic Memory / Agent memory profiles。原文短锚点：original anonymized memory profile

### C2 来源记载

报告的失败包括把新纠正追加在旧规则后而不消除矛盾，以及有相关外部记忆却直接作答。

范围与位置：Generalized learning / Retrieving context；作者示例。原文短锚点：simply logging the feedback

## 局限与解释边界

[我方审查] Context-Bench V2为私有基准，任务由生产轨迹生成而非真实生产效果；未给足够公开样本及评分校准供复现。把疑似注入规则删除计为遵循失败反映该场景的评分目标，不能推广为永远服从记忆。

## 与已有知识的比较

补M-014/M-010：记录经验、修改规则、实际检索与行为改变不是一件事。与M-048是不同机构的方法补充，非同任务效果交叉验证。

## 下一步

寻公开任务和人工评分；重点找错误泛化、保留过期规则与删除合法约束的双向失败。



## 2026-10-14 正文一致性纠正

按既有docs08/总纲裁决及本篇内部证据限制，同步正文中的旧强断言、状态或阅读范围；未重抓来源、未新增效果验证。修改前文本见[_review_archive/2026-10-14-batch13/notes/M-049_memory_usage_generation.md](_review_archive/2026-10-14-batch13/notes/M-049_memory_usage_generation.md)，仅供历史追溯。
