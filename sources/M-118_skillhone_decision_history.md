# M-118 SkillHone：以持久决策历史支撑技能持续进化

## 元信息

- 来源链接：[arXiv:2606.08671](https://arxiv.org/abs/2606.08671)（EMNLP 2026 Industry Track，web检索确认；代码 github.com/Tencent/SkillHone，未取）
- 原文快照：[_snapshots_local/batch17/skillhone.pdf](_snapshots_local/batch17/skillhone.pdf)，哈希见同名.pdf.json；pypdf提取txt（11页，行号以txt计）。
- 发布日期：arXiv 2606（2026-06，约5个月前，窗口内）。
- 检索/审查日期：2026-11-21；验证日期：未复现。
- 作者/机构：Zhiwei Li、Yong Hu / 微信·腾讯（Industry Track 两作者论文）。
- 适用模型：deep-research 基准与内部场景（底座构成未在摘要级内核）；下一代模型发布触发复核。
- 来源类型与利益关系：预印本（Industry）；企业工程展示动机，内部场景数据不可外部验证。
- 阅读覆盖与媒介限制：摘要+引言开头精读——**摘要级精读**。
- 渠道路径：B站UP主11-17视频发现（docs/39 A17，简介未挂链接，本轮经web检索定位）。

## 一句话

技能进化不能只留最终工件——丢弃决策历史会让后来的 agent 无法解读先前修订/评估/被拒方案（need to interpret），并重复旧优化（图1"repeat a prior optimization and make future improvement harder"）；SkillHone 把每次技能修订与评估侧证据配对，持久记录诊断/修订/证据/被拒方案的结构化历史，让跨会话优化不必重新发现过去的 rationale：GAIA +15.8、内部七场景平均 +18.8。

## C1 来源记载（摘要直述，skillhone.txt L7-23；图1语境 L51-53）

- 问题："Existing methods improve skills in bounded runs and retain only the final artifact, discarding the decision history that later agents need to interpret prior revisions, evaluations, and rejected alternatives."
- 机制：修订与评估侧证据（practice feedback）配对；结构化历史四元组（diagnoses, revisions, evidence, outcomes）；角色分离子代理在练习探针上跑候选技能，"with redacted reporting"（脱敏报告），依据既往决策提修订——"enabling cross-session refinement without rediscovering past rationale"。
- 结果：无预集成搜索栈的设置下超商业 deep-research agent：GAIA +15.8、WebWalkerQA-EN +3.2；超先前技能进化方法；内部工具分析七场景平均 +18.8。

## C3 我方推导与比较（工作草案）

1. **决策历史=provenance 在技能层的实例**：与 M-110"provenance 是记忆可修正性前提"、Kwon 2026"source-first 写入"三方收敛——**保留"为什么"（依据/取舍/被拒方案）而非只留"是什么"（最终工件）**是跨会话知识系统可持续改进的共同前提。此主题本批第三次出现，登记为候选原则素材（工程实践类）。
2. 与 M-065（skills from feedback）衔接：M-065 讲从反馈生成技能；本篇讲技能的**世代传承**问题（接手者需要理解决策脉络）——技能生命周期两端的互补证据。
3. "重复旧优化"失败模式（图1）与 M-104 memory trap 同族结构：历史信息丢失（本篇）或历史信息过泛（M-104）都会导致后续行为劣化——**历史保留的粒度是双向风险的设计变量**（太少重复劳动、太多过度泛化）。
4. 脱敏报告（redacted reporting）是角色分离+信息控制的实践细节，与 M-110 信任层级/隔离思想呼应。

## C4 限制

- 摘要级；Industry 论文，内部场景（+18.8）不可外部验证；两作者企业自报；GAIA 基线（"commercially backed deep-research agent"）具体所指未核。

## C5 下次复核触发

- 代码开源后第三方评测；与 M-065/M-115 技能线合审。

## C6 来源去向

- 纳入知识库（A17，摘要级）；skill 进化线+决策历史/provenance 主题证据。

## C7 勘误与核对记录

- 2026-11-21：UP主"记录修改依据，让接手优化的Agent理解过去的取舍"与论文命题一致。
