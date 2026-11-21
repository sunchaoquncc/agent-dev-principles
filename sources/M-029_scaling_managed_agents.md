# M-029 Scaling Managed Agents: Decoupling the Brain from the Hands

> 当前用途（2026-10-14）：以下保留来源当时的做法与作者主张，仅作历史/自我修订对照；不将旧型号处方或旧“认可”记录作为现行要求。当前原则状态见[证据登记](../principles/07_evidence.md)，效果仍未验证。

> **2026-10-13审查勘误/适用范围（优先于下文历史解读）**：2026-04-08超6个月；平台托管不等于模型吸收。git remote叙述不足以复刻安全实现，不得将原始token写进remote URL并声称不可读；应外部代理并实测。

## 元信息

- 来源链接：https://www.anthropic.com/engineering/managed-agents
- 原文快照（供复核）：https://web.archive.org/web/20261013080513/https://www.anthropic.com/engineering/managed-agents
- 发布日期：2026-04-08
- 检索日期：2026-10-13
- 作者/机构：Lance Martin, Gabe Cemaj, Michael Cohen（Anthropic）
- 适用模型：Claude 系（案例基于 Sonnet 4.5 / Opus 4.5 行为差异）；设计原则泛
- 证据等级：可检验结论（厂商工程博客一手自述，含具体接口与指标；厂商=营销渠道，见反证节）
- 框架落点：harness 治理（元脚手架设计）为主；上下文治理（session≠context window）；安全（凭据结构性隔离）；评测横切（TTFT 指标）
- 关联条目：Q-001（本文是其一等表述）；M-002、M-003（compaction 不可逆决策）；M-014（外部持久化笔记）；M-023（多脑多手）；M-025（分层缓解）；K-002；K-011（同日产品公告）

## 一句话结论

厂商一手承认 harness 假设会随模型进步而过期（见下节逐字引文），其工程对策不是预测模型能力，而是把 agent 虚拟化为 session / harness / sandbox 三个稳定接口——与本项目"复核触发器而非预测"的总设计同构。

## 要点摘录（正文级精读，引文逐字取自当次抓取）

### Q-001 的厂商直证（开篇即主题）

- "Harnesses encode assumptions that go stale as models improve."（页面导语）
- 正文展开："A common thread across this work is that harnesses encode assumptions about what Claude can't do on its own. However, those assumptions need to be frequently questioned because they can go stale as models improve."
- **context anxiety 案例**（跨代失效的最小完整样本）："in prior work we found that Claude Sonnet 4.5 would wrap up tasks prematurely as it sensed its context limit approaching—a behavior sometimes called \"context anxiety.\" We addressed this by adding context resets to the harness. But when we used the same harness on Claude Opus 4.5, we found that the behavior was gone. The resets had become dead weight."

### 元脚手架：三个虚拟化抽象

- "We virtualized the components of an agent: a session (the append-only log of everything that happened), a harness (the loop that calls Claude and routes Claude's tool calls to the relevant infrastructure), and a sandbox (an execution environment where Claude can run code and edit files)."
- 设计哲学借操作系统："Decades ago, operating systems solved this problem by virtualizing hardware into abstractions—process, file—general enough for programs that didn't exist yet."
- 边界立场："We're opinionated about the shape of these interfaces, not about what runs behind them."；"Managed Agents is a meta-harness in the same spirit, unopinionated about the specific harness that Claude will need in the future."；"But we make no assumptions about the number or location of brains or hands that Claude will need."

### Pet→cattle：为什么解耦

- 单容器耦合的失败模式："by coupling everything into one container, we ran into an old infrastructure problem: we'd adopted a pet"——容器挂=会话丢；"Our only window in was the WebSocket event stream, but that couldn't tell us where failures arose"；调试须进容器 shell，而"that container often also held user data, that approach essentially meant we lacked the ability to debug."
- 解耦后接口：容器成为工具——"It called the container the way it called any other tool: execute(name, input) → string. The container became cattle."；harness 亦可随时重启："a new one can be rebooted with wake(sessionId), use getSession(id) to get back the event log, and resume from the last event. During the agent loop, the harness writes to the session with emitEvent(id, event)"
- "The harness doesn't know whether the sandbox is a container, a phone, or a Pokémon emulator."

### 安全：凭据结构性隔离（对 M-025 的重要细化）

- 耦合设计的风险："any untrusted code that Claude generated was run in the same container as credentials—so a prompt injection only had to convince Claude to read its own environment."（拿到 token 后攻击者可"spawn fresh, unrestricted sessions"）
- 对"窄权限"的警告（安全维度的 Q-001！）："Narrow scoping is an obvious mitigation, but this encodes an assumption about what Claude can't do with a limited token—and Claude is getting increasingly smart."
- 结构性修复两条路径：git——"we use each repository's access token to clone the repo during sandbox initialization and wire it into the local git remote. Git push and pull work from inside the sandbox without the agent ever handling the token itself."；MCP——OAuth token 存沙箱外 vault，经代理调用。总原则："The harness is never made aware of any credentials."

### 上下文治理：session ≠ context window

