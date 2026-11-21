# M-115 WikiSkill：把 Agent 经验编译为持久知识以进化技能

## 元信息

- 来源链接：[arXiv:2608.27454](https://arxiv.org/abs/2608.27454)
- 原文快照：[_snapshots_local/batch17/wikiskill.pdf](_snapshots_local/batch17/wikiskill.pdf)，哈希见同名.pdf.json；pypdf提取txt（28页，行号以txt计）。
- 发布日期：2026-08-28；主张实质更新日期：未知。
- 检索/审查日期：2026-11-21；验证日期：未复现。
- 作者/机构：Liyan Tang、Cyrus Rashtchian 等 / Google Research、Virginia Tech。
- 适用模型：Qwen3.5-4B/9B、Qwen3.6-27B、Gemini 3.5 Flash 等（图1）；下一代模型发布触发复核。
- 来源类型与利益关系：预印本；Google 学术。
- 阅读覆盖与媒介限制：摘要+结构段+关键结果定位段精读（L67-92、L149-211）；实验全表未逐项核——**摘要级+定位段精读**。
- 渠道路径：B站UP主09-03视频发现（docs/39 A13）；内容取自论文原文。

## 一句话

把技能进化与持久 wiki 知识库共演化：分离原始执行轨迹/Wiki层/Skill层三层，经验持续固化进 wiki 供后续技能更新复用——跨基准超 SOTA 技能进化方法，且**更大模型从进化技能中受益更多**（Qwen 4B/9B/27B 提升 12.3%/17.5%/23.9% 递增）、技能跨模型迁移有效（他模型进化的技能可超自进化）。

## C1 来源记载（摘要+定位段直述）

- 动机："the insights that guide skill development typically remain scattered across optimization histories, limiting their systematic reuse across iterations"——技能开发的洞见散落在优化历史里。
- 三层结构：执行轨迹 / Wiki Layer（"compiles raw traces into structured, compounding knowledge"）/ Skill Layer（可执行技能）；带 Rollback 机制——"retains updates that improve validation performance"（L67-71）。
- 规模互补发现（摘要）："skill evolution complements model scaling: larger models generally benefit more from evolved skills, while smaller models with skills can outperform substantially larger models without them"；Qwen 家族内平均提升 4B 12.3%、9B 17.5%、27B 23.9%（L84）。
- 迁移发现（摘要）："evolved skills transfer effectively across models and model families, and skills evolved by other models can outperform self-evolved skills"。
- 消融：持久知识积累（wiki）对技能进化关键（摘要倒数第二句）。

## C3 我方推导与比较（工作草案）

1. **与 M-103 的 wiki 层同构**：Anthropic 的记忆表示（dreaming 建 wiki 页）与本文 Wiki Layer 都是"经验→结构化知识→复用"，且都发现 wiki 需要维护成本（M-103 反例：膨胀超原文）；本篇加了"技能层可执行"的闭环。三方（M-103 跨会话记忆 / 本篇技能进化 / M-049 Letta）在"wiki 作为中间表示"上收敛。
2. **"更大模型受益更多"与"更强模型更易感"并列**：M-104/M-107 记录能力放大失败面，本篇记录能力放大脚手架收益——**能力是放大器，方向由机制决定**。这对 Q-001 是精确化的观察框架：不必预测吸收量，看具体机制被放大的是收益还是失败。
3. "他模型进化的技能可超自进化"——技能工件质量与模型自洽性解耦，支持 skills 作为可交易中间件的产品含义（未展开）。

## C4 限制

- 摘要级阅读；"超 SOTA 方法"为自报，基线（EvoSkill/SkillOpt）版本未核。
- wiki 维护成本与膨胀风险未在本篇所读段落量化（对照 M-103 反例存疑）。

## C5 下次复核触发

- 与 M-065（skills from feedback）、A17 SkillHone 的技能线合审时回看。

## C6 来源去向

- 纳入知识库（A13，摘要级+定位段）；skill 进化线证据。

## C7 勘误与核对记录

- 2026-11-21：UP主"Wiki层保存经验，显著提升Skill效果"与摘要一致。
