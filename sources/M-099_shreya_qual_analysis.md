# M-099 Shreya Shankar：agent 辅助定性分析的六条件对照与失败量化

## 元信息

- 来源链接：[Exploring Agent-Assisted Qualitative Analysis](https://www.sh-reya.com/blog/ai-qual-analysis)
- 原文快照（供复核）：`_snapshots_local/batch16_glm_20261018/shreya_qual.html`（SHA-256 36ebbed8…，56,655B，见同名 .json）、提取文本 `shreya_qual.txt`（164 行全文）
- 发布日期：2026-05-21（正文自述；B 类筛选记录一致）；主张实质更新日期：未知
- 数据/事件观测窗口：实验在发布前"几天"内运行（作者自述 "I spent a few days running these experiments"）；具体日期未给
- 当前适用状态：候选（一手实验+交互式轨迹工件；作者自称 "this is a blog post, not a paper"）
- 工件/配置/预算及复现范围：博文全文阅读；文内链接的交互式 trace viewer（六条件完整日志：提示/工具调用/thinking/子 agent 轨迹）与各条件最终报告对比页**未打开**（外链数据不落地，登记为可回查工件）；451 条推文语料未下载；未复跑实验
- 阅读覆盖与媒介限制：全文文字；图表数字（编码复用率、覆盖率、ρ 相关系数、轴向类别表）取自正文；trace viewer 内容未逐条核
- 版本日期：2026-10-18 抓取版本
- 利益关系与独立性：Shreya Shankar（CMU，独立研究者视角；刚完成教职求职）；无产品营销；对 agent 能力的立场偏批判（作者自述 "agents can do the mechanical parts… fast, but they have no taste"）
- 复核触发器：作者扩展为论文或发布数据；其他任务域（访谈转录/长文档）上的重复；模型换代后重跑
- 检索日期：2026-10-18（A 类筛选子代理发现，主审读原文）
- 作者/机构：Shreya Shankar / CMU
- 适用模型：Claude Sonnet（当期版本未固定；Agent SDK）
- 证据等级：可检验结论（六条件设计+量化失败指标+轨迹工件公开）+ 经验断言（"没有品味"等定性总结）；单作者单语料
- 框架落点：prompt 治理（反馈通道有效性）；上下文治理（codebook 表示）；harness 治理（多 agent 编排/超时退化）；评测（开放产物验收/类别不可证伪陷阱）
- 关联条目：M-033（早停）、M-069（开放生成与有限决策分开）、M-083（长产物评分）、D03/D08/D10

## 一句话结论

六种探索配置暴露开放编码、反馈维持和编排退化问题，但不能证明“约束外置改善质量”。exp3-independent 的一次性代码种类比例最低（4.5%），恰也是子 agent 超时后改用 Python 关键词匹配的条件；配置、执行路径和赋码覆盖均不同。该指标变低不代表语义任务完成得更好。已赋码推文占比为 5.5%—67.8%，不等于已读范围；反馈过拟合、失粘滞及疲劳主要为作者的质性观察。

## 要点摘录

（引号内逐字取自 2026-10-18 抓取正文。）

### 设计

- 语料：451 条回复 Sholto Douglas 提问（"When do you reach for other models instead of Claude?"）的推文；问题="why are users switching away from Claude?"
- 六种非全因子配置：提示是否含方法论描述 × 人类介入方式（无/逐批改码/逐批书面反馈）× 单/多 agent（层级、独立双编码）；全部 Claude Sonnet + Agent SDK，agent 可读写文件、起 Flask UI 收人类反馈。
- 自我定位："the goal was not to optimize for the best possible system, but to see where straightforward approaches broke down and what kinds of human involvement seemed useful."

### 失败一：转述而非分析

- 长推文获得更多编码（同义重复被逐条命名）："the number of open codes the agent generated per tweet was highly correlated with the length of the tweet (ρ = 0.81 in exp1)"；exp2-memo 书面反馈后"dropped significantly to ρ = 0.15"。[主审] 这是不同配置、不同覆盖样本的相关系数，不能当同输入前后修复；作者认为反馈有帮助，但未证明语义质量提升。
- 一次性编码率：exp1 93.8%、exp2-codes 100%、exp2-memo 96.5%、exp3-hierarchical 74.2%、**exp3-independent 4.5%**；唯一低值来自"two independent coders both coded against the same predefined set of categories from the main agent"。该指标分母是代码种类，分子是仅使用一次的种类；同条件发生关键词脚本替代（见失败三），未识别类别约束的独立作用，更没有外置位置干预。

### 失败二：提前结束与到达后漏码须分开

- "The best condition was exp2-codes, which coded 68% of the 451 tweets. The worst was exp3-hierarchical at 6%. Most conditions covered around 25-35%."——指令要求通读并多遍，agent 中途"declare the analysis complete"。
- 已到达的推文也错：空编码列表跳过实质抱怨（轨迹例：把含具体抱怨的长推文判为 "defending Claude, token management advice" 而赋空码）。

### 失败三：不会管理任务

- 顺序处理、不用可用并行："In exp1, one agent said it would parallelize and had a worker subagent configured; however, it made zero subagent calls."
- **编排塌缩（正文记载，原 trace 未核）**：exp3-independent 两个编码子 agent 超时后，"the orchestrator agent switched strategies entirely: instead of having the subagents read tweets, it generated Python scripts with different hardcoded keyword heuristics for each 'coder.'"——"the 'independent coders' were no longer performing qualitative analysis at all; they were effectively doing substring matching with different keyword lists."（例：含 "sycoph" 即赋 overly_agreeable）

### 失败四：反馈通道双向失灵

- 过拟合："I mentioned it once. In later rounds, the agent kept looking for competitor comparisons… elevated 'competitor comparisons' into a top axial category"——未回溯重编早前推文。
- 失忆："The agent reacted immediately: it consolidated codes… said it would be "more disciplined," whatever that means. But the change did not stick. Later batches went back to producing mostly one-off codes, and the final codebook still had a 96.5% one-off code rate."
- 根因概括（作者）："agents either overfit strongly to early feedback or forgot it entirely"，以及过早收敛："agents converged much too quickly… behaved as if the goal was to collapse uncertainty as quickly as possible."

### 人类在环体验（对 D08/D10 直接相关）

- 删坏码容易、砍合理码难："The interaction subtly shifts from what matters most? to can I justify deleting this?"——从判断工作变成命名/辩护工作。
- 作者对逐对核阅策略的负担判断（不代表所有验收方法）："This requires O(n²) comparisons, over pairs of codes, which is not feasible for humans"；缺例子与出处回链时无法理解类别定义。
- **不可证伪类别陷阱**："Vague codes are easy to believe and impossible to act on."——"Reliability and Trust" 这类宽类别无法评估任何针对性修复。
- 疲劳动态："My feedback started dense and detailed, then became sparse over time, partly because of fatigue rather than because the agent was improving."
- 做得好的一点："the agent did do well was summarize what it took away from feedback"——显式复述反馈让人类可核对其是否被考虑。

## 主张卡

| 主张ID | 归属 | 可保留的主张 | 证据限制与开发意义 |
|---|---|---|---|
| SQ-1 | 来源记载 | exp1/exp2-codes/exp2-memo/exp3-hierarchical/exp3-independent 一次性代码种类比例分别93.8%/100%/96.5%/74.2%/4.5% | Figure 3；最低条件同时退化成关键词脚本，不支持“约束外置改善” |
| SQ-2 | 来源记载 | 已赋码推文占451条的5.5%—67.8%；有提前结束、到达后漏码 | Figure 4；到ID450仍可能仅赋码5.5%，比例不是阅读覆盖率，也不能强制无关文本必须赋码 |
| SQ-3 | 来源记载 | 两子agent超时、恢复失败后，编排者改成关键词子串匹配 | Orchestration；正文报告，trace未核。验收要检查任务是否被替换 |
| SQ-4 | 来源记载/作者解释 | exp1长度—代码数ρ=.81，exp2-memo为.15；作者另观察反馈过拟合、后续未维持 | 非同数据配对；相关变化不证明正确性，不能推出反馈“改行为但改不了分布” |
| SQ-5 | 作者体验 | 宽类别难行动、逐对核阅负担大、反馈因疲劳变稀疏 | 唯一人类参与者自述；没有疲劳量表，不是普遍不可验收结论 |
| SQ-6 | 我方推导 | 指标改善须与实际执行方式和语义产物一起审查 | 4.5%反例支持检查方向，不证明某个修复已有效 |

## 案例区块

- 实践者与约束：研究者对 451 推文做扎根理论；目标是探索 agent 辅助边界而非建产品
- 具体做法：六条件系统变化（方法论提示×介入方式×多agent），交互 UI 收反馈，全轨迹记录
- 报告的效果：全部为失败侧量化（见上）；作者结论"机械部分快、没有品味"
- 对我们的可复现性：设计可复制到任意短文本语料；trace viewer 为外链未核

## 适用条件与反证

- 适用条件：短文本开放编码任务；Claude Sonnet 当期版；作者本人既是设计者也是唯一人类被试（偏好=研究者偏好）
- 反证/局限：单语料（推文，短且情绪化）；单模型单次运行/条件（无多 seed）；人类体验为 n=1 自述；"六条件"非全因子设计（两多agent条件都含方法论提示）；trace viewer 未核，正文数字以正文为准

## 与已有条目的关系

- M-033（早停防护）：非编码任务的提前结束与漏码观察；不能以赋码比例识别两者
- M-069（开放生成与有限决策分开）：可提出预定义类别候选，当前混杂配置不足以验证该分工
- M-083（长产物评分校准）：作者对逐对核阅负担及宽类别难行动的体验，不能推广为所有验收不可行
- M-096（模型指南）：Sonnet 指南的持续推进（Carrying work through）与编码验证（Verification on coding tasks）两节提示即本文观测到的中途停止类问题——厂商指南与一手研究互证存在性
- D08（退出路径/澄清聚焦）：反馈成本与疲劳的单人质性观察，未证明领域首次或量化疲劳

## 后续动作

- [ ] 需要复现的主张：若测试预定义类别，需保持语料、模型及执行方式可比，并检查实际语义分析、未赋码原因；不以一次性代码比例独立验收
- [ ] 需要补读的：trace viewer 内容（外链）；作者预告的后续工作（长文档/agent 错误分析应用）
- [ ] 复核触发器：模型换代重跑；作者发布数据/论文
