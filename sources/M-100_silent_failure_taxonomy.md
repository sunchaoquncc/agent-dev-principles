# M-100 生产 LLM agent 运行时的静默失败分类学：点修复→元规则→扫描器

## 元信息

- 来源链接：[arXiv:2606.14589](https://arxiv.org/abs/2606.14589)、[HTML 全文](https://arxiv.org/html/2606.14589v1)
- 原文快照（供复核）：`_snapshots_local/batch16_glm_20261018/silent_failures.html`（SHA-256 619c6bfd…，见同名 .json）、提取文本 `silent_failures.txt`（1053 行全文）
- 发布日期：2026-06-12（v1，正文标注 June 2026 · Draft v0.3）；主张实质更新日期：无（仅 v1，自称草稿）
- 数据/事件观测窗口：事故语料 2026-04-09 至 2026-06-02（正文明确）；系统自 2026-03 初连续生产；规模快照 2026-06-11
- 当前适用状态：候选（单系统纵向案例研究，作者自报；公开工件本次抽核三文件，未全面验证）
- 工件/配置/预算及复现范围：论文 HTML 全文（正文、五类分类、22 事故叙述摘要、交叉发现、防御框架、威胁效度、参考文献）阅读；公开仓库（openclaw-model-bridge 的 22 份 postmortem、治理本体 90 不变式/827 检查/23 元规则、14 扫描器、PyPI openclaw-ontology-engine v0.1.0）初次未核；本次主审固定commit抽核三文件（见末节），未克隆整库；“所有数字可机械追溯”不能接受为全量保证
- 阅读覆盖与媒介限制：原批登记全文文字，Fig 1—5只读图注；主审核决定性章节并核作者15行矩阵计数，未复现原实验
- 版本日期：2026-10-18 抓取 v1
- 利益关系与独立性：Wei Wu，独立研究者（个人邮箱，无机构）；系统作者=研究者=操作者；**Claude 作为 AI 工程协作方共同实现系统、共同撰写 postmortem 与本稿（首页脚注完整披露，并把该安排本身作为 §7 的研究发现）**；运行时模型为 Qwen3 级（与协作方分离）
- 复核触发器：论文修订/会议版本；仓库数字核对；其他系统上的分类学重复；PyPI 包被第三方采用的结果
- 检索日期：2026-10-18（A 类筛选子代理发现，主审读原文）
- 作者/机构：Wei Wu / 独立研究者
- 适用模型：运行时 Qwen3-235B 主+Qwen2.5-VL+商用回退；Claude 为开发协作方——分类学主张面向系统层非模型层
- 证据等级：公开工件的有限描述性核对；事故计数属作者单系统统计，约70%属定性估计，87%属防护强度自评。未独立验证效果；无独立标注者（作者自认无κ）
- 框架落点：harness 治理（观察/审计/告警）；评测（作者的回溯防护评级、破坏验证）；安全（fail-plausible/上下文卫生）；上下文治理（污染链）
- 关联条目：M-032（评测方法论）、M-093（观测工具完整性）、M-070（可靠性机制对应实际后果）、M-033（长运行）、D02/D06/D09/D10

## 一句话结论

单系统约8周22起已发生、经历静默期并完成复盘的事故，为排查错误传播路径提供了具体经验。前15起回溯中，作者评为旧审计可完全覆盖的为0；新防护自评5起“完全”＋8起“一半”，13/15约87%不是实测复发阻断率，0也不是全部风险的总体预防率。三步成熟路径截至截止日无记录复发，但暴露量和随访不齐，不能推出点修复必复发或扫描器根治。适合提取有条件诊断方法，不作为“改哪层”的普适效果答案。

## 要点摘录

（引号内逐字取自 2026-10-18 抓取正文。）

### 系统与语料

- 个人助理 agent 运行时（OpenClaw 桥 WhatsApp/Discord）：~40 定时任务、8 提供商、工具治理代理、知识库记忆面；4,286 单测/121 套件、827 声明式治理检查；单 macOS 主机；一人操作+Claude 协作开发。
- 22 起事故=研究窗内全部"到达生产+有全绿指标下的静默期+完成 postmortem"的事件；元模式（错误信号从未以可行动形式到达人类）≥28 次显现。
- postmortem 协议（第 2 起后固化）：修复前必须先画完整因果链、三层归因（trigger/amplifier/concealer）、分钟级时间线、条件组合分析、喂治理本体。

### 五类机制分类（22 起）

| 类 | 机制 | 起 | 静默期 |
|---|---|---|---|
| A 环境/平台怪癖 | 逻辑对、运行环境隐含行为击败它（bash3.2 ERR trap、BSD awk、无 GNU timeout、4000 字符折叠） | 1(+6) | 小时—周 |
| B 设计假设失配 | 代码自洽于假设、生产违反假设（路径解析三候选全miss；**LLM 输出按行位置解析**） | 4 | 天 |
| C 错误吞咽/稀释 | 错误发生但被吃掉或逐层剥离原因（502 三跳剥离成零信息；67 个检查 exec("") 空转数月） | 5 | 小时—天 |
| D 链式幻觉/捏造（fail-plausible） | LLM 把污染上下文转成自信假输出 | 4 | 小时—天 |
| E 运营遗漏/取证盲区 | 部署步骤未发生或取证工具本身被挡（60 天 EPERM：收集器被沙箱静默拒绝记为"正常"） | 8 | 天—60 天 |

- Class D 四例：D1 夜间综合任务把 HTTP 400 缓存污染编成"Hugging Face platform crisis"行业分析推给用户（"the pipeline laundered an encoding bug into industry analysis"）；D2 系统告警混入聊天历史→模型编造 macOS Full Disk Access 修复指令；D3 回退路径机械输出残句并无条件写 "llm": true（"a hallucination implemented in shell"）；D4 未标注出处的真上下文→捏造社区发行版（"provenance-free enrichment is fabrication fuel"）。
- 保留文件事故：agent 把任务完成笔记写进 HEARTBEAT.md——对模型是草稿名、对运行时是控制文件，13 小时全部回复被剥离成静默；元规则=保留路径必须对 LLM 通用文件工具不可写。

### 三条交叉发现

1. **发现渠道**："roughly 70% of silent failures were ultimately caught by human user-view observation of system output, not by unit tests, health checks, or governance audits"——制度化成每周 30 分钟观察仪式（禁止写码；四维：告警噪声/推送延迟/信息密度/响应质量），"it continued to out-detect the automated stack"；单测对该类 ≈0%（按选择偏构造）。LLM 观察者任务找到了真实回归（含一次捏造和自身两个 bug），但"an LLM judging a system's output for silent failure is itself an LLM component of that system, inheriting every class in this taxonomy"。
2. **审计=回归引擎**：对前15起已发生静默事故的回溯评级——旧审计完全覆盖0/15、部分预警2/15；新防护5起“完全”+8起“一半”=13/15（87%），并非15次重演挡住13次；漏检根因 80% 是"从未设想过的维度"；"audits, like regression test suites, encode the past."
3. **延迟跟机制层不跟复杂度**："the longest-lived failures lived in the seams between components"；对静默失败"time-to-detect dominates time-to-repair by one to two orders of magnitude"。

### 防御成熟路径（本批核心）

- 三步：point fix（"an import-omission bug fixed at one site recurred at eight sites via an automated injector two days later"）→ meta-rule（23 条；diagnostics-to-stderr、key-based parsing、alert-path independence、declared-state convergence、reserved-file unwritability）→ mechanized scanner（14 个，CI+每日审计跑）。"Every meta-rule that reached step 3 has zero recorded recurrences as of the study cutoff; every recurrence in the corpus involves a lesson that had stopped at step 1."
- 破坏验证（"test the test"）："Every new guard must be proven alive by deliberately introducing the violation it targets and observing it fire"——抓到过自引用 grep、67 个空转检查、镜像错误假设的 fixture；"an unvalidated guard is indistinguishable from a vacuous one."
- trigger/amplifier/concealer：只修 trigger 是装饰性的（"Triggers are unbounded…the environment will always produce another malformed byte"）；最高杠杆修复在 amplifier/concealer 层——D1 的整条幻觉链被"one >&2"（一个 stderr 重定向）切断。
- 反捏造分层：作者把提示护栏放在卫生与出处之后；六级累积提示护栏自报53–92%下降，实际代理为多跳因果链及“因此”句等语言模式频次，不等于真实幻觉率或事实错误下降。
- Sunset Law："before adding any mechanism, attempt to retire an equivalent one; one logical entity must have one physical representation"；防御本身是事故面（收敛引擎曾因 observer-mutates-observed 接缝制造三次事故后被迫只读化）；五周内"retired more representation duplicates than it added invariants"且事故频率下降（作者自注混杂警告）。
- AI 协作发现：AI 协作者会"industrializing the trigger-level cosmetic fix"（五连环"修复"替代一次文件拷贝的正解）——协议刚性存在正是为对抗这一点；"AI collaboration shifts the binding constraint of reliability engineering from implementation bandwidth to judgment discipline."

### 威胁效度（作者自列）

单系统单操作者对单 OS 八周——频次/份额/延迟均为案例描述统计非总体估计；70% 发现份额可能反映该操作者异乎寻常的专注；分类无独立标注者（缓解=每类驱动一个真实扫描器）；语料只含"停止静默"的失败，延迟分布右删失；AI 协作方共同撰写本稿，数字声称以公共仓库为核对锚。

## 主张卡

| 主张ID | 归属 | 主张与环境范围 | 原文位置与短锚点 | 局限/缺失信息 | 与既有知识的关系 |
|---|---|---|---|---|---|
| SF-1 | 来源记载 | 前15起已发生静默事故中，旧审计完全覆盖自评0/15；新防护至少“一半”自评13/15 | §5.6 表；`regression engine` | 单系统 15 起回溯审计；作者自评 | 直接支持 D10"评分链条本身也要核对"并给出两种效度的分离 |
| SF-2 | 来源记载 | 走完三步成熟路径的教训零复发（截至研究截止日）；语料中每次复发都涉及停在第一步的教训（逆方向——停在第一步者是否均复发——未测） | §5.5；`zero recorded recurrences`、`every recurrence…stopped at step 1` | 截止日内零复发；非受控实验 | 对可重复且可可靠编码的模式，考虑共享修复/检查；不要求每条经验机械化，不证明提示层无效 |
| SF-3 | 来源记载 | 约70%由人类用户视角发现是作者定性估计；静默期全绿是入样条件 | §5.2 表 | 选择偏构造（单测行近同义反复）；操作者专注度混杂 | 支持 D09"观察实际运行"的不可替代维度；周 30 分钟观察是可操作制度 |
| SF-4 | 来源记载 | fail-plausible：污染上下文→流畅假叙事；防御=系统侧卫生（stderr 纪律/告警剥离/出处标注），提示护栏是最后一层 | §4.4/§6.4；`the last layer` | 53–92%为特定语言模式代理的内部自测，不是总体事实正确率 | 提供错误上下文传播的工程路径；各层单独效果及模型内部机制未验证 |
| SF-5 | 来源记载 | 长静默住在组件接缝；防御堆叠本身制造接缝；Sunset Law 先退役再新增 | §7；`seams` | 五周观察期+混杂自认 | 与 D02"增加组件要说明修复什么"同向并加"退役"维度 |
| SF-6 | 来源记载 | 本例未强约束自由文本按固定stride解析，缺行导致跨条目错位；作者改为按键 | §4.2；`never positional` | — | 按实际格式契约解析并检错；不禁止受约束数组等位置结构 |
| SF-7 | 我方推导 | 该文的分类频次不外推（单系统），但方法（因果链 postmortem+机制目录+破坏验证转化）可迁移 | §Generalizability 作者自述 | 我方与作者判断一致 | 本库"批次红队+裁决"流程的同类结构 |

## 案例区块

- 实践者与约束：单人+AI 协作运维的个人生产系统；真实用户推送（WhatsApp/Discord）；非企业规模
- 具体做法：强制 postmortem 协议；治理本体+扫描器+破坏验证；收敛引擎；周观察仪式
- 报告的效果：频次/延迟为作者自报；87%为回溯防护评级，70%为定性估计；三文件抽核不是运行复现
- 对我们的可复现性：可按具体失败与维护成本选择复盘、破坏验证或共享检查；分类频次不可复用于他系统

## 适用条件与反证

- 适用条件：长运行、有定时自主性、向人类推送产出的 agent 系统；结构性结论（三步路径、审计两效度、接缝论）比频次更可迁移
- 反证/局限：作者自列威胁见上；公开仓库本次仅三文件抽核，不能消除单操作者与AI协作撰文的叙事偏差；单用户/自有数据场景不代表企业部署；防御框架存在不等于效果证明（87%也是自评）。

## 与已有条目的关系

- M-093（METR 观测工具完整性）：同为"观测链路自身是攻击/失败面"，本文给出防御侧成熟路径
- M-070（可靠性机制对应实际后果）：Sunset Law 与"防御是事故面"是其工程化对应
- M-032（评测方法论）：审计=回归引擎补其"评测测什么"的效度分离
- M-033（长运行 harness）：time-to-detect>>time-to-repair 的量化
- D03/D09/D10/D06：获得一份作者事故报告；不排名为最强或最直接证据（见主张卡）

## 后续动作

- [ ] 需要复现的主张：破坏验证与"点修复 vs 元规则复发"可在本库 scripts/ 治理上小规模试点（无需业务系统）
- [ ] 需要补读的：已抽核库存、审计评级及一份Dream复盘；其他21份完整复盘仍未核；PyPI openclaw-ontology-engine 的实际形态
- [ ] 复核触发器：论文修订/录用；其他系统采用分类学的报告；2027-01 前查新据

## 2026-10-18 主审三文件抽核

固定仓库 [27af1f9f](https://github.com/bisdom-cell/openclaw-model-bridge/tree/27af1f9fe1c2b3cfeaf8a49064bea99bc3ac3eb7)，核库存全文、审计评级标准/15行矩阵及选定个案、Dream复盘全文。范围和哈希见 `_snapshots_local/batch16_master_20261018/incident/manifest.json`，裁决见 `_review_archive/batch16_incident_master.md`；未核全部22份或执行任何源代码。

矩阵复算5完全/8一半/2表层，“一半”包括只能挡同触发、漏变体，或仅改善告警。库存明确70%为定性份额，没有分子。Dream给出日志进入stdout→命令替换捕获→cache非空即采信→模型把内部HTTP故障编成行业分析的链条，值得作为排查边界的历史工件；对应4月15日事故已超六个月，不充当新的现行效果证据。作者关于安全训练、幻觉必然、四层任一独立有效的解释未经独立模型实验。

公开仓库提升可追查性，不能自动消除作者兼操作者、AI共同撰写以及框架推广的偏差。当前仓库树不是冻结事故库存；提交日不刷新事件日。方法可迁移仍属候选判断，不以“机制层”标签代替实际修复效力。
