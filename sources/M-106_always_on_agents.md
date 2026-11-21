# M-106 Always-On Agents 五原语：常驻智能体的工程架构

## 元信息

- 来源链接：[Building always-on agents](https://claude.com/resources/articles/building-always-on-agents)
- 原文快照：[_snapshots_local/batch17/claude_always_on.html](_snapshots_local/batch17/claude_always_on.html)，哈希见同名.html.json；txt（95行）定位辅助，引文行号以txt计。
- 发布日期：页面提取文本未显示本文日期（相关文章列表最新至 2026-11-17）；UP主11-15视频已引用，推测2026-11-15前后发布，**待核**；主张实质更新日期：未知。
- 检索/审查日期：2026-11-20；验证日期：未验证效果（厂商工程指导文）。
- 作者/机构：William Hu，致谢 Rodrigo Olivares、Michael Segner / Anthropic（claude.com）。
- 适用模型：文中提及 Opus 5.5 / Opus 5 成本对比、Claude Code auto mode；下一代模型发布触发复核。
- 来源类型与利益关系：厂商官方工程指导（教学性质），同时是 Claude Code/Messages API memory tool 的生态导流；一手不等于独立验证。
- 阅读覆盖与媒介限制：正文全读；无图表数值依赖。
- 渠道路径：B站UP主11-15视频发现（docs/39 A3，UP主称"Claude Duet架构"）；内容全部取自原文。

## 一句话

常驻 agent = 事件驱动 + 定时器 + 记忆 + 权限 + 发件箱五原语围着的核心循环：agent 大部分时间在睡，被事件唤醒做一段 run、存状态、再睡——厂商给出每个原语的持久化、去重、单写者、凭据隔离与延期审批等工程模式。

## C1 来源记载（正文直述，引文逐字自txt）

**经济学背景（L4）**："on one long-horizon coding benchmark, Opus 5.5 cost 78% less per solved task than Opus 5, compared with 40% less on typical workloads." 常驻 agent 复兴归因于模型判断力提升+长程任务智能变便宜。

**run/session 模型（L8-9）**："An always-on agent is not actually 'always on.' This is just a description of the user experience." 实际是睡→被事件唤醒→run（收事件、完任务、存信息）→再睡；run 在 session（消息与工具调用transcript）内进行。

**① Event inbox（L13-26）**：不要让事件源直接调 agent（失败模式：并发竞争 run、crash 丢事件）。三组件：持久事件列表（数据库表）、handler（HTTP端点）、worker（后台服务）。事件按源唯一标识去重；一用户一 inbox 起步。最佳实践：
- handler 快速 ack（"Some sources, such as webhook providers, treat slow responses as failures"，L23）；深度校验如 prompt injection 检查放 run 内。
- **"The inbox should be the source of truth"**（L24）：worker 先从 inbox 拉最新事件；worker 中途死亡，新 worker 取同一事件重试。
- **"An inbox should only have one active worker at a time"**（L25）防重复工作/互相覆写；mid-run 新事件三选一：push 到下一 run / 并入当前 / 中断重启。
- worker 批处理 pending 事件（用户连发数条合并单 run 只回一次，L26）。

**② Timers（L28-36）**：follow-up（agent 自设截止）与 schedule（固定节奏）两类；独立持久存储；scheduler 轮询到期→更新计时器状态→向 inbox 加事件→唤醒 worker。

**③ Memory（L38-46）**：独立存储（产品中为文件目录，映射到数据库/对象存储以 outlive worker）。**经验法则（L40）："memory should only hold what the agent can't look up again. If something already lives in another system, such as an issue tracker, you should save a pointer instead."** 四类：用户指令（每 run 加载）；用户笔记（"only an index is loaded at the start of each run, but the agent can pull the individual files into context when it needs more details"，L42）；过往消息（防重复）；任务进度（同 index+按需拉取，L44）。可选 dreaming 整理（引用 M-103 那篇，L46）。

**会话与开销（L48-50）**：初始 overhead（系统提示+工具定义+记忆文件）每 run 常在——保持精简+prompt caching；session 过长则 compact 或开新 session，"Both approaches lose detail, so anything that needs to persist should be saved to memory along the way."

**④ Permissions（L51-56）**："Permissions are where always-on agents carry the most risk."（L52）run 持用户访问权且无人值守，每工具调用三择：自行继续/阻断/等审批。三组件：
- 凭据代理：agent 环境外的 proxy 注入真实凭据，agent 发无凭据请求（L54）。
- auto mode：分类器审高风险动作并拦危险者（Claude Code 同款）；"User review, however, is still necessary for the most important decisions."（L55）
- **deferred tool calls（L56）**：hook 推迟调用；"When a call is deferred, the run ends and the session is saved mid-call."；用户答复作为 inbox 事件回来、新 run 恢复保存的 session；等待期间 worker 处理其他事件不阻塞。

**⑤ Outbox（L58-66）**：输出表+dispatcher 与 inbox/worker 对称；run 三种结局：发消息/不发/deferred 请求。正式 outbox 用于消息节奏控制与错误恢复。消息量治理（L66）：过多变噪音、过少漏要事——"We recommend building evals to find the right balance. In practice, it's better for the agent to start quiet and then earn more of the user's attention over time."

## C2 作者解释

- 五原语拼装循环（L68-70）：inbox 事件→run（新或既有 session）→读记忆取基线→权限内行动→更新记忆→outbox→dispatcher 投递；run 可设 timer 再唤醒，用户回复再入 inbox。"Each run is brief, but the cycle keeps going indefinitely."

## C3 我方推导与比较（工作草案）

1. **与 M-104 的交叉互证（本批最重要发现）**：M-104（普林斯顿+Anthropic）实验证明记忆中的一次性授权会被泛化为跳过确认（memory trap），并建议 harness "asking the user before a remembered preference licenses an irreversible action"；本文 deferred tool calls 正是该建议的产品化原语（run 挂起、session 保存在 mid-call、答复以事件回流恢复）。风险论文与工程文章同期出现于同一厂商生态（本文日期待核，按UP主11-15引用推测同期）——**记忆泛化风险的缓解已进入厂商工程实践**，可作为安全横切层"治理有边界"的证据链（时间关联以日期核实为准）。
2. **幂等/持久恢复的启用条件实例**：AGENTS.md 定位"按条件启用，不默认重点"；常驻 agent 恰是启用条件——inbox 作 source of truth + worker 死亡重试 = at-least-once 投递，配合事件去重与批处理。本文是"什么场景需要持久恢复原语"的一手厂商答案。
3. **单写者原则再现**：一 inbox 一 active worker（L25）与 M-103 L72-76 的共享表并发覆写→单 agent 单页方案同构。跨两文的模式：**多写者并发更新共享状态是记忆/协作系统的共同失败源，厂商方案一致收敛到单写者**。
4. **渐进披露三度出现**：用户笔记与任务进度均"index 先载、按需拉取"（L42/44）+ M-103 的 MEMORY.md 前200行——同一厂商在跨产品线一致执行"注入层小、索引导航"模式，与 M-097 渐进披露对照研究形成厂商实践vs学术测量的呼应。
5. **"只存查不到的、其余存指针"（L40）**：与 M-048 的"业务事实工件与记忆分工"同向——记忆不复制系统事实，存指针。三家（OpenAI/Anthropic 工程文）收敛。
6. 发送量治理（start quiet + evals 定平衡，L66）是行为治理的度量实例：常驻 agent 的"何时不打扰用户"被明确列为可评测维度。

## C4 限制与反证

- 纯指导文，无基准、无失败案例数据；"最佳实践"为厂商经验断言（未验证）。
- 78%/40% 成本数字出自厂商自选基准（未命名具体基准），不可横向比较。
- UP主称此文揭示"Claude Duet 架构"——文中未出现 Duet 产品名（仅 M-103 L70 提及 Duet 一词）；两者关联为UP主解读，本文按自述内容登记，不采用"Duet=五原语实现"的归属。
- 发布日期未从页面核实。

## C5 下次复核触发

- Claude Duet 或常驻 agent 产品正式发布时的架构文档（验证五原语落地形态）。
- auto mode 分类器拦截的公开评测或第三方分析。
- M-104 后续：scope 存储是否进入该架构（当前五原语的 memory 未含 scope 元数据）。

## C6 来源去向

- 纳入知识库（A3精读）；harness 治理线（常驻/持久恢复/权限）核心工程证据；与 M-104 组安全互证对、与 M-103/M-048 组记忆分工共识。

## C7 勘误与核对记录

- 2026-11-20：UP主视频标题称"Claude Duet架构"，原文无 Duit/Duet 字样，产品归属按未证实登记（见C4）。五原语内容与UP主视频简介要点方向一致（未逐条对照视频，字幕稿未校验）。
- 2026-11-21 红队勘误：C3-1"同月（2026-11）"依赖本文未核日期，改为"同期（日期待核）"并弱化时间关联表述。
