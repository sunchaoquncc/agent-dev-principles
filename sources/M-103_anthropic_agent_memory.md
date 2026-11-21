# M-103 Anthropic Agent 记忆架构：四层表示与 Dreaming 整理

## 元信息

- 来源链接：[The components of agent memory](https://www.anthropic.com/research/components-of-agent-memory)
- 原文快照：[_snapshots_local/batch17/anthropic_agent_memory.html](_snapshots_local/batch17/anthropic_agent_memory.html)，哈希/检索时间见同名.html.json；txt 仅定位辅助（有损提取，89行，引文行号以txt计）。
- 发布日期：2026-11-06（B站解读视频发布于2026-11-11，称原文发表于11-06；HTML正文无显式日期字段，此日期待快照核验，暂按视频转述登记）；主张实质更新日期：未知。
- 检索/审查日期：2026-11-20；验证日期：未验证效果（厂商自评）。
- 作者/机构：Lance Martin 执笔，编辑团队见文末致谢 / Anthropic。
- 适用模型：Claude Opus 5 / 5.5、Sonnet 5 / 5.5、Fable 5、Opus 4.7、Sonnet 4.6、Sonnet 3.7（正文各实验分别使用）；下一代模型发布触发复核。
- 来源类型与利益关系：厂商官方研究博客，展示自家的 Claude Managed Agents / Claude Duet / Claude Code；一手不等于独立验证。
- 数据/事件观测窗口：CL-Bench 1.0、Pokémon Red、Stainless 语料（约35万文件）、Harvey LAB；未提供实测运行日期。
- 工件/配置/预算及复现范围：全文读完；图表数值不在HTML文本中（图内数字未核）；文末指向cookbooks（dreaming与knowledge wikis），未取。
- 阅读覆盖与媒介限制：正文全读；图1-15仅见文字描述。
- 渠道路径：B站"Agent智能体深度研究院"11-11视频发现（docs/39 A1）；本笔记全部内容取自原文HTML，UP主解读仅用于选题，其转述数字未采信（见C7核对记录）。

## 一句话

Anthropic 给出 agent 记忆的分层图景：会话日志/记忆笔记/wiki等表示/注入上下文多层共存，用 "dreaming"（后台对照原始transcript整理记忆）做修正、建表示、提升层级，并报告了模型代际在"自主判断 salience"上的快速进步。

## C1 来源记载（正文直述，引文逐字自txt）

**定义与边界（L12）**：agent memory 指 Claude 从经验获得、跨会话保留的知识；明确排除 weights 变化、单会话内 in-context learning、以及 compaction（"summaries written by Claude that replace its older turns so it can continue working in a new context window"）。dreaming 概念引自 Letta 与 UC Berkeley 的 sleep-time compute（L8）。

**记忆是预测（L17）**："Memory is, occasionally, a prediction. By writing down a rule, an agent predicts that the pattern it's describing will be relevant again."

**CL-Bench 数据库任务（L18-25）**：每题新会话开始，唯一跨会话通道是记忆目录。模型代际差异（来源记载，各模型行为描述）：Sonnet 4.6 只到"生成理论"（散落未测试的猜测文件）；Opus 4.7 合并为单一参考文档并标注已核/未核事实；Sonnet 5 对答案标 confirmed、错误写 correction；Opus 5 是第一个闭环者——记录"rule (and also how it knew the rule was true), answers to earlier questions, and clear warnings about traps"（L24）。Opus 5.5/Sonnet 5.5 同样闭环，基线略高、加记忆后与 Opus 5 得分相当（L25）。

**Pokémon salience 对比（L28-34）**：Sonnet 3.7 写 413 个记忆文件（225个文件夹）得 1 枚徽章；Fable 5 写 9 个文件（2个文件夹）+ global.md 得 4 枚徽章。Sonnet 3.7 在约 step 10,000 后的 17 步里"created six files, deleted nine others, and took no actions in the game itself"（L31）。Fable 5 只记游戏不直接告诉它的东西（策略/计划/测试过的规则），不记屏幕上随时可读的状态（钱数/位置）。Magikarp 规则原文（L33）："If 3+ balls fail in a row, VARY the timing (insert extra 'wait' presses between menu steps) - the catch landed right after doing this." Opus 5.5 保持小文件夹并通关（L34）。

**Steering（L36-41）**：官方做法是"tell Claude what memory is for, but not how to use it"（L36）。设定"record only failures"规则后，Opus 5 与 4.7 "lost much of the performance boost that memory gave them"（L37）；"For stronger models, giving them freedom to judge salience was more effective than setting fixed rules in advance"（L37）。反向：对 Sonnet 4.6，提示其先读记忆再显式测试理论，benchmark 得分近翻倍（L40）；Sonnet 5 无提示也 10 次中 9 次主动读记忆（L40）。

**Dreaming 修正错误（L43-51）**：Mt. Moon 案例——错误笔记（PokéCenter 在东侧+"Mt Moon DONE"）导致反复掉落同一悬崖路线三次；Claude 写道 "I'm going to stop rather than keep looping."（L50）。dreaming 对照 transcript 修正笔记后，Claude 直返洞中并抵达 Cerulean City（L49）。"The transcript gave Claude a ground truth to validate its memory against."（L49）

**Wiki 表示（L53-63）**：Stainless（"a software company we acquired in May"，L55，未标年份）内部文档约 35 万文件、约 4.2 亿 token；25 题评测；128 个会话逐步建 wiki；从 2 会话到 128 会话，成绩从 13% 升到 48%（L56）。搜索+wiki 联用随 wiki 成长从 54% 升到 61%，单搜索 53%；联用省约 2 万 token/题（L57）。**并购文档集问答（与 Harvey LAB 为两个并列评测对象，L59-60）**：并购文档 24 题（计分子集为跨文档组合或需判断/计算的题），wiki 87% vs 搜索 73%（L60）；单文档可答的 Harvey LAB 任务上 wiki 无明显增益（L62）。反例：一个 LAB 任务中 "the wiki grew larger than the documents themselves"，作者引 Borges 地图比喻称其 "effectively abstracted nothing"（L62）。

**层级提升与注入（L64-68）**：dreaming 可把重要笔记提升到顶层由 harness 预载进每个会话（context injection），但有三个代价：注入占 token；错误笔记会被带进每个会话；载入不保证被执行——援引 Claude Code 文档警告 "longer instruction files reduce adherence"（L66）。Claude Code auto memory 的做法："It loads only the first 200 lines or 25 KB of MEMORY.md. This header serves as an index"（L67）。

**目标导向与指令自进化（L69-76）**：LAB 收购任务中，初始指令未说明合约条款最重要，多 agent 并写共享表导致 57 个 facts 只存活 41 个（72%）；让 Claude 反思失败、自行改写建 wiki 指令（每合约一页、单 agent、逐字引用而非摘要进共享表）后，"100% of the criteria could be met, up from 72%"（L76）。

**补缺口（L77-80）**：第二轮 dreaming pass 修复 9 个指向缺失页面的链接、新增 3 页（含索引）。

## C2 作者解释（Anthropic 的归因与展望）

- 记忆架构类比海马体（快记）与新皮层（慢整合）、睡眠重放（L5-8）——生物学类比是叙事框架，非证据。
- 开放问题（L81-85）：何时记（即时记分心 vs 后台dreaming延迟可用）；如何保鲜（记忆drift，建议 "focus dreaming on information that's likely to change or to carefully tune the cadence of dreaming"）；transcript search 可作基础、表示层有维护成本。
- "Memory systems will evolve as Claude gets more capable"（L85）——厂商对"模型能力吸收脚手架"方向的表态，与总纲 Q-001 观测相关。

## C3 我方推导与比较（登记到比较前，属工作草案）

1. **与 M-048（OpenAI compaction）口径关系**：本文明确把 compaction 排除在 agent memory 之外（L12）——两家"记忆"词同指异：OpenAI 讲窗口内压缩+业务事实工件，Anthropic 讲跨会话记忆目录。互补非冲突；引用任一家结论时须注明口径。
2. **与 M-049（Letta）同源谱系**：dreaming 承认源自 Letta/UC Berkeley sleep-time compute（L8），厂商间思想传导的直接记载。
3. **渐进披露的厂商一手证据**：MEMORY.md 只载前 200 行/25KB 作索引（L67）——与 M-097 渐进披露对照研究同族，且是"注入层保持小"的三重理由（token/错误传播/遵循度下降，L66）支撑。
4. **"给目的不给方法"的实证**：L37 显示固定规则（record only failures）削弱强模型增益，但 L39-40 显示旧模型需要具体提示——**方向性指导的效果随模型代际反转**，符合项目"每条原则带适用模型字段"的硬规则，且是 prompt 治理层"steering 粒度"的直接证据。
5. **多写者并发问题的解法**：L72-76 共享表被并发覆写 → 单写者+逐字引用。与多智能体协调的通用问题（写冲突）相关，但此处是单任务内方案，不外推。
6. **反例价值**：wiki 膨胀超过原文（L62）是"表示层必须抽象否则负资产"的证据，与 L57 联用最优并列——表示层不是越多越好。

## C4 限制与反证

- 全部实验为 Anthropic 自评，无第三方复现；基准（CL-Bench/Pokémon/LAB）选择权在厂商。
- 图表数值（如各模型具体得分曲线、Figure 3 的 0.564→0.828 类数字）不在HTML文本中，本笔记未引用任何图内数字。
- Pokémon 对比为单次 run（"one run each"，L28），样本量为1，是轶事级证据。
- 模型代际叙事（旧模型不会用记忆→新模型会）可能受基准与提示词设计影响。

## C5 下次复核触发

- 下一代 Claude 模型发布（自主 salience 判断与 steering 效果可能进一步反转）。
- Claude Code auto memory 的 200行/25KB 参数变化。
- CL-Bench 版本升级或第三方独立评测出现。
- 关联 A2（Memory Trap，arxiv 2611.07554）精读后回看本文"错误注入传播"风险（L66）是否被独立证实。

## C6 来源去向

- 纳入知识库（A1精读）；衔接 M-046/M-048/M-049/M-065/M-097 比较线。
- B站UP主解读（BV1KoW16NEBf）字幕快照已存（_snapshots_local/bili_agentyjy_bv1KoW16NEBf_20261120_fx/），未核听、未过机器稿校验，不作为本笔记证据。

## C7 勘误与核对记录

- 2026-11-20：UP主简介称"Opus 5的平均奖励从0.564提高到0.828"，本数字不在HTML正文（疑在Figure 3图中），未采信、未核验，登记为线索。UP主简介其余数字（53%/61%/2万token/87% vs 73%/41→57 of 57）与正文核对一致。
- 2026-11-21 红队勘误：初版把并购文档集24题（87%/73%）误归于 Harvey LAB 名下——原文两者为并列评测对象（L59-60），已更正；Stainless 收购月份"May"未标年份，初版补入"2026年"已删。
