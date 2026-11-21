# M-052 AQuA：从对话失败定位到部署版本

## 元信息

- 来源链接：[原文](https://developers.googleblog.com/the-outer-loop-insights-first-an-ambient-quality-agent-that-diagnoses-your-production-agent/)
- 原文快照：[_snapshots_local/batch09/google_aqua.html](_snapshots_local/batch09/google_aqua.html)，哈希/检索时间见同名.html.json；txt仅定位辅助。
- 发布日期：2026-10-08；主张实质更新日期：未知。
- 检索/审查日期：2026-10-13；验证日期：未验证效果。
- 作者/机构：Dima Melnyk、Elia Secchi / Google
- 适用模型：示例review/cluster Gemini 3.1 Pro；verify 3.7 Flash；diagnosis 3.8 Flash
- 来源类型与利益关系：厂商参考实现与脚本化回放示例；一手不等于独立验证。
- 数据/事件观测窗口：示例运行日期未给；32会话为四个脚本旅程的重复回放。
- 工件检查范围（当前）：正文及两个选定节点源码全文已读；不是全仓审计，未运行，见文末固定版本复核。
- 证据等级：经验断言/作者报告；当前状态：候选，原则升级为零。
- 复核触发器：下一代模型发布、原文修订、反例或新工件出现；超六个月补新据，不刷新旧数据日期。
- 框架落点：prompt / 上下文 / harness及评测安全；关联[总纲](../graph/overview.md)。

## 主张提取

### C1 来源记载

流程把采样、会话审查、聚类、回查原对话、跟踪拆开；诊断同时读取失败轨迹和部署时源码快照。

范围与位置：What AQuA is / Diagnose；参考实现描述。原文短锚点：immutable source snapshot

### C2 来源记载

作者明确静态回放不重建外部状态；基于少量全文的簇验证也不核实所有成员。

范围与位置：Hard problems / Findings；模型验证不是因果证明。原文短锚点：static replay does not reconstruct external environment state

## 局限与解释边界

[我方审查] verified是模型抽查后的产品状态，不等于人工真值或因果成立；引用行存在也不证明归因正确。修复前后复用同批脚本，无独立保留集；未见14天不等于缺陷已修复。成本依轨迹深度，根因诊断另计。

## 与已有知识的比较

补M-040/M-042：同样正常HTTP也可能业务错；缺失信息传递、工具与提示不匹配可定位到不同责任层。Google同源材料不重复计票。

## 下一步

检查google/adk-recipes的ambient-quality-agent实现与漏检例；增加环境快照与独立回放，非先要求所有项目部署AQuA。



## 2026-10-14 第十二批复核

关联[总纲](../graph/overview.md)及[工件审查](./_review_archive/batch12_code_review.md)。本次静态阅读全文/代码，不是运行效果验证；固定commit、文件哈希、范围见审查报告与batch12同名快照元数据。历史判断保留，以下限制优先。

AQuA两个节点中error、failed、passed有区分：没有finding才判passed，不能等同客观业务成功；预算<=0会跳过。目标不可读时可能继续无目标评审并警告，不能声称目标总是完整。goal版本/prompt hash与session revision有节点级记录；不可变全依赖快照、根因与14天resolved算法不在本次代码范围。采样分母与未知结果应单列，不把reviewed当成功数。


## 2026-10-14 正文一致性纠正

按既有docs08/总纲裁决及本篇内部证据限制，同步正文中的旧强断言、状态或阅读范围；未重抓来源、未新增效果验证。修改前文本见[_review_archive/2026-10-14-batch13/notes/M-052_aqua_failure_diagnosis.md](_review_archive/2026-10-14-batch13/notes/M-052_aqua_failure_diagnosis.md)，仅供历史追溯。
