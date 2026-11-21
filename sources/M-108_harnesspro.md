# M-108 HarnessPro：递归 Harness 自进化的性能-成本帕累托优化

## 元信息

- 来源链接：[arXiv:2610.26770v2](https://arxiv.org/abs/2610.26770)
- 原文快照：[_snapshots_local/batch17/harnesspro.pdf](_snapshots_local/batch17/harnesspro.pdf)，哈希见同名.pdf.json；pypdf提取txt（41页，行号以txt计）。
- 发布日期：arXiv v2 2026-10-20；Under review（未经同行评审）；主张实质更新日期：v1→v2 未逐版对比。
- 检索/审查日期：2026-11-21；验证日期：未复现。代码声明"available at this link"（匿名链接，未取）。
- 作者/机构：Zhuoshi Pan、ZhiYuan Feng 等，通讯 H. Vicky Zhao、Jie Tang / 清华、Z.AI、上交、Warwick、Kling AI。
- 适用模型：GPT-5.5×Codex 0.147.0、GLM-5.2×Claude Code 2.1.231（模型冻结，只进化 harness）；下一代模型/agent版本发布触发复核。
- 来源类型与利益关系：预印本，Z.AI（智谱）深度参与（唐杰通讯）——自研生态展示利益；一手不等于独立验证。
- 阅读覆盖与媒介限制：摘要/方法/主结果表2/消融表3/演化动力学/分析5.3全读；附录（prompt模板、价目表、工件示例）未读。
- 渠道路径：B站UP主10-25视频发现（docs/39 A7）；内容全部取自论文原文。

## 一句话

label-free 的递归 harness 自进化：多 agent（轨迹诊断→按性能-成本优先级规划→编辑→LLM生成测试评估）迭代修改整个 runtime 层，输出 lite/medium/heavy 三档帕累托代表——在三基准上同时提性能降成本；最大功臣是用 LLM 生成测试替代 LLM 直接判轨迹（失败召回 41.7%→83.3%）。

## C1 来源记载（正文直述，引文逐字自txt）

**问题设定（L99-157）**：harness = "software runtime layer that manages a foundation model's interactions and execution"，含 prompts、tools/skills、context/memory 机制、hooks、验证规则。既有 RSI 方法"pursue performance gains through more extensive exploration and stronger verification ... often at the cost of higher token consumption"（L34-36）。目标 min(−PR, C) s.t. PR≥PR(h₀)，输出三档操作点。防泄漏：训练/验证/测试三分，测试集只在进化完成后评估。

**Test synthesizer 动机（L610-626）**：RHO 靠 LLM 自偏好选 harness，但 **"LLM judges tend to be overly optimistic when assessing the execution trajectories, often treating flawed implementations as successful"**（L614-616）。改为专用测试合成 agent 从任务描述+初始轨迹生成固定测试，候选 harness 全程用同一批测试比较；"failure recall increasing from 41.7% to 83.3% compared with direct LLM judgments"（L625-626，Fig 2，TB2+SWE-Bench Pro 训练任务池化）。

**过滤与选择（L629-711）**：每 epoch 候选先淘汰——低于初始通过率下限、或被 Pareto 支配；normalized weighted squared-distance 选三档代表；只用验证集指标，测试集不可见。

**主结果（Table 2，GPT-5.5×Codex）**：TB2：heavy 80.8±1.0% / $0.72 vs RHO 76.3% / $1.09（+4.5pp、-33.9%成本）；Vanilla 69.5% / $0.89。SWE-Bench Pro：medium 79.0% / $1.26 vs RHO 80.0% / $2.68（-53.0%成本）；heavy 80.7% / $1.97。ProgramBench：heavy 69.6% / $2.95 vs RHO 68.8% / $3.59。lite 三基准全超 Vanilla 且省 17.7-57.4%。三基准平均 +2.0pp / -26.1%（相对 RHO）。GLM-5.2×Claude Code 同型（TB2 heavy 81.4% vs RHO 78.0%，成本更低）。延迟非目标但多数场景更快（SWE-Bench Pro heavy 412s vs RHO 520s）。

**进化出的 harness 做了什么（L789-803）**：按任务描述选执行 profile（reasoning effort 档位+工具调用预算）；runtime hooks 强制预算——TB2 medium 例：14 次调用后提醒并行调用/避免冗余检查，26 次后专注完成与验证，44 次后阻断；**"The reminders are appended to tool results, preserving the prompt prefix for cache reuse."**（L797）；RTK 类工具输出压缩折叠重复日志；精简指令。

**演化动力学（L804-817）**：TB2 heavy 从 epoch1 74.6%/$0.91 → epoch3 80.8%/$0.72；SWE-Bench Pro medium 前 2 轮性能升成本也升（70.0%/$1.57→77.0%/$1.66），epoch3 才双改善（79.0%/$1.26）——递归多轮优于单轮。

**消融（Table 3）**：去 planner 性能降且成本升（medium SWE 79.0→73.0%）；**去 test synthesizer 三模式两基准掉 3.4-10.0pp（最大组件）**。给 RHO 单加个别策略（dynamic routing / budget hooks）降成本但**可能**降性能（原文"can also degrade"：TB2 上两变体均维持 76.3% 持平，降性能发生在 SWE-Bench Pro）；统一低 reasoning 掉到 62.7%——"all three RHO variants are Pareto-dominated"，收益来自机制协同。

**AI 使用声明（L905-910）**：AI 辅助软件实现与文稿撰写；LLM 是方法本体；结果人工核对。

## C2 作者解释

- 结论（L891-902）："performance and efficiency can improve together, making cost-aware evolution a promising direction for practical recursive self-improvement"。
- 机制归因（L61-68）：进化收益不是靠压缩上下文或盲目加推理——是动态分配（按任务分配 effort 与工具预算）+hooks 从探索导向收敛+输出压缩+指令精简的协同，"curb avoidable overhead while preserving the reasoning and verification needed for task success"。

## C3 我方推导与比较（工作草案）

1. **评测横切的关键一课**：LLM 直接判断轨迹失败召回仅 41.7%（系统性乐观），LLM 生成测试替代直接判断翻倍至 83.3%——**"用 LLM 评测"的形态选择（判轨迹 vs 生成测试）比"是否用 LLM"更重要**。与 M-091（Jev 评分器一致性）同线，为原则层"评测器设计"提供 2026 年强证据；亦与 M-104"按行为审计而非文本审计"结论同构：可执行测试 > 模型主观判断。
2. **harness 治理层 2026 年证据主干**：harness 优化对象从 prompt（GEPA 家族）扩展到整个 runtime 层（指令/工具/skills/hooks/验证规则，L96-97），且可 label-free 递归。Q-001 观测：这是"脚手架功能在增厚"方向的证据——模型吸收旧脚手架的同时，工程界在造更大的外围自动化层；两方向并行不矛盾，登记为观察点。
3. **成本-性能同向改善证据族**：M-105（结构化状态 O(T)）、M-106（Opus 5.5 长程 -78%）、本篇（-26.1% 均）——三方独立来源反对"提性能必加预算"默认假设。候选原则素材（效果主张，须复现纪律）。
4. **缓存前缀保持的行为模式**（提醒附在工具结果后，L797）与 M-103/M-106 的注入层控制同族——跨源第三次出现"prompt 前缀稳定/注入最小化"实践。
5. 预算 hooks 的三段式（提醒→聚焦→阻断）是"运行时行为治理"的具体原语，与 M-106 的 timers/outbox 同为常驻执行编排件。
6. RHO 单加策略被支配（L884-890）：**harness 各机制收益非加性，需整栈协同进化**——反对"挑单个 best practice 拼装"的工程直觉，证据在编码域内。

## C4 限制与反证

- Under review；三基准全部是终端/编码/程序重建域，非编码业务不外推。
- 训练集仅 10 任务（DPP coreset）、G=3 rollouts、3-4 epochs——小规模进化，稳定性未证。
- 成本按固定价目表折算（附录A未核），价格波动与缓存命中策略影响可比性。
- RHO 为其团队前作（Pan et al. 2026a），自家对比自家基线；第三方未复现。
- "label-free" 指进化过程，最终评估仍用官方测试（标准但需说明）。
- [我方推导] failure recall 41.7%→83.3% 的对照是"直接 LLM 判断"这一较弱基线；与人工标注测试的差距未报。

## C5 下次复核触发

- 论文被会议接收或撤稿；代码公开仓库可复核时。
- RHO/HarnessX/AHE 同线工作（L918-923 已列线索）进入精读后回看比较结论。
- Codex/Claude Code 大版本更新（进化出的 hooks 机制可能被产品内置）。

## C6 来源去向

- 纳入知识库（A7精读）；harness 治理线 2026 证据主干；评测横切（评测器形态）新证据；与 M-105/M-106 组"成本-性能同向"证据族。

## C7 勘误与核对记录

- 2026-11-21：UP主称"智谱唐杰-清华爆火论文…提分又省钱"，作者机构与结论方向核对一致（Z.AI+清华、唐杰通讯作者在列）；"帕累托优化引导递归自进化"与论文机制一致。UP主视频详细数字未对照（字幕稿未校验）。
- 2026-11-21 红队勘误：RHO 单加策略"降性能"补原文限定（can also degrade；TB2 持平、SWE-Bench Pro 降）。
