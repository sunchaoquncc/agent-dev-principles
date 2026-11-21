# M-053 长文档审阅的分工、覆盖与交付失败

## 元信息

- 来源链接：[原文](https://www.harvey.ai/blog/post-training-rlm-agents-for-m-and-a-diligence)
- 原文快照：[_snapshots_local/batch09/harvey_rlm.html](_snapshots_local/batch09/harvey_rlm.html)，哈希/检索时间见同名.html.json；txt仅定位辅助。
- 发布日期：2026-09-08；主张实质更新日期：未知。
- 检索/审查日期：2026-10-13；验证日期：未验证效果。
- 作者/机构：Niko Grupen等 / Harvey与Baseten
- 适用模型：多种root；主比较subagent Qwen3.6-35B-A3B；深度对照Qwen3.5-122B-A10B等
- 来源类型与利益关系：业务厂商研究自述，合成LAB Diligence任务；一手不等于独立验证。
- 数据/事件观测窗口：实验日期未知；不是客户真实尽调成功率。
- 工件检查范围：正文与深度附录；未复现、未检查训练工件。
- 证据等级：经验断言/作者报告；当前状态：候选，原则升级为零。
- 复核触发器：下一代模型发布、原文修订、反例或新工件出现；超六个月补新据，不刷新旧数据日期。
- 框架落点：prompt / 上下文 / harness及评测安全；关联[总纲](../graph/overview.md)。

## 主张提取

### C1 来源记载

文档全集作为REPL变量，root只接收打印出的内容；子任务在各自上下文读有界资料，再返回结果供root合成备忘录。

范围与位置：Figure 5及An RLM Harness；机制描述。原文短锚点：Only the output the root agent prints

### C2 来源记载

作者报告更深委派出现读了资料却未产出报告的失败；提升资料覆盖也并非普遍减少生成成本。

范围与位置：Coverage and Cost / RLM Recursion Depth；合成任务。原文短锚点：never produced a report

## 局限与解释边界

[我方审查] 评分是LLM按专家rubric的条目通过率，不是任务完成率/法律正确率。主比较50房间、分工30、SFT20、深度14，不能混分母。覆盖与分数关联非隔离因果；多数模型生成成本上升，估价不含全部训练/工程成本。部分深度运行超时，不能只看完成者。

## 与已有知识的比较

补M-050与D03/D04/D12候选：有界输入可伴随更大系统总开销，阅读覆盖与按时交付需同时观察。与播客转述归为同一证据链。

## 下一步

追LAB Diligence公开工件和rubric校准；核时间/调用预算、失败计分及root/subagent分工对照。



## 2026-10-14 Harvey工件复核

固定commit a15650fe74bb20b86f160aaabdad75b87a91b6e8，方法/教程/评分及judge/模板/README与一个Diligence任务全文团队阅读；635条rubric完整遍历，唯一ID/标题/标准无字段缺项。未取得配套VDR，不能验证数字、法律真值或全数据集质量。详见[独立审查](_review_archive/batch12_code_review.md)。

当前score_rubric按全部标准all-pass，error计入分母；这是当前实现口径，不能替换9月文章的条目通过率、预算或旧任务数。缺文件/提取异常可能变占位文字交judge，并非代码硬失败；文件名还有模糊匹配与额外模型调用。judge输入为任务标题、报告与rubric，未自动核原始VDR，多个判分器不等于多个独立业务真值。顶层deliverables别名与sources未在所读score_rubric读取；最后一次结构输出回退与verdict运行校验不足仅为静态疑点，未运行复现。

可迁移的收获：把工件存在/可读、信息提取、语义评审、业务成功分开；分项率、全通过、双judge均值、严格双通过的单位不能混用。旧实验日志、人工校准未获是外部证据边界，本轮已取七工件的阅读已完成。
