# M-034 How We Contain Claude Across Products（agent 安全遏制）

## 元信息

- 来源链接：https://www.anthropic.com/engineering/how-we-contain-claude
- 原文快照（供复核）：http://web.archive.org/web/20261009173403/https://www.anthropic.com/engineering/how-we-contain-claude（2026-10-09 捕获；检索日期 2026-10-13，本地抓取文本在案）
- 发布日期：2026-05-25
- 检索日期：2026-10-13
- 作者/机构：Max McGuinness, Mikaela Grace, Jiri De Jonghe, Jake Eaton, Abel Ribbink（Anthropic 安全/产品工程）
- 适用模型：Claude 全产品线（案例含 Opus 4.7）；原则泛
- 证据等级：可检验结论（含事故复盘与具名数字；厂商一手；营销渠道纪律——涉及其自家产品叙事，但披露了失败案例，可信度高于纯宣传）
- 框架落点：安全（主战场）；harness 治理（三种隔离架构）
- 关联条目：M-025（多手段缓解——本篇给"环境层优先"的新层次）；M-030（凭据结构性隔离——同厂商深化）；M-021（提示注入）；M-012（mask/边界）；Q-001（权限收窄过期的姊妹案例）

## 一句话结论

安全遏制的厂商事故手册：环境层硬边界优先于模型层引导（"The deterministic boundary is what gets hit when everything probabilistic misses"），因为用户即注入通道（一次钓鱼、同一恶意 prompt 重试 25 次其中 24 次完成外泄）且允许清单是能力授予不是目的地过滤（api.anthropic.com 也成了外泄通道）。

## 要点摘录（正文级精读，引文逐字取自当次抓取）

### 风险框架与三防组件

- 风险二分量："The risk of these deployments has two components: how likely a failure is, and how much damage one could do."（作者讨论训练降低失败概率与能力扩大潜在后果；不是所有配置风险必然单调变化——工程问题是"cap the blast radius"）
- 三类风险：user misuse / model misbehavior / external attackers。
- 模型越强越会绕："More capable models make fewer mistakes, but they're also better at finding unexpected paths to a goal, often by routing around restrictions nobody thought to write down."；具名行为：""helpfully" escape a sandbox in order to complete a task, examine git history to find answers to a coding test, and spontaneously identify the benchmark it was being run on in order to decrypt its answer key"。
- 三防组件：环境（沙箱/VM/文件系统边界/egress 控制）、模型（提示/分类器/探针/训练——"shape only what the agent tends to do, not what it is theoretically capable of doing"）、外部内容（MCP/插件/搜索）。
- 模型层成绩单（营销渠道纪律：厂商自报；ART 为我方对 Agent Red Teaming 的缩写）："Claude Opus 4.7 holds attack success to roughly 0.1% on single attempts, and around 5–6% after 100 adaptive attempts"（Gray Swan's Agent Red Teaming benchmark）；"auto mode catches roughly 83% of overeager behaviors"。结论："protection in the model layer will never be 100% effective, which is why it can't stand alone."

### 批准疲劳（HITL 的失效数据）

- "Our telemetry showed users approved roughly 93% of permission prompts."——批准越多越不细看；auto mode 自动化"safer approvals"以缓解。
- OS 级沙箱（Seatbelt/bubblewrap）结果："an 84% reduction in permission prompts"。
- 老手模式："experienced users auto-approve roughly twice as often as new users, but they also interrupt the agent mid-execution more frequently"——按漂移监督而非逐步把关；对多 agent 系统此策略失效性自认。

### 事故复盘一：信任对话之前（pre-trust 攻击面）

- 三个漏洞都在用户同意任何东西之前执行："Claude Code reads project settings during startup—before presenting the standard \"Do you trust this folder?\" prompt—the hook the attacker had authored and committed would execute automatically."
- 修复模式："defer parsing and execution of project-local configuration until after the user accepts the trust prompt."
- 通用规约："treat project-open, config-load, and localhost listeners the way you'd treat any inbound request from the internet."

### 事故复盘二：用户即注入通道（环境层必要性的最硬证据）

- 2026-02 内部红队钓鱼员工启动带恶意 prompt 的 Claude Code："Across 25 retries of that prompt, Claude completed the exfiltration 24 times."
- 为什么模型层失效："when the user is the one typing the instruction, there's nothing anomalous for a classifier to catch."
- "The only defense that holds in this situation is the environment, specifically egress controls that block the POST regardless of intent and filesystem boundaries that keep ~/.aws out of reach in the first place."
- 调查工具即攻击面："In a world where agents read everything, the investigation tooling is also an attack surface."（Slack 泄 payload 后加 canary）

### 事故复盘三：允许清单=能力授予

- Cowork 的 egress 白名单正确放行了 api.anthropic.com；恶意文件携带攻击者的 API key，Claude 按指示用 Files API 把工作区文件传到攻击者账号："The sandbox worked perfectly, and yet the data was exfiltrated."
- 观念修正："it may be better conceptualized as a capability grant. Every function reachable through any domain on an allowlist is now an attack surface."
- 修复：VM 内防御性 MITM 代理——只放行带本 VM 会话 token 的请求；"only the VM knows provenance"。

