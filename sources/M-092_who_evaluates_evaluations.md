# M-092 Who evaluates the evaluations：surprisal 难度扫描与真值审计

## 元信息

- 来源链接：[Who evaluates the evaluations?](https://cloud.google.com/blog/products/data-analytics/evaluate-agent-performance)
- 原文快照（供复核）：`_snapshots_local/batch15/google_who_evals.md/.html/.txt`（HTML SHA-256 4858f294…）
- 发布日期：原10-14本地正文快照为2026-07-11；10-16官方在线正文/新快照显示07-10，两版差异保留，原因未核，不把其中一版称唯一确证日期
- 主张实质更新日期：未知
- 数据/事件观测窗口：F1 曲线为某 recall-oriented Discovery Agent（"on Gemini 3.1 Pro"）；具体运行日期未给
- 当前适用状态：有条件方法参照（元基准思路+真值审计清单）；数字为厂商自报
- 工件/配置/预算及复现范围：博客全文阅读；Discovery Bench/iSQR 代码与数据**未随文公开**（正文无链接），无法复算任何数字
- 阅读覆盖与媒介限制：正文全文+脚注引用8条；图（iSQR 环、F1 曲线）只读文字描述未核像素
- 版本日期：2026-10-14 抓取版本
- 利益关系与独立性：Google Data Cloud Frontier AI 团队厂商博客（Gemini 自家 agent、BigQuery 生态叙事）；引用的第三方文献（MMLU-Redux 等）为公开研究
- 复核触发器：Discovery Bench/iSQR 工件公开；KramaBench 修复或新版本；第三方采用或反驳；最迟 2027-01-11 查新据
- 检索日期：2026-10-14
- 作者/机构：Manav Garg、Sunil Pedapudi / Google
- 适用模型：被测 agent=Gemini 3.1 Pro（正文）；方法域=数据发现/检索任务
- 证据等级：经验断言（厂商自报实验；无公开工件）
- 框架落点：评测（真值质量/难度校准）；prompt 治理（查询表述与答案空间的关系）
- 关联条目：M-032（评测方法论）、M-083（评分器校准）、M-076（专家数据可信度）、M-082（错误发现）；E-02 后续设计；D10

## 一句话结论

把"难度"从主观标签变成可测量的量（surprisal/信息量）并沿歧义轴扫描，暴露了静态 pass/fail 基准结构性看不见的两样东西——能力悬崖（同一查询去掉一个区分性术语 F1 从 1.00 掉到 0.00）与真值本身的损坏；但该方法与数字全部无公开工件，且增删术语可能改变解释与候选答案空间，是否仍是等价任务需另外核对。

## 要点摘录

（引号内逐字取自 2026-10-14 抓取正文。）

### 方法：难度作为被工程化的量

- 核心主张："Difficulty stops being a property that is attributed by sentiment or classification, and becomes one we engineer."
- iSQR（iterative surprisal-based query refinement）：按术语信息量增删，生成 high/medium/low 三档校准歧义变体，"each grounded in bits (not subjective opinion)"、"We can even justify, term by term, why a word was added or removed."
- TLE 实例：查询含 "TLE" 时几乎唯一指向 TLE_____48445 表；去掉后"whose vague phrasing now matches density tables, precise-orbit files, and decay logs alike"

### 发现一：cliff（静态基准的结构盲区）

- "This query scores a perfect F1 = 1.00 at neutral phrasing — and 0.00 at high ambiguity."
- "A static benchmark tests the neutral phrasing, stamps 'solved,' and reports flat ground where there is a precipice. Pass/fail was particularly misleading in that it did not just miss the cliff, but it told us the terrain was level."
- F1 曲线（Gemini 3.1 Pro recall agent，KramaBench）：high 0.34 / neutral 0.76 / medium 0.81 / low 0.78

### 发现二：sweet spot（特异性非单调）

- "medium ambiguity beat neutral, and low ambiguity sometimes underperformed it. More specificity is not monotonically better"
- 具体失败模式定位：time-sharded tables（"precision collapsing to ~8% as the agent over-retrieves 21 near-identical shards for a two-table answer"）、context blow-up（"F1 dropping from 0.75 to 0.32 once a query triggers long search chains"）

### 发现三：真值损坏审计

- kramabench-astronomy 衍生基准实际核查结果："ground-truth tables that did not answer their query, a question whose 124 sharded tables exceeded what some teams' retrieval APIs could even return, months specified where exact dates were required."
- "an evaluation is itself an artifact that can be defective, and almost nobody evaluates it. We instrument the agent and trust the ruler"

### 发现四：生成器递归评测

- "we built the same ambiguity sweep two ways: steering terms from a pure-LLM guess, versus terms grounded in TF-IDF surprisal. The two disagreed violently. At high ambiguity, the LLM-built sweep scored the agent at F1 ≈ 0.34; the grounded sweep, ≈ 0.85."
- [我方推导] 这是 M-082/M-083 线索的具体化：评测生成器自身也有系统性偏差，且两种构造法可给出相反结论。

### 作者自认的张力

- "Difficulty-as-entropy is only as reliable as the model that estimates the entropy. There's a risk that if we push too hard on a measurable proxy, we optimize the ruler instead of the agent."
- 饱和问题："as agents clear coarse benchmarks, the score saturates near the top and the exam loses its ability to highlight where the agent can be improved."

## 口径审查（本批执行）

- **难度调制与答案空间**：iSQR 增删术语后是**不同的查询**，其可能解释和候选答案集合可能改变，原文未给足以证明语义等价的规则（TLE 例：去掉 TLE 后多表匹配）。[我方推导] 因此"high ambiguity 变体 F1=0"测的是"接近真实用户不完美表述时的鲁棒性"，不能自动视为仅改变难度而语义不变；把它当"同一任务的难度"需要在报告里显式定义变体构造规则。正文以 surprisal（"剩余不确定性"）定义难度，逻辑自洽，但未讨论"更模糊的查询对人类标注者是否也更难/更不可判"
- **真值与生成器偏差**：正文已含双向（人工标注难复现、LLM 生成器与 grounded 生成器剧烈分歧），是同主题材料中自审较充分的一篇
- **代码公开范围**：无任何代码/数据链接；F1 数字、124 分片、~8% precision、0.75→0.32 均不可复算——全部按厂商自报处理
- **跨域限制**：方法域是数据发现（检索/F1），不能直接当开放长文评分方法使用（brief 提醒落实：检索任务的"答案空间"在长文任务中无对应物，长文的"更模糊"变体如何构造未定义）
- 引用谱系健康（tinyBenchmarks/metabench/PSN-IRT/MMLU-Redux 6.49% 错标/Platinum/AmbigQA），均公开研究，可作后续线索

## 案例区块

- 实践者与约束：Google Data Cloud 团队评测数据发现 agent（warehouse/lake 中找数据集）
- 具体做法：iSQR 三档歧义变体+逐术语信息量依据；衍生基准逐条人工（Gemini 辅助）核查真值
- 报告的效果：cliff/sweet spot/真值损坏/生成器分歧四项发现（作者自述，无工件）
- 对我们的可复现性：思路可迁移——①E-02 后续可做"删区分性术语"的梯度版本（本地小规模、无付费 API）；②对自有评测集做一次"真值逐条核读"清单（M-082 已有类似）；surprisal 具体计算需语料统计，未公开前不照抄其实现

## 适用条件与反证

- 适用条件：检索型任务（答案空间可枚举）、有真实语料统计 surprisal 的环境；企业数据场景（Google 生态）
- 反证/局限：
  - 作者自认：熵估计依赖模型、优化尺子风险、饱和
  - 我方限制：零公开工件；单 agent 单基准数字；"sweet spot"可能是该 agent 实现特异性（正文承认"idiosyncratic"）而非普遍规律；F1 曲线四点无置信区间/重复次数
  - 未核：KramaBench 原文与其 astronomy 衍生损坏范围（Google 单方叙述）；引用文献均未读原文

## 与已有条目的关系

- M-032/M-082/M-083：同线加强——"先审尺子再审学生"从主张推进到具体方法（surprisal 扫描+真值逐条核读+生成器对照）
- M-076（专家数据可信度）：真值损坏是同类证据（基准数据生产端缺陷）
- E-02 后续设计：cliff 扫描思路（梯度变体而非单点）直接可用；避免饱和的路径
- D10：真值逐条核读与"难度=可测量量"可作为评测细则的条件性补充（待证据累积，本篇单独不升级）

## 后续动作

- [ ] 需要复现的主张：删区分性术语的 cliff 效应可在本地小语料上复现（检索型任务，无付费 API）——列入 E-02 后续设计候选，不在本批执行
- [ ] 需要补读的反方/正方：KramaBench 原文（含 astronomy 子集）；MMLU-Redux/Platinum（真值损坏量化先例）；Discovery Bench 工件若公开
- [ ] 复核触发器：工件公开、KramaBench 修复、第三方采用/反驳；2027-01-11 前查新据

## 2026-10-16 主审限定

两种变体生成器给出不同分数，只能确认测量不一致，不能仅因有TF-IDF依据就证明某一方是真值。作者自报是来源证据的一种，不是无工件就完全不算证据；保持经验断言，不称已验证。引用文献原文未补读。
