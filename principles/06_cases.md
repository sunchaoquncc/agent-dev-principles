# 案例索引 v0.1（2026-10-13）

厚层证据入口：每个案例的结构化拆解（实践者/约束/做法/效果/可复现性）在对应笔记的"案例区块"。**原则过期后案例仍是证据**（docs/03：案例层保持厚）。

## 生产级案例（真实系统）

| 案例 | 谁 | 一句话 | 细节 | 关联原则 |
|---|---|---|---|---|
| Claude Code（编码 agent） | Anthropic | hybrid 检索（CLAUDE.md+grep/glob）+compaction（摘要+保最近 5 文件）+todo list 的生产实现 | M-002 案例区块 | M-009/M-010/M-014 |
| Claude playing Pokémon | Anthropic | 长时程记忆外置笔记的极端案例（1234 步后靠笔记续命） | M-002 案例区块 | M-014 |
| Manus 生产参数 | Manus | 100:1 输入输出比、KV-cache 优先、todo.md 复述、错误保留的通用 agent 产品实践 | M-003 案例区块 | M-007/M-011/M-014/M-015 |
| Devin 多 agent 形态 | Cognition | 修订版讨论的形态：检索子 agent/manager（**已上线 Devin**）/干净上下文评审（自报均值 2 bugs/PR）/小模型主控+强模型当工具 | M-017 案例区块 | M-023、K-008 |
| Anthropic 多 agent 研究系统 | Anthropic | 研究型任务上多 agent 对单 agent"substantial improvement"（自报，无第三方复现） | M-002 要点摘录 | M-023、Q-002 |
| 客服 workflow + 编码 agent 域 | Anthropic（客户观察） | 附录 1 两案例：路由分流+分级模型；SWE-bench Verified+按解决计费 | M-001 案例区块 | M-004/M-005 |
| OpenAI 企业部署 | OpenAI | 单 agent 优先+guardrails 分层+工具风险评级的部署经验 | M-019 案例区块 | M-023/M-024/M-025 |

## 实验/演示案例（可复现性高）

| 案例 | 谁 | 一句话 | 细节 | 关联原则 |
|---|---|---|---|---|
| 400 行 agent | Amp（Thorsten Ball） | LLM+4 工具+循环写完代码编辑 agent；工具偏好靠实验发现 | M-018 案例区块（源码可下载，本库可复现性最高） | M-004/M-006/M-022 |
| SWE-agent ACI 消融 | Princeton 等 | 为 agent 重设计接口：SWE-bench ~2%→12.5%（受控对照，NeurIPS 2024） | M-020 案例区块 | M-006 |
| Flappy Bird 双 agent | Cognition | 两个 agent 分做背景与小鸟，上下文不共享→背景被建成 Super Mario 风、与小鸟不匹配 | M-017 要点摘录 | M-023 |
| METR 时长域曲线 | METR（第三方） | 50% 时域每 ~7 个月翻倍；能力增长的度量基线 | K-007 案例区块 | M-024/K-007 |
| 注入外泄演示 | Simon Willison（引 Greshake 等） | markdown 链接/图片带参会话内容外泄 | M-021 案例区块（E-10 可零成本复现） | M-025 |

## 反向更新样本（知识过期的行为证据）

| 样本 | 事件 | 启示 | 载体 |
|---|---|---|---|
| BEA 编者注（2026-08） | Anthropic 给 2024-12 经典文加"工具环境已变"注，指向 Managed Agents | 厂商自己的原则文 20 个月就需修订 | K-004/M-001 |
| Cognition 自我修订（2026-04） | "别建多 agent"→"智能并行+写单线程" | 绝对化主张十个月收回；修订本身比原文更有教学价值 | K-009/M-017 |

## 待补案例位

- 生产级多 agent 失败案例（现在只有 Flappy Bird 演示级）；
- 注入攻击真实事件（非演示）；
- compaction/memory tool 内置化后的官方替代方案实践（触发器命中后回填）。
