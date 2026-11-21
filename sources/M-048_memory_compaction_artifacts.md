# M-048 记忆、压缩与业务事实工件的分工

## 元信息

- 来源链接：[原文](https://developers.openai.com/cookbook/examples/agents_sdk/building_reliable_agents_memory_compaction)
- 原文快照：[_snapshots_local/batch09/openai_memory.html](_snapshots_local/batch09/openai_memory.html)，哈希/检索时间见同名.html.json；txt仅定位辅助。
- 发布日期：2026-05-01；主张实质更新日期：未知。
- 检索/审查日期：2026-10-13；验证日期：未验证效果。
- 作者/机构：Wesley Pasfield、Emre Okcular / OpenAI
- 适用模型：示例gpt-5.5；checkpoint压缩gpt-5.4-mini；SDK版本未固定
- 来源类型与利益关系：官方教学代码示例；一手不等于独立验证。
- 数据/事件观测窗口：合成证据批次；未提供实测运行日期。
- 工件检查范围（当前）：现有提取正文和全部可见内嵌代码已全文复读，未执行notebook；细节见文末复读。
- 证据等级：经验断言/作者报告；当前状态：候选，原则升级为零。
- 复核触发器：下一代模型发布、原文修订、反例或新工件出现；超六个月补新据，不刷新旧数据日期。
- 框架落点：prompt / 上下文 / harness及评测安全；关联[总纲](../graph/overview.md)。

## 主张提取

### C1 来源记载

示例把当前工作状态交给压缩、跨运行的方法经验交给记忆、个案结论交给带引用且供人审查的备忘录。

范围与位置：Memory vs Compaction / Step 3；合成资料审阅示例。原文短锚点：workflow lessons, not investigation facts

### C2 来源记载

示例默认不执行模型，数据规模小，展示checkpoint辅助函数与预期输出；实际调用在基线结束后，未展示组合运行/随后恢复，不能算运行结果。

范围与位置：前置说明与Step 2/4；读代码未运行。原文短锚点：RUN_AGENT defaults to False

## 局限与解释边界

[我方审查] 没有压缩前后质量或成本对照。记忆写入限制主要是提示要求，不能据此宣称运行机制已保证隔离；生成备忘录也不自动等于人已审定。发布日期不保证滚动代码在首发时即为当前版本。

## 与已有知识的比较

补M-044/M-045及D04候选的信息生命周期案例；支持区分方法经验与业务事实的设计思路，不验证本库流程有效。

## 下一步

取得固定commit，检查压缩checkpoint实际输入、记忆生成内容及事实污染失败例。



## 2026-10-14 全文反方复读

现有1258行提取文本（正文672—1256，全部内嵌代码）已全文复读，未执行notebook；原HTML对调用名做有限交叉定位。可见代码只调用baseline_run，没有final_run赋值/组合调用；强制checkpoint在Runner.run结束后，不是三批之间，未展示随后恢复。初始Manifest同时放三批，只靠提示要求按批读取。跨run记忆消费也未演示，不能从Memory API名称推断共享/隔离范围。原文ENABLE_TRACING与代码DISABLE_TRACING不一致。max_turns12不等于压缩/记忆/全流程费用预算。手写EXAMPLE_OUTPUT不是模型输出或人工核验结果；基线仅一批而组合目标三批，不能直接作机制消融。

纠正旧“强制阶段checkpoint展示压缩”的宽泛措辞：本快照展示辅助配置与函数，未完成组合运行和恢复实演。可能是页面渲染/源notebook遗漏，未核固定notebook，不称SDK缺此能力。保留方法经验与个案事实分离作为设计意图，非已验证持久记忆效果。

范围及逐行证据见[独立报告](_review_archive/batch12_memory_full_review.md)；日期不刷新，效果不升级。


## 2026-10-14 正文一致性纠正

按既有docs08/总纲裁决及本篇内部证据限制，同步正文中的旧强断言、状态或阅读范围；未重抓来源、未新增效果验证。修改前文本见[_review_archive/2026-10-14-batch13/notes/M-048_memory_compaction_artifacts.md](_review_archive/2026-10-14-batch13/notes/M-048_memory_compaction_artifacts.md)，仅供历史追溯。

## 2026-10-18 有界筛查（docs29附带项）

页面重抓对比 2026-10-13 快照：文章正文无变化（规范化 diff 的全部差异在文档站导航层，如新增 Evaluation/Promptfoo 导航项）；无新工件、无日期变更。六个月复核节点（2026-11-01）临近，届时按触发器处理，本项本轮关闭。
