# Harness 层细则 v0.1（2026-10-13）

对应核心层规则 1—4、13—16。证据见 notes/（M-001/M-003/M-017/M-018/M-019/M-020），条目定义见 graph/overview.md。

## 规则 1：复杂度递增 ✅ [M-004]

**升级阶梯**：集成（检索/示例）→ 单次 LLM 调用 → workflow（预定义路径）→ agent（模型自主）。升档条件=度量证据（evals 对比），不是"感觉 agent 更强"。

- 三独立方同向：Anthropic（"finding the simplest solution possible"）、Amp（最底档实证：LLM+工具+循环<400 行）、OpenAI（"Most successful teams start with a single agent and incrementally add complexity as needs arise."）。
- **硬数据（v0.6 补，M-027↔M-020 并置，K-010）**：2024-07 时点、同基准（SWE-bench Lite）、同基模型（GPT-4 Turbo）下，固定三阶段管线（Agentless：定位→修复→验证，无自主决策）32.00%@$0.70，反超 ACI 精调的 agent 循环（SWE-agent）18.00%@$1.67——**"从简单开始"不只是稳妥，当时即最优**。时点性注明：2025 年后强模型时代 agent 系统已反超；该对照是 Q-001 时间序列上的数据点，不是永久判决。
- 判断"何时 agent"：开放式问题、步数不可预测、要探索解空间；代价=延迟与成本换任务表现（M-005 ✅）。
- 五类 workflow 模式速查（M-001，正文非附录）：prompt chaining（串行+检查门）/ routing（分类分流，可配分级模型）/ parallelization（sectioning 分片+voting 投票）/ orchestrator-workers（动态分解）/ evaluator-optimizer（生成-评审循环）。

## 规则 3：读侧智能并行+写单线程 ◐ [M-023/M-017]

**状态说明（v0.2 修正）**：核心表述"agentic contribution to intelligence, single-threaded writes"仅 Cognition 修订版明说；Anthropic（ECE 检索子 agent 隔离）与 OpenAI（单 agent 优先）是**相邻收敛**——故 ◐ 而非 ✅。"默认单 agent"部分由规则 1（M-004/M-019）独立支撑。

**结构**（按 Cognition 修订版讨论的形态）：
1. **只读检索子 agent**（第一适用域，Anthropic 与 Cognition 独立同结论）：主循环发起，单工具+防 query 跑偏的上下文护栏；
2. **Manager pattern**：调度 agent 拆解大任务给子 agent——**已在 Devin 上线**（"This is live in Devin today"）；
3. **并行评审（clean context）**：见规则 14；
4. **小模型主控+强模型当"聪明朋友"工具**：主 agent 用便宜小模型，强模型作为可调用工具；小模型单独主控不够用（原文："SWE 1.5 was not good enough at being the primary model for this setup to really work"）；跨前沿模型验证——是 **capability router（能力路由）而非 difficulty escalator**。

- 反多 agent 的两条检查项（Cognition 原版，仍是拦路测试）：上下文共享不足→世界观不一致（Flappy Bird：一个 agent 把背景做成 Super Mario 风、另一个做小鸟，风格互不匹配）；并行写同一 artifact→隐含决策冲突（"Actions carry implicit decisions"）。
- 原则 1 的细化：共享**完整轨迹**而非单条消息（"Share context, and share full agent traces, not just individual messages"）——但验证者角色例外（规则 14）。
- 未解（Cognition 三问）：弱模型何时升级主控、兄弟 agent 的发现如何上报、上下文传递如何不淹没对端（"The open problems are all communication problems."）。

## 规则 4：框架最小依赖 ◐ [M-022]

- v0.2 修正：强源仅 BEA 一家（"start by using LLM APIs directly"；框架加抽象层/遮蔽响应/妨碍调试）；OpenAI 边栏只反**声明式图框架**（"can quickly become cumbersome"+DSL 成本）且明文让步"标准化程度高的任务仍合适"；Amp 祛魅的是 agent 神秘感、未直接谈框架。
- 使用建议：起步 API 直连；上框架前问自己——是否需要框架兜底的规模化/团队协作，且能接受 prompt/响应被遮蔽的调试成本。
- Q-001 注记：2026-08 BEA 修订把框架推荐从第三方（LangGraph/Bedrock）改成自家 SDK——框架层正向厂商收敛，复核触发器敏感。

## 规则 13：mask-not-remove 🧪 [M-012]

- 中途禁用工具的两重代价：KV-cache 失效+悬空引用；正确做法=屏蔽动作空间：Auto/Required/Specified 三档 prefill（多数厂商支持）到解码期 logits masking（需自托管）。
- 负实验（Manus）：类 RAG 动态加载工具不划算，除非必要不动态增删。
- 工具名前缀分组（`browser_`/`shell_`/`python_`）：逻辑分组→token 邻接→缓存局部性。

## 规则 14：评审用干净上下文 🧪 [M-017/K-008]

- 评审 agent：开新会话、用自包含 prompt、被鼓励给出与作者不同的方案（转述自修订版）。
- 核心发现：**不共享**生成者上下文更利于发现问题——共享会让评审与作者犯同样的错误；Devin 自报该形态均值发现 2 bugs/PR、约 58% 严重（无倍数/速度数据、无人类基线——E-07 验证）。
- （v0.2 勘误：初版"评审死于上下文饥饿而非膨胀"及"2x bugs 且更快"为虚构/失真，已删。）

## 规则 15：错误恢复进循环 ✅ [K-006/M-001]

- 三源同向：错误恢复是 agent 成熟度/agentic 性的核心指标（BEA/ECE/Manus，K-006）。
- 工程面：失败要可检测才可恢复；沙箱（文件系统/运行时/凭据隔离）+搜索/备份类工具让 agent 安全试错；checkpoint 处保留人工反馈通道（M-001）。

## 规则 16：批处理防轨迹僵化 🧪 [M-016]

- 现象：批量同质任务中模型"falls into a rhythm—repeating similar actions"，输出趋同；上下文里的历史轨迹本身就是 few-shot。
- 对策：在 actions/observations 的**序列化**中引入少量结构化变体（不同序列化模板、措辞、顺序/格式噪声）——注意变体加在轨迹序列化上，不是约束输出模板（红队纠错过的高频误读）。

## 本层缺口

- Agentless（反方：更简单结构有时赢）未读——Q-001 支持吸收方的关键反例，harness 层结论的对冲项。
- 生产化三件套（监控/回放/灰度）各源均浅；Claude Managed Agents（BEA 编者注指向）未读。
- E-07/E-08/E-09 复现全部待做。