- 对 compaction 类操作的批判："the standard ways to address this all involve irreversible decisions about what to keep"；"But irreversible decisions to selectively retain or discard context can lead to failures. It is difficult to know which tokens the future turns will need."
- session 作为窗口外的持久上下文对象：`getEvents()` 支持"selecting positional slices of the event stream"，可回看事件前的铺垫、重读行动前的上下文。
- 关注点分离的理由（又是 Q-001）："We separated the concerns of recoverable context storage in the session and arbitrary context management in the harness because we can't predict what specific context engineering will be required in future models."
- harness 内变换可含缓存意识："including context organization to achieve a high prompt cache hit rate and context engineering"（与 M-003 Manus KV-cache 论互证）。

### 性能与规模

- TTFT 定义与收益："That dead time is expressed in time-to-first-token (TTFT), which measures how long a session waits between accepting work and producing its first response token. TTFT is the latency the user most acutely feels."；"our p50 TTFT dropped roughly 60% and p95 dropped over 90%."（厂商自测，未第三方复现）
- 多手=能力边界迁移的又一个案："Claude must reason about many execution environments and decide where to send work—a harder cognitive task than operating in a single shell."其后作者自述：起初把 brain 放单容器正因早期模型做不到多环境推理，"As intelligence scaled, the single container became the limitation instead"——能力增长使旧架构选择反转为瓶颈。

## 案例区块

- 实践者与约束：Anthropic 平台团队；长时程 hosted agent 服务（VPC 对接、规模化、故障恢复是硬约束）。
- 具体做法：session/harness/sandbox 三接口虚拟化；harness 无状态化（wake+getSession 恢复）；凭据处理（git remote为厂商叙述但复刻细节未给；MCP描述vault+proxy，不应把原始token放入可读remote）；容器按需 provision。
- 报告的效果：p50 TTFT ~-60%、p95 -90%（作者自述）；VPC 场景：原文称此前客户"had to either peer their network with ours, or run our harness in their own environment"，解耦后该假设不再成立（未用"原生支持"表述）。
- 对我们的可复现性：接口形状（execute/provision/wake/getSession/emitEvent/getEvents）可直接借为自建 harness 的模块边界；TTFT 收益依赖其托管架构，本地不必复现数字，可复现的是**结构对照**（有状态单容器 vs 无状态+外置日志的错误恢复行为）。

## 适用条件与反证

- 适用条件：Claude 平台语境；长时程任务（超上下文窗口）；多租户/多 VPC 的生产约束。接口分层思想对自建系统泛用。
- 反证/局限：
  - 厂商营销渠道纪律：本文卖点是 Anthropic 自己的托管服务，"meta-harness"叙事同时是护城河论证。TTFT 数字无第三方验证。
  - 抽象比实现长寿是设计信条而非被验证的规律——OS 抽象（process/file）确实是幸存者偏差下的显例。
  - 我方怀疑：session append-only 全量日志的存储/合规成本未讨论；"many hands"对模型的认知负担（文中自己承认是 harder cognitive task）在弱模型上会反转结论。
- 与 Q-001 关系：记录作者报告的context anxiety行为变化、接口设计取舍与凭据风险；它们是不同性质的观察和解释，不证明权限约束过期或平台托管等于模型吸收。

## 与已有条目的关系

- **Q-001**：厂商工程实践出现同构机制（一手表述）——Anthropic 用与我们相同的治理姿态（不预测、给过期留接口）应对，但这是其自述设计应对，非对吸收假设的背书。观测表新增 3 行。
- **M-002/M-003**：compaction 的"不可逆决策"风险被厂商再度确认；session 外置对象 = M-014"外部笔记"的平台级版本。
- **M-025**：凭据隔离与最小权限是互补措施；本文不证明权限收窄过时，也不证明任意代理实现已隔离凭据。
- **M-023**：多脑多手可传递（"brains can pass hands to one another"）是编排模式的相邻注脚——本文主题是执行环境解耦，与读并行/写单线程不同轴，作者亦自认多环境推理是 harder cognitive task。
- **K-011**：同日产品公告的工程背书来源。

## 后续动作

- [ ] 需要复现的主张：无直接廉价复现项（托管服务）；结构思想并入 E-01 设计（有状态 vs 无状态 harness 对照）。
  - [ ] 需要补读的反方/正方：HN 对本篇的讨论（社区对 meta-harness 叙事的质疑）；Cloudflare 集成公告 [外注：WebSearch 检索结果示 blog.cloudflare.com 2026-05-19，未抓取核验]；"prior work on context engineering" 所引的 compaction/memory tool 细节已在 M-002。
- [ ] 复核触发器：Claude 大版本发布（context anxiety 类行为是否复现/消失）；Managed Agents 接口变更（接口稳定性主张的检验）；6 个月例行。


## 2026-10-14 正文一致性纠正

按既有docs08/总纲裁决及本篇内部证据限制，同步正文中的旧强断言、状态或阅读范围；未重抓来源、未新增效果验证。修改前文本见[_review_archive/2026-10-14-batch13/notes/M-029_scaling_managed_agents.md](_review_archive/2026-10-14-batch13/notes/M-029_scaling_managed_agents.md)，仅供历史追溯。
