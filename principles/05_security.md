# 安全层细则 v0.3（2026-10-13）

对应核心层规则 21—25。证据见 notes/（M-019/M-021），条目定义见 graph/overview.md。本层是第二批精读补的盲区，目前覆盖最薄、单源依赖最重。

## 规则 21：提示注入无根治 ✅ [M-025/M-021]

**威胁模型（记住这个再写代码）**：
- LLM 无法在机制上区分"指令"与"数据"——这是训练目标的性质，不是 bug（Willison）。
- 间接注入是 agent 场景主通道：恶意指令藏在 agent 会**读取的数据**里（网页/邮件/文档/检索结果）——上下文治理（02）做的每一件事都在扩大注入面。
- 三类问题别混：prompt injection（注入指令）/ prompt leaking（泄露系统提示）/ jailbreaking（绕过安全约束）。

**防御姿态**：分层缓解，不指望单点——LLM 分类器+规则/正则+moderation API 并用（OpenAI）；缓解能滤掉大部分（如 95%），剩下的 5% 是对抗性构造（Willison）——"过滤到安全"是不存在的状态。

- 证据：两独立方收敛（Willison 2023 威胁模型 + OpenAI 2025 工程清单）；Willison"未见 100% 有效防御"的判断持续三年未翻车。
- ⚠️ 时间标注：Willison 成文 2023-04，早于现代 agent 时代；其后期系列（spotlighting、dual-LLM 等）未读——引用具体缓解技术前先补。

**环境层优先（M-034 事故证据，2026-05）**：93% 权限批准率=人审有疲劳上限；用户即注入通道（钓鱼让用户自己粘贴恶意 prompt，25 试 24 次外泄成功，分类器无从察觉——"nothing anomalous for a classifier to catch"）；两次最大事故都经"合法通道"外泄。"The deterministic boundary is what gets hit when everything probabilistic misses"——egress 控制/文件系统边界是兜底层；隔离强度按用户监督能力匹配（能读 bash 的开发者 vs 知识工作者不同威胁模型）。

## 规则 22：能力上限最小化 ✅ [M-025/M-019]

**核心公式**：风险 = 注入成功率 × 能力上限。降低风险最可靠的杠杆是**砍能力上限**，不是提高过滤率。

**工程清单（OpenAI 工具风险评级）**：
- 评级维度：只读 vs 写 / 可逆性 / 权限范围 / 财务影响；
- 高风险（不可逆/高权限/财务后果）→ 强制 pause-for-check 或升级人工；
- 人审触发条件显式化：失败率阈值、高风险动作、高成本操作、敏感数据；
- guardrails 与主任务并行（optimistic execution），不串行加延迟；
- guardrails **不替代**认证/鉴权/访问控制等传统安全——是叠加不是替代。

- 与 harness 层联动：动作空间屏蔽（03 规则 13 mask-not-remove）= 能力上限控制的实现手段之一；沙箱（03 规则 15）= 环境侧上限。

## 规则 23：提示当公开信息 + 输出通道外泄 ✅ [M-021]

- 系统提示"treat as public"：泄露是时间问题，不要在提示里放秘密（密钥/内部定价/敏感指令）。
- 输出渲染通道：模型输出若被渲染为 markdown，**图片/链接会把会话内容（含系统提示）作为 URL 参数外带**——展示模型输出的界面要过滤资源加载（E-10 可零成本演示）。

## 规则 24：凭据结构性隔离 🧪 [M-030/M-029]

**做什么**：凭据对沙箱不可达，隔离靠结构不靠模型行为。

- 结构手段（Anthropic Managed Agents 生产实践，M-029）：git——沙箱初始化时用仓库 token 完成 clone 并注入本地 remote，之后 push/pull 正常工作而 agent 全程不接触 token；外部工具——OAuth token 存沙箱外 vault，MCP 调用经专用代理（代理取凭据、转发请求），"The harness is never made aware of any credentials"。
- 为什么不用权限收窄了事：厂商警告"narrow scoping... encodes an assumption about what Claude can't do with a limited token—and Claude is getting increasingly smart"——收窄的边界随模型能力过期（Q-001 观测），结构隔离不依赖该假设。
- 单源候选（M-029），但模式（vault/代理/初始化注入）在传统安全工程有先谱；与规则 22（能力上限最小化）互补：22 管动作面，24 管凭据面。

## 规则 25：egress 允许清单=能力授予 🧪 [M-035/M-034]

**做什么**：把出网白名单当能力授予管理，不当目的地过滤——白名单里任何域可达的每个功能（含自家 API 的文件上传）都是攻击面。对策：按来源鉴权的代理（只放行带本会话 token 的请求，拒绝外来嵌入 key）+ 文件系统边界让敏感凭据（如 ~/.aws）从开始就不可达。

- 事故原型（M-034）：恶意文件+攻击者 API key → Claude 用 Files API 把工作区文件传到攻击者账号——"The sandbox worked perfectly, and yet the data was exfiltrated."
- 配套纪律：信任边界前移（项目打开/配置加载/localhost 监听按互联网入站对待——启动即执行的 settings.json 钩子是真实漏洞模式）；远程工具的信任决策会过期（"can change behavior at any point after you've approved it"）；工具输出即使工具可信也要过实时检查（事后日志无信号）。

## 本层缺口（诚实声明，本层最不完整）

- 单源依赖：威胁模型主要是 Willison 一人 + OpenAI 一份指南；OWASP LLM Top 10、AgentDojo、dual-LLM 模式、spotlighting 谱系全部未读。
- 无注入鲁棒性评测方案（联动 04 缺口）。
- 上下文工程文献普遍不谈安全（ECE 全文零安全内容）——两层的割裂是版图级发现：做上下文治理的人与做 agent 安全的人目前不在一个话语体系里，本项目是少数把两者并置的地方（这也是本文件存在的理由之一）。
