# M-097 渐进披露受控研究：收益随配置变化，路由深度与常驻描述尚未隔离

## 元信息

- 来源链接：[arXiv:2607.17598](https://arxiv.org/abs/2607.17598)、[HTML 全文](https://arxiv.org/html/2607.17598v1)
- 原文快照（供复核）：`_snapshots_local/batch16_glm_20261018/progdisc.html`（HTML SHA-256 见同名 .json，328,912B）、提取文本 `progdisc.txt`（729 行）；摘要页 `progdisc_abs.html/.txt`
- 发布日期：2026-07-20（v1 提交时间戳 Mon, 20 Jul 2026 06:35:32 UTC）；主张实质更新日期：无（仅 v1）
- 数据/事件观测窗口：实验运行日期未在正文给出（v1 前完成）
- 当前适用状态：候选（预印本、作者自报、未独立复现）
- 工件/配置/预算及复现范围：论文 HTML 全文（正文、表格数字、附录结构、局限性、参考文献标题）阅读；图 4/9 的 Pareto 前沿只读文字描述未核像素；未下载 TeX 源/PDF、未运行 LoongDoc、未查开源代码链接（正文未见代码仓库声明，Ethics 声明不随包发布 skill packs）
- 阅读覆盖与媒介限制：全文文字；Table 1/Table 2 数字直接从提取文本读取（含 LaTeX 残留标记）；未复算任何统计
- 版本日期：2026-10-18 抓取 v1
- 利益关系与独立性：作者 Yifeng He、Yinzhe Zhao、Jicheng Wang、Hao Chen（页面未列机构；致谢 UC Noyce Initiative）；预印本未经同行评审；无明示厂商利益，机构背景未核
- 复核触发器：论文被会议录用或修订；LoongDoc/代码开源后核对数字；其他 harness/模型上的复现或反例；最迟 2027-01 前查新据
- 检索日期：2026-10-18（B 类筛选子代理发现，主审复核原文）
- 作者/机构：如上（机构未核）
- 适用模型：gpt-5.4-mini（Codex/Pi harness）、qwen3.6-27b（Pi）、claude-haiku-4.5（Claude-Code harness）——非当期旗舰，换代需重测
- 证据等级：可检验结论（方法与数字公开可对）+ 经验断言（结论外推）；未独立复现
- 框架落点：上下文治理（渐进披露/检索取舍）；评测（InfiniteBench 改造）
- 关联条目：M-002（hybrid 检索/compaction）、M-068（Skills 按需加载）、M-053（长文档审阅）、D04/D11

## 一句话结论

在所测叙事 QA 配置中，单书 Codex 的三种表示按作者一个标准差的判据未清晰分离，不能称“零收益”；hierarchical 相对 flat 未显示超出该噪声判据的优势，但部分均值更高，Pi 部分格明显退化。库规模下 flat 的若干分数改善，弱导航 open-QA 格 hierarchical 也可反超。flat/hierarchical 同时改变深度和子描述常驻位置，未隔离深度因果；harness 差异也不是仅导航能力的消融。摘要“never helps”与附录保留为源内冲突，不转写成通用单层默认。

## 要点摘录

（引号内逐字取自 2026-10-18 抓取的 HTML 提取文本；LaTeX 残留符号按原文保留。）

### 设计

- 三种阅读配置；仅 flat/hierarchical 共享同一 chunk 集，raw 为整书："Both packs share a single chunk set (Section 3.1), so the disclosure wiring is the only variable"——raw（原文+自由导航）、flat（单一 SKILL.md 索引、按需读 chunk）、hierarchical（每 chunk 一个子 skill、描述常驻+meta-router）。
- 环境：把 ∞Bench（论文写法 \inftyBench，学界通称 InfiniteBench）改造成 LoongDoc（BenchFlow + Agent Client Protocol，沙箱文件系统+确定性 verifier+完整轨迹记录）；Table 1实际四组合：Codex/gpt-5.4-mini、Pi/gpt-5.4-mini、Pi/qwen3.6-27b、Claude-Code/claude-haiku-4.5，并非三乘三全组合；hybrid-rag（检索-重排）作外部参照。
- 库规模：K∈{5,10,20} 本书，每题仍只涉及一本书，测"先找书再作答"。

### 单书结果（Table 1，3 seeds 均值±标准差）

- flat vs raw：Pi 与 Claude-Code 上 flat 每格匹配或超过 raw（唯一例外 qwen3.6-27b Zh.QA 在一个标准差内）；Claude-Code haiku-4.5 En.MC 0.7448→0.8667。
- **Codex 反转**："on gpt-5.4-mini the three approaches tie within error on all three subsets"；轨迹检查解释：裸 Codex "does not read the book linearly but builds its own retrieval, grepping the raw text for the entities named in each question"——"disclosure is redundant when the agent already navigates well natively; for such agents a pre-cut skill buys controllability of the retrieval path, not accuracy"。
- hybrid-rag 参照："Routing to a chunk through an in-skill index thus outscores the classical rerank-and-feed pipeline in nearly every cell"（qwen3.6-27b 上落后 raw+flat 于全部三子集）。
- **特定层级实现的退化（作者解释，非深度单因素）**："No cell rewards the extra depth: hierarchical ties flat within noise on claude-haiku-4.5 and on Codex gpt-5.4-mini, and trails it everywhere else. On Pi it is actively harmful, collapsing En.MC from 0.9126 under flat to 0.6398 on gpt-5.4-mini"（Zh.QA 0.7479→0.3890）；机制解释："the always-loaded child descriptions saturate the router's context before it commits to a chunk"。

### 库规模结果（Table 2，均值±标准误，跨 bundle 与 seed）

- raw 崩溃：Codex En.QA 从 K=5 的 0.657 跌到 K=20 的 0.257；Zh.QA 0.698→0.043（"collapses to near zero"）。
- flat 救回：K=20 En.QA flat 0.462 vs raw 0.257；"it beats the bare agent in all six En.QA cells across two harnesses and two models, the most robust effect in the table"。
- K=20 En.QA，Codex的flat/hierarchical为.462/.267，约1.73倍；Claude-Code为.354/.302，约1.17倍，不能把原文“well over 1.7×”套到两组。作者以常驻子描述增加上下文压力解释退化，未隔离该因素；按任务分数记录，不统称二元准确率。
- **但弱导航 harness 的 open-QA 格两层恢复**（附录 C.1/Table 3，Pi/gpt-5.4-mini）：En.QA K=10 hierarchical 0.310 为三法最优（flat 0.221）；Zh.QA K=20 hierarchical 0.330 持最佳格。C.1 原文："Where the corpus is large and the questions are open, the extra routing level that hurts En.MC recovers, so depth is a scale- and task-specific effect rather than a uniform cost."——正文 §5.1 takeaway 亦限定"only at library scale, on weak-navigator open-QA cells, does the extra level recover"。摘要/结论的"never helps / one level is enough"全称句与附录矛盾，保留冲突。
- 效率："a larger corpus is strictly less efficient, not merely harder"——精度下降且达到任一固定精度的成本上升。
- 语言差异：Zh.QA 收益缺失或为负，"the base model, not the skill pack, sets the ceiling"。

### 作者自述局限

- En.MC 预训练混淆（经典小说可被参数记忆作答："even at K=20 the raw agent answers En.MC correctly in a handful of tool calls, far too few to have read twenty books"）。
- 规模轴只有 K∈{1,5,10,20}、单一 benchmark 家族、叙事语料；"we cannot say whether the effect transfers to non-narrative corpora such as code or technical manuals"。
- chunking/description 配方固定单一；样本量受 ∞Bench 限制，多处比较在一个标准误内。

## 主张卡

| 主张ID | 归属 | 主张与环境范围 | 原文位置与短锚点 | 局限/缺失信息 | 与既有知识的关系 |
|---|---|---|---|---|---|
| PD-1 | 来源记载 | 所测单书配置的收益随 harness/模型组合变化；Codex 未显示清晰分离，不等于零效应 | §5.1 "The gain is harness-dependent"；Codex 轨迹 grep 证据 | 3 seeds；未测更多 harness；运行日期未给 | 细化 M-068（按需加载非普遍收益）与 D04（表示取舍先看消费方能力） |
| PD-2 | 来源记载 | **单书下**hierarchical 未显示超过作者噪声标准的优势，Pi 部分格明显退化；深度与常驻描述同时变化；库规模弱导航 open-QA 格可恢复（附录 C.1，与摘要全称句矛盾） | §5.1 "Depth does not pay, and can hurt"（单书）；C.1 "scale- and task-specific effect"；0.9126→0.6398 | Pi 上最烈，机制为上下文压力解释 | 支持 D04"不要无界追加/常驻预算"约束的具体化；深度取舍按规模×任务×harness 条件化 |
| PD-3 | 来源记载 | 库规模下 flat 披露成为候选（六格 En.QA 均值均高于 raw，并非均显著） | §5.2 "the most robust effect in the table" | K 只到 20；叙事语料 | 补 D04"超限处理"与 M-053 长文档分工的实证边界 |
| PD-4 | 来源记载 | 所测多数格的索引路由分数高于该固定 hybrid-rag 基线 | §5.1 hybrid-rag 段 | 固定 BM25+BGE-M3+RRF+reranker；agent 可继续读原文而基线只看检索证据，权限不同 | 限制"上 RAG"默认；与 M-002 hybrid 检索建议需并读 |
| PD-5 | 我方推导 | 选择披露方案时应比较目标 harness、语料规模和常驻负担；本文提供候选，不给通用深度最优解 | 全文与附录 | 未隔离导航能力、深度和描述位置；无本库任务实验 | D02/D04 保持，不新增默认架构 |

## 案例区块

- 实践者与约束：长文档/多书语料的 agent 阅读路径选型（非业务部署；学术受控）
- 具体做法：raw 为整书，flat/hierarchical 共用 chunk；后两者同时改变路由深度与子描述常驻位置。三 harness 三模型，作者记录轨迹
- 报告的效果：如上 Table 1/2 数字（作者自报，未复算）
- 对我们的可复现性：LoongDoc 基于 BenchFlow+ACP 可搭建；hybrid-rag 与 skill pack 生成管线论文附录 A 给了提示词；未实际运行，成本未估

## 适用条件与反证

- 适用条件： InfiniteBench 叙事语料；上述四个harness/模型组合，具体运行日期未给；flat 是可比较的候选，不升为通用默认；论文的任务分数不能直接外推本库或业务效果
- 反证/局限：作者自列五条局限（见上）；[我方审查] chunk描述质量可能影响结果，但未隔离其因果贡献，论文固定一个生成配方未做敏感性；机构与代码可得性未核，“first controlled study”为作者自称；多数单书格未超作者噪声标准，不能等同无效。

## 与已有条目的关系

- M-068（Skills 按需加载）：本篇研究文档导航，不验证工具绑定；其所有子描述常驻实现不等于本库按需多层目录，不能据此要求全库扁平化
- M-053（Harvey 长文档审阅）：分工/覆盖问题在叙事 QA 的受控版本
- M-046（上下文文件消融阴性）：同为“预组织上下文未必提升”家族，本篇提供若干配置/规模下的观察，不证明“弱导航+大语料”是提升的充分条件
- M-002：hybrid 检索建议需叠加"agent 可自建检索时结构预建非必要"的条件

## 后续动作

- [ ] 需要复现的主张：在本地小语料（如本库 notes/）复刻 flat vs raw 对照，成本可控
- [ ] 需要补读的：SkillsBench（Li et al. 2026）与 Zhang et al. 2026 的 13.8 万 SKILL.md 元数据审计（论文引用的相邻测量）；LoongDoc 代码可得性
- [ ] 复核触发器：论文录用/修订；新 harness 或当期模型上的重复实验；2027-01 前查新据
