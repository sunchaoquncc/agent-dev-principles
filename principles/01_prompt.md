# Prompt 层细则 v0.1（2026-10-13）

对应核心层规则 5—7。证据与勘误见 notes/（M-001/M-002/M-003/M-018/M-019/M-020），条目定义见 graph/overview.md。

## 规则 5：系统提示 right altitude 🧪 [M-008]

**做什么**：系统提示取稳定中间层——足够高层以抵抗模型版本变化，足够具体以可执行；用工具与数据约束边界行为，不写死格式规则。按功能区划分（领域知识/工具/输出模板），用 XML 或 Markdown 标题分隔。追求"最小充分信息"：去掉冗余与离题，而非压长度。

- 适用条件：长生命周期系统（提示要跨模型版本存活）；单次脚本无所谓。
- 反证/张力：与 M-011（前缀稳定）有工程摩擦——按失败模式迭代提示会打爆 KV-cache（docs/07 D2）；Anthropic 自认"提示格式重要性随能力下降"（Q-001 观测表）。
- 证据：ECE（M-002）单源候选。

## 规则 6：指令工程化 🧪 [M-026]

**做什么**：四个动作——①从既有操作文档（SOP）出发写指令，不从零杜撰；②要求模型先分解任务再执行；③每个场景写明边界行动（能做什么、不能做什么、缺信息时怎么办）；④显式覆盖边缘案例（edge cases 单列）。

- 适用条件：有既定流程的业务任务（客服、运维、审批类）。
- 反证：两源（OpenAI 清单式 M-019 + ECE altitude 式 M-002）支持的是不同侧面，打包成一条有拉伸——用时分两条自查。
- few-shot：精选少量多样化 canonical examples，覆盖输入全谱；示例里出现的任何行为生产都会放大（示例即宪法，M-002）。

## 规则 7：工具即接口（ACI）✅ [M-006/M-020]

**做什么**：
- 定义结构=名称+描述+参数 schema+函数（"同构于函数签名"，M-018）；描述写给模型看的自然语言，不需要"AI 特殊格式"。
- **少而精、不重叠**：重叠比数量致命——"15 个定义清晰的没问题，10 个重叠的会出事"（M-019 经验值）。
- 防呆（poka-yoke）：参数默认值、类型约束、前置校验；把可预期的错误挡在调用前（例：代码用绝对路径）。
- token 效率：工具定义常驻每个请求，是最贵的固定上下文开销（M-002）。
- 工具输出格式：模型能理解即可，哪种格式好用**靠实验确定**，不靠理论（M-018："Anything goes as long as Claude can make sense of it"）。

- 证据强度：本层最硬——SWE-agent（M-020，NeurIPS 2024，正文级）**严格消融**：同模型同循环只换接口 +10.7 个百分点（Shell-only 11.00%→18.00%，SWE-bench Lite）；四条设计原则（正文逐字）：
  1. "Actions should be simple and easy to understand for agents."（少选项、简文档）
  2. "Actions should be compact and efficient."（高阶操作合并为单动作）
  3. "Environment feedback should be informative but concise."
  4. "Guardrails mitigate error propagation and hasten recovery."
  消融佐证：编辑器去 linting -3.0pp、完全无编辑命令 -7.7pp；窗口过小（30 行 14.3）或过大（全文件 12.7）都不如 100 行（18.0）；上下文保留最近 5 条观察（18.0）优于全历史（15.0）。
- 分歧记录（docs/07 D5）：本层"最小工具集"处方 vs Manus"工具集必然膨胀→用 mask 管理膨胀"（M-012）——OpenAI 的"重叠度判据"是中间立场（**单源经验值**：15 个定义清晰的没问题，10 个重叠的会出事）。工具多且重叠时先去重叠，再考虑 mask 机制。
- 负结果警示（M-020 消融）：给 agent 仿人类的迭代式搜索接口（逐条翻阅）比不给搜索工具还差（12.0 vs 15.7）——agent 会穷尽式翻完每个匹配。"人类好用的接口≠agent 好用的接口"是 ACI 的核心论点。
- 复现队列：E-08（跨模型工具偏好）、E-09（ACI 粒度消融）。

## 本层缺口（诚实声明）

- 模型专属提示差异（GPT vs Claude vs GLM 的写法差异）**零覆盖**——厂商提示指南信源未读（docs/02 已列）。
- M-008/M-026 均非认可级；prompt 层是五层中证据最薄的一层。
- Q-001 风险最高层：Anthropic 官方已声明提示格式重要性下降——本层条目复核触发器最敏感。


## 规则 26：提示词矛盾审查 🧪 [M-037/M-036]

**做什么**：把系统提示当活文档做卫生管理——上线前+定期扫描矛盾与模糊指令；官方依据（GPT-5 指南，2025-08）：模型"surgical precision"式遵循使矛盾提示"more damaging... as it expends reasoning tokens searching for a way to reconcile the contradictions rather than picking one instruction at random"；早期用户清理核心提示库的矛盾后性能大幅改善。

- 配套手段：逃生口条款（"even if it might not be fully correct"类，允许在明确条件下继续）；按工具分级的确认阈值（支付/删除低阈值、搜索高阈值）；persistence 提示防过早收尾（与 M-033 结构层对策互补）。
- 最小推理档模型更需要提示脚手架：思路摘要/工具前导语/消歧/规划提示（推理 token 越少，提示承载越多）。
- 元提示：用模型自查提示词（"what are some minimal edits/additions"模板）。
- 复现候选：矛盾 vs 修复版提示的推理损耗对照（E 系列可跑）。