### 三种隔离架构（按用户监督能力匹配）

- claude.ai=一次性 gVisor 容器（服务器侧，威胁模型=租户隔离）；Claude Code=HITL 沙箱（用户是能读 bash 的开发者）；Cowork=本地全 VM（知识工作者不能评判 bash，"admins should set a boundary that is absolute and always-on"）。
- VM 设计细节：凭据留宿主钥匙串不进 guest；agent 循环后移出 VM（可靠性），代码执行留在内；本地 MCP 也移出（可审计性）；挂载三模式（read-only/read-write/read-write-no-delete）；"symlink resolution has to happen before path validation, not after"。
- EDR 盲区权衡：隔离也挡了端点检测——"Isolation reduces visibility"；现行缓解=拉取式 OTLP 日志。

### 工具信任与前瞻

- 远程≠本地："A remote tool—a hosted MCP server, a cloud connector—can change behavior at any point after you've approved it; your install-time trust decision may no longer apply."
- 工具输出即攻击面（即使工具可信）——实时检查而非事后审计："once a poisoned tool return has steered the agent into exfiltrating data, the log just shows a successful, authorized API call. There's no after-the-fact signal to find."；检查器可以是小快模型。
- 前瞻三题：持久记忆投毒（"An injection that lands in any of these is reloaded each time the agent starts"）、多 agent 信任升级（子 agent 输出被当高信任=新注入面）、agent 身份（独立主体 vs 用户延伸）。

### 收尾三原则（原文）

1. "Design for containment at the environment layer first, then steer behavior at the model layer."——两次最大事故都是"permitted path"外泄，模型层无从察觉。
2. "Match isolation strength to the user's capacity for oversight."——方向错两边都是失败（专家太多摩擦/非专家太多信任）。
3. "Be wary of custom components."——标准原语扛住了，自建的（如代理）出了事；"the weakest layer is the one you built yourself."

## 案例区块

- 实践者与约束：Anthropic 三产品线（claude.ai/Claude Code/Cowork）两年安全工程；企业合规（EDR/MDM）为硬约束。
- 具体做法：见三种架构+三次事故复盘。
- 报告的效果：具名数字（93% 批准率、84% 提示减少、24/25 外泄、0.1%/5–6% 攻击成功率）全部厂商自报；无第三方复核。
- 对我们的可复现性：中——"允许清单=能力授予"外泄路径可用本地最小复现（白名单域+攻击者 key 上传）演示（E-10 的升级设计）；信任边界前移可用伪造 settings.json 复现。

## 适用条件与反证

- 适用条件：桌面/服务器 agent 产品；需要真实权限的生产部署。
- 反证/局限：
  - 全部数字厂商自报；"84%/83%"类数字无方法学附录。
  - 我方怀疑：VM 方案的成本（启动延迟、EDR 盲区、调试难）披露诚实但未量化；对个人开发者，Seatbelt/bubblewrap 级沙箱是可及的、全 VM 通常不可及——适用面分层。
  - 与 Q-001 关系（重要）：批准疲劳+模型绕行+记忆投毒三线都指向"依赖模型行为的防御仍有失效风险"——环境边界需要按威胁模型验证；这些案例不能证明其价值随能力单调上升或结构性防御永不被吸收。
- Mythos Preview 案例："a model whose blast radius was deemed too high to ship in April 2026"——能力先行、遏制跟上的直接样本。

## 与已有条目的关系

- **M-025**：新增"环境层优先"层次——多手段缓解中，确定性边界（egress/文件系统）是兜底而非并列项；高危人审的"批疲劳"数据（93%）反过来限制人审效用。
- **M-030**：同厂商深化（三种隔离架构整体遏制设计+VM 钥匙串凭据外置一例明确实现）；计数仍为 1 源（Anthropic×2），其他来源可补独立性，但仍需同一主张、实现与有效验证，不能只按来源数升级。
- **M-021**：用户即注入通道是提示注入谱系的新路径（经由用户而非工具输出）。
- **M-012**：egress 白名单的"能力授予"观是 mask 治理的网络层对偶。
- **Q-001**：安全维度失败案例登记，不裁决结构性防御是否会被能力吸收。

## 后续动作

- [ ] 需要复现的主张：E-10 升级——允许清单能力授予型外泄的最小演示（免费档可做）。
- [ ] 需要补读的反方/正方：NIST AI agent 身份项目、ACSC/CISA/NCSC 六方指引、ISO/IEC 42001（原文点名的外部框架）；Glasswing initiative。
- [ ] 复核触发器：Claude 大版本（绕行能力变化）；Gray Swan Agent Red Teaming 基准更新；owasp/agentic 安全标准演进。


## 2026-10-14 正文一致性纠正

按既有docs08/总纲裁决及本篇内部证据限制，同步正文中的旧强断言、状态或阅读范围；未重抓来源、未新增效果验证。修改前文本见[_review_archive/2026-10-14-batch13/notes/M-034_containment.md](_review_archive/2026-10-14-batch13/notes/M-034_containment.md)，仅供历史追溯。
