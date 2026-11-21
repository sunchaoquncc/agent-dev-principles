# M-046 上下文文件消融：阴性结果的范围

## 元信息

- 来源链接：[原文](https://arxiv.org/html/2607.27250v1)
- 原文快照：[_snapshots_local/batch08/context_ablation.html](_snapshots_local/batch08/context_ablation.html)；哈希与获取时间见同名.html.json；检索文本.txt仅供定位。
- 发布日期：2026-07-28；主张实质更新日期：未知。
- 检索/审查日期：2026-10-13；验证日期：未验证效果。
- 作者/机构：Prakhar Khatri / Independent Researcher
- 适用模型：claude-sonnet-4-6、gpt-5.5，分别通过Claude Code与Codex CLI
- 数据/事件观测窗口：正文未给统一运行日期；模型为该研究快照
- 利益关系与独立性：单作者预印本；作者公开仓库，未确认完成同行评议或第三方复现
- 证据等级：作者报告，未独立复现；当前适用状态：研究候选。
- 工件/配置/预算及复现范围：本轮读正文；未运行agent、未调用付费API。
- 框架落点：prompt / 上下文 / 评测；关联[总纲](../graph/overview.md)。
- 复核触发器：下一代模型发布、来源修订、取得原始工件或出现相反结果；超六个月复核新据，不刷新旧数据日期。

## 主张提取

### C1 来源记载

研究在三个Python仓库比较无额外上下文、常驻文件和按需wiki，报告未检出正确率改善；不是上下文普遍无效的证明。

范围：15/17任务、3次重复；291次运行中288有有效正确率评分，3次crash/timeout排除于正确率分析。定位短锚点：not a powered equivalence claim

### C2 来源记载

按需wiki在两个仓库比原文件内容更广；不同agent注入通道也不同，限制通道与模型间归因。

范围：Method 3.3与Limitations；小样本与生态效度另受限。定位短锚点：its corpus is not content-matched

## 局限与解释边界

[我方审查] 摘要的等效界限措辞比正文的检验能力限制更强，不能采用为确定上界。把主要失败解释为能力而非知识是作者对样本的归因，非通用结论；更多材料可能增噪，不能接受作者称内容混杂只会加强阴性结果的单向解释。

## 与已有知识的比较

对Q-004/M-007提供限制证据：上下文策略效果需要任务与实现条件。既不证明本库原则有效，也不推翻知识库价值。无原则升级。

## 下一步

公开仓库https://github.com/codeprakhar25/context-files-coding-agents 已打开：存在聚合结果/分析代码；README说明原始jsonl轨迹未随库公开。首轮未下载数据；第十二批已完成下述聚合数据/选定统计工件审计，仍未运行模型复现。后续重点为排除字段、原始轨迹和统计口径澄清。



## 2026-10-14 全文/统计复核

固定commit cfa048e5a83284ac1ba768c0928ec03e6f381865的README、数据字典、179行power_analysis及统计登记全文已读，公开CSV291记录全部解析并自写标准库核算，未执行来源模型/代码。发现：①Claude直接均值25/47、25/46、25/45，与headline24/45、25/45、25/45不一致；CSV缺error列，不能复原排除规则，54条Codex run_id为空。②72条标line_overlap而非tests，全部gold-test正确率的表述未与数据对齐。③所谓TOST是95%任务bootstrap区间内含判据；Claude范围可探索复算吻合，但Codex selective−always_on约[-17.65,+7.84]pp不在±15内，不能笼统声称各对等效。④功效模拟把baseline+delta裁到1，名义10pp实际平均只约5.33/5.88pp，不能直接引用“检测总体10pp需120任务”。实验日期2026-05—06仍单列。

裁决：原作者“未检出改善”只保留为其报告；公开数据一致性和效应上界进一步降级待澄清。不据此反推上下文必然有用。完整计算表、锚点与限制见独立报告；这是统计工件审计，不是Agent效果复现。

关联[总纲](../graph/overview.md)；[逐段证据与审查](./_review_archive/batch12_backlog_review.md)。效果验证状态不升级。


## 2026-10-14 正文一致性纠正

按既有docs08/总纲裁决及本篇内部证据限制，同步正文中的旧强断言、状态或阅读范围；未重抓来源、未新增效果验证。修改前文本见[_review_archive/2026-10-14-batch13/notes/M-046_context_file_ablation.md](_review_archive/2026-10-14-batch13/notes/M-046_context_file_ablation.md)，仅供历史追溯。
