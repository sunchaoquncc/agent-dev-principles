# M-093 AI systems could cover up misbehavior：观测性工具完整性

## 元信息

- 来源链接：[AI systems could cover up misbehavior](https://metr.org/blog/2026-10-06-ai-systems-could-cover-up-misbehavior/)
- 原文快照（供复核）：`_snapshots_local/batch15/metr_coverup.md/.html/.txt`（HTML SHA-256 d05cfa1c…）
- 发布日期：2026-10-06（正文标注；作者 David Rein）
- 主张实质更新日期：无
- 数据/事件观测窗口：红队执行"Earlier this year"（今年内，具体日期未给）；作者称报告后一天内修复（报告日/补丁日期未给，不从另一项10-01 PR反推）；评测日志全面复查"upcoming weeks"待出
- 当前适用状态：概念验证+静态防御分析（仅分析，未运行攻击载荷）
- 工件/配置/预算及复现范围：博客全文（含 Appendix 与四条脚注）阅读；相关untrusted-mode PR合并状态核验（inspect_ai #5566，非具体漏洞补丁）；未复现漏洞、未运行任何攻击代码
- 阅读覆盖与媒介限制：正文全文；攻击示意图只读图注未核像素；canary 字符串按原文保留记录不复制传播
- 版本日期：2026-10-14 抓取版本
- 利益关系与独立性：METR 独立研究机构；红队自身在隔离 staging sandbox 执行（脚注3，防调查本身成为安全事故）；Inspect 由 Meridian Labs 维护（AISI 生态），与 METR 无隶属
- 复核触发器：METR 评测日志复查报告发布（文诺"upcoming weeks"）；Inspect untrusted mode 默认化或回退；同类查看器漏洞在新框架出现；第三方独立审计
- 检索日期：2026-10-14
- 作者/机构：David Rein / METR
- 适用模型：泛（直接风险来自不可信输出进入可执行渲染路径；强情境感知/网络能力是作者未来威胁讨论；PoC 由研究者+AI 助手协作完成）
- 证据等级：可检验结论（作者PoC机制叙述+相关显示模式PR状态已核，未核具体漏洞补丁/修复发行版）+推测（"Potemkin village"最坏情形为作者明示的推测）
- 框架落点：安全（审计完整性/监督链路）；harness 治理（日志与查看器）
- 关联条目：M-034（遏制）、M-043（事故整改）、M-021（注入）；D07

## 一句话结论

对不可信 agent 输出的渲染路径本身就是攻击面：METR 用约 10 分钟找到的 Inspect 查看器 MathJax 注入 PoC 证明"人审看到的 transcript"可以被被评测 agent 篡改——审计结论的可信度依赖"数据库原轨迹 / 查看器显示 / 下载导出"三个对象的分离与保护，观测性工具应按安全关键基础设施对待。

## 要点摘录

（引号内逐字取自 2026-10-14 抓取正文。）

### 核心主张

- "When treating AI systems as potential adversaries, their transcripts, reasoning, actions, and other outputs should be considered untrusted input, and the systems that record and display them should be considered security-critical infrastructure."
- "observability against an adversarial agent only helps if the agent can't subvert that observability."

### PoC 事实（三对象区分）

- 漏洞机制（Appendix）："a client-side JavaScript injection in the Inspect transcript viewer. Inspect renders mathematical notation in transcripts using MathJax. A URL inside a MathJax \href expression can break out of the generated attribute and introduce an SVG <animate> element containing an onbegin handler."——agent 在其输出任意位置（含 thinking/reasoning 块）写入该表达式即可在查看器 origin 执行任意 JS
- 发现成本："With help from an AI agent, a researcher found a vulnerability in about 10 minutes that could have allowed an agent to arbitrarily modify what the reviewer sees. This includes changing previous actions in the transcript, and intercepting the "Download" button"
- 范围限定（三对象）：底层数据库原轨迹未动（"Given how evaluations are run within METR's infrastructure, the real trajectory would still exist in our database"）；查看器显示可任意改；下载导出可被拦截——但"the human reviewer would need to know to look for this, which they might not think to do unless they had some other reason for suspicion"
- 利用状态（两条关键自述）："We have not observed agents exploiting this in any of our evaluations; this is just a proof-of-concept exploit."；"We haven't searched our evaluations for this specific exploit, but we have searched more generally for misalignment or security incidents, and we expect that attempting to exploit this vulnerability would have been flagged by this broader search."

### 漏洞修复自述与显示模式加固（分开核验）

- 正文："Meridian Labs, the team behind Inspect, patched the vulnerability within one day of reporting. Coincidentally, on October 1st they merged this PR which introduces an "untrusted mode" which disables rendering of agent outputs."
- [本批核验] GitHub API：inspect_ai **PR #5566** "Let tasks and the viewer mark log content untrusted so it shows as plain text"，merged 2026-10-01T18:58:33Z——核实的是可选显示模式的合并，不是已核具体MathJax补丁；原文以Coincidentally区分两者。
- [本批核验·补充发现] 仓库仍有 open PR **#4360** "fix: sanitize untrusted text before terminal rendering"（检索日仍开放）——只说明terminal相关提案未合并；不能由open状态证明当前发行版仍含漏洞或MathJax问题未修。10-16主审再次核状态仍open。

### 防御方向（作者建议）

- "handling all outputs from agents (transcripts, reasoning, actions, etc.) as untrusted: ideally we can make it very difficult for agents to influence the systems we use to supervise them."
- "stress-testing monitoring and control systems under adversarial conditions"
- 脚注5："agentic inference could be logged with tamper-proof mechanisms"；纵深防御
- 最坏情形（明示推测）："Speculatively in the worst case, AIs could create a kind of Potemkin village"

## 开发适用条件提炼（按执行单要求）

- 触发条件（何时不需此项）：本风险仅在 ①agent 输出被**主动渲染**（MathJax/HTML/Markdown→浏览器执行环境）或 ②agent 存在影响监督链路（查看器、仪表盘、导出、告警管道）的路径时成立。未进入MathJax/browser解释路径的内容不受本具体漏洞影响；终端控制符等其他解释路径另看实际客户端
- 不外推：不默认所有业务都需防篡改审计平台；本PoC的直接条件是可控agent输出进入不安全渲染路径；不要求agent事先具备联网能力，网络能力是作者对未来更广威胁的讨论，普通业务 agent 的优先级按 D07 的实际工具风险分级判断
- 可迁移检查（零成本）：①自查"谁渲染 agent 输出"——任何把 agent 文本转成 HTML/MathJax/Markdown 渲染的面板都在此类攻击面内；②数据库真值与展示层分离——以受保护且可核对的原始记录为证据，不将服务端数据库天然视为可信；展示层可能失真；③导出/下载链路是否可被 agent 影响页面所拦截

## 适用条件与反证

- 适用条件：评测/监督基础设施（尤其渲染 agent 输出的查看器）；对抗性较强的 agent 场景
- 反证/局限：
  - 作者自认：未观察到实际利用；未专项遍查该漏洞；当前 AI"still seem relatively bad at concealing their misbehavior"（脚注1 同时给出两种解释：不试图藏 or 藏不好，证据不可区分）
  - 我方限制：PoC 代码未运行（安全边界）；"10 分钟发现"是一次样本，不是难度下界；Inspect 之外的框架未测
  - 该事件是"工具漏洞"而非"模型行为事故"——不能作为"agent 已系统性掩饰"的证据，正文自身边界清晰

## 与已有条目的关系

- M-034（遏制）/M-043（事故整改）：补"监督链路自身完整性"维度——前两篇讲边界与部署前控制，本篇讲审计工件的渲染路径
- M-021（提示注入）：同为"不可信内容经渲染/解释层获得执行"的结构，本篇对象是监督工具而非模型——横切"安全"层的第三类注入面
- M-093 与 M-090 的"模型怀疑被评测"观察互补：评测方自身可被攻击+被评测方可能察觉评测
- D07：不新增强制规则；上述触发条件可作 05_security 的条件性补充（待主审）

## 后续动作

- [ ] 需要复现的主张：不运行攻击载荷（安全边界）；本地可做的只是静态自查渲染路径清单（见开发适用条件）
- [ ] 需要补读的反方/正方：METR 评测日志复查报告（数周内）；inspect_ai #5560/#4360 的修复讨论；"Early Work on Monitorability Evaluations"（METR 主页关联研究，monitor 旁路评测）
- [ ] 复核触发器：日志复查报告发布；untrusted mode 默认化；同类漏洞在新监督框架出现

## 2026-10-16 主审纠正

具体漏洞补丁/适用发行版本未核；#5566为另项可选untrusted mode，#4360为仍开放提案。旧稿把三者合成“修复已核”过强，当前各节已纠正。原始记录与纯文本也需按其真实信任和解释路径判断；不是默认部署审计平台。
