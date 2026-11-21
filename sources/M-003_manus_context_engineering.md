# M-003 Manus《Context Engineering for AI Agents: Lessons from Building Manus》

> 当前用途（2026-10-14）：以下保留来源当时的做法与作者主张，仅作历史/自我修订对照；不将旧型号处方或旧“认可”记录作为现行要求。当前原则状态见[证据登记](../principles/07_evidence.md)，效果仍未验证。

> **2026-10-13审查勘误/适用范围（优先于下文历史解读）**：2025-07经验仅历史案例；缓存第一指标、mask-not-remove和动态工具负实验不是通用军规。当前官方tool-search支持按需发现；E-04只测位置。

## 元信息

- 来源链接：https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus
- 原文快照（供复核）：https://web.archive.org/web/20250725000000/https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus（2025-07-25 快照）
- 发布日期：2025-07-18（页面标注，2026-10-13 复核一致）
- 检索日期：2026-10-13（当日两次独立抓取 + Wayback 快照交叉核验）
- 作者/机构：Yichao "Peak" Ji（Manus 团队）
- 适用模型：Claude Sonnet（原文未标版本；外部记载为 3.7，未在原文核实 [外注]）；泛化待验证——解码期 logits-masking 状态机强依赖自托管推理栈，response prefill 则如原文所说"most model providers and inference frameworks support some form of response prefill"，可用性较广
- 证据等级：经验断言（生产教训归纳，无受控实验；价格与 token 比例为可检验公开事实）
- 框架落点：上下文治理为主；harness 治理（沙箱工具编排、动作空间约束）；评测横切（作者当时优先关注KV-cache hit rate + "基准聚焦理想条件"的批评）
- 关联条目：M-007、M-011、M-012、M-013、M-014、M-015、M-016；K-002、K-003、K-006；Q-001、Q-002
- 修订：2026-10-13 v0.2，依红队审查修正 10 处（失实数字归属、虚构节题/引文、prefill 机制、变体对策方向等，逐条见"勘误记录"）

## 一句话结论

Manus在2025年特定长循环产品中优先优化KV-cache，并报告append-only、动作屏蔽、可恢复信息和保留失败轨迹等做法；这些是作者局部经验，不是当前通用输入或工具加载要求。

## 要点摘录

（引号内文字为红队复核确认的原文逐字引文；其余为忠实转述。小节名凡带引号者为原文节题。）

### 作者立场与出发点

- 路线陈述：在"基于前沿模型做 in-context 学习"与"自训端到端 agentic 模型"之间，Manus 选前者，并援引 BERT 时代微调的经验教训（原文无"平台期"表述，初版为过度概括，已改）。
- 立场："no amount of raw capability replaces the need for memory, environment, and feedback"——反"模型吸收一切"叙事（Q-001 反方证据）；修辞："If model progress is the rising tide, we want Manus to be the boat"。
- 工程事实（Q-001/K 素材）：Manus 把自家 agent 框架重写过四次（"rebuilt our agent framework four times"）；平均一个任务约 50 次工具调用。
- 方法论自述：这些是试错得出的局部最优（local optima），非普适真理——作者主动限定适用范围。

### 作者当时优先优化KV-cache命中率

- 生产形态：agent 平均每个任务约 50 次工具调用；原文："the average input-to-output token ratio is around 100:1"。
- 经济学：Claude Sonnet 缓存命中 $0.30 vs 未命中 $3.00（每百万输入 token，2025-07 价格，与 Anthropic 官方 caching 文档一致），10 倍价差。
- [我方推导，非原文]：按 100:1 与 Sonnet 牌价（输入 $3 / 输出 $15 每百万）估算，输入占成本约 2/3（全命中）到 95%（全未命中）——这仅是所给价格和比例下的成本估算，不定义所有上下文工程的首要目标。（初版"输入占成本近半（Manus 生产数据）"为虚构归属且算术不符，已删。）

### "Design Around the KV-Cache"（原文节题；初版误拆为独立一课并虚构节题"Prompts are not manuals—they're programs"，已归位）

- 核心主张：围绕 KV-cache 的结构特性设计系统。三条实践：
  1. **前缀稳定**：prompt 里避免会变的内容——反例是精确到秒的时间戳（"a timestamp—especially one precise to the second"），会持续破坏缓存；动态内容后置。
  2. **append-only**：对话历史只追加、不回改。
  3. **缓存断点**：显式设置 cache breakpoints（原文语境：对不支持自动增量前缀缓存的厂商，手动断点保住长共享前缀）。
- [外注] Anthropic API 最多允许 4 个 cache breakpoints（来源：Anthropic prompt caching 文档，非本文内容）。

### "Mask, Don't Remove"（原文节题）

- 场景：需在对话中途增删工具（如安全收敛、防幻觉）。物理移除工具列表有两重代价：KV-cache 失效；模型对早前上下文里工具存在性的引用悬空（dangling references）。
- 作者当时采用的做法：工具定义留在上下文，**屏蔽动作空间**——Manus 的实现是解码期对工具 token 做 logits masking 的状态机（自托管粒度）。
- 更通用的层次：三种 function calling 模式（Auto / Required / Specified，由长到短的 response prefill 实现）——原文指出多数模型厂商与推理框架都支持某种 response prefill。（初版把三模式误描述为"屏蔽非白名单 token/限制候选集/固定下一 token"，且把 prefill 也标成自托管专属，已改。）
- 附带手法：工具名加功能前缀（`browser_` / `shell_` / `python_`），逻辑分组变成 token 邻接，作者据此组织动作命名；本笔记未核到独立缓存收益证据。
- 原文还记了一次负实验：用类 RAG 方式动态加载工具（"loading tools on demand using something RAG-like. We tried that in Manus too"）——这是其当时配置的负实验，不能推出当前工具搜索或按需加载应禁用。

### "Use the File System as Context"（原文节题；初版节题为虚构引文，已改）

- 原文："we treat the file system as the ultimate context in Manus"——文件系统是承载（Manus 场景下的）终极上下文。
- 压缩原则：**可恢复压缩（recoverable compression）**——丢网页全文但保留 URL、删中间文件但保留路径；信息交给指针，需要时可再取。
- SSM 关联：用户个人化状态以文件系统为载体做联想记忆。
- ⚠️ 勘误记录（v0.2）：初版写"反对过度 RAG、知识存有语义路径的文件、grep/find 检索、无需 embeddings"——原文均无（原文唯一 RAG 出现在 Mask 节且对象是工具动态加载）。M-013 原则句已随之修正。

### todo.md：用复述操纵注意力（recitation）

- 做法：让 agent 把目标与 todo 重述（recite）进上下文——原文原话是复述到上下文的末端（"into the end of the context"）。
- 机制：对抗 lost-in-the-middle（K-002 的对策应用）——目标与当前状态持续占据注意力热区。
- 这是"上下文位置治理"：不只是放什么，还有放哪里、何时重放。（初版"最高优先级项放末端/每步重写"为过度具体化，已按原文措辞收敛。）

### "Keep the Wrong Stuff In"（原文节题）

- 主张：失败尝试不要从上下文删除——原文："error recovery is one of the clearest indicators"（错误恢复是真实 agentic 行为的清晰指标之一；初版"分水岭"为加重表述，已改）。
- 批评基准：主流基准聚焦理想条件下的任务成功（"focus on task success under ideal conditions"），错误恢复欠代表——评测层的结构性缺口。

### "Don't Get Few-Shotted"（原文节题）

- 现象：批量同质任务（如简历审查）中，模型看到自己前几份的动作-观察对后"falls into a rhythm—repeating similar actions"，输出趋同。
- 机制：上下文里的历史轨迹本身就是 few-shot 示例——模型会过度复制自己的早期模式。
- 对策（原文方向）：在 actions 与 observations 的序列化中引入少量结构化变体——不同序列化模板、措辞、顺序/格式噪声。
- ⚠️ 勘误记录（v0.2）：初版把对策写成"字段化结构化输出、每字段独立采样"并引用不存在的"natural-language-y serialized templates"——原文变体加在**轨迹序列化**上，不是约束输出模板。M-016 已修正。

### 结语

- "Less structure, more intelligence."——结构给到最小必要，剩余交给模型智能。（方向上支持 Q-001 的"结构随智能递减"，但前提仍是工程细节决定成败。）

## 案例区块

- 实践者与约束：Manus（通用 agent 产品，多用户并发、长任务、成本敏感；主力模型 Claude Sonnet）。
- 具体做法：前缀稳定+append-only+断点、logits masking 管理工具集、文件系统承载状态、todo.md 复述、错误保留、轨迹序列化变体。
- 报告的效果：100:1 与 $0.30/$3.00 为可核数据；其余为作者自述，无第三方复现。
- 对我们的可复现性：①KV-cache 命中率→成本关系可用任一支持缓存的 API 小规模验证（E-05）；②todo.md复述须另做对照（E-04实际只测要求位置）；③轨迹僵化可复现——批量跑同质任务看输出多样性衰减（E-06）；logits masking 依赖自托管栈，暂不复现。

## 适用条件与反证

- 适用条件：长循环、高并发的生产 agent；推理栈可控或 API 支持缓存断点与 response prefill；成本敏感（成本不敏感时 KV-cache 优先级下降，仅剩能力侧理由）。
- 反证/局限：
  - 作者自认：是"local optima"，非普适原则。
  - 结构性局限：数字与计价绑定 Claude 生态（2025-07）；100:1 是 Manus 任务形态（长浏览器/终端循环）的数据，对话型/短任务 agent 不适用。
  - 我方怀疑：文件系统结论绑定文件系统友好任务域，无对比数据；"错误保留"与 ECE 的 tool result clearing 平台化方向直接冲突（docs/07 D1 具名分歧）。
  - 独立性折扣：全文围绕 Claude 计价与 Hermes 格式，与 Anthropic 证据同处一个模型生态——跨厂商"独立"汇合需打折扣标注（docs/03 v0.2 补则）。
- 与 Q-001 的关系：核心立场是"脚手架不可被能力吸收"（反方）+ "窗口再大也装不下"（痛点 1，与 ECE 的 context pollution 声明独立同向）；但结语"Less structure"承认结构量随智能下降——中间立场。

## 与已有条目的关系

- 与 M-002 汇合（跨厂商同构，带生态折扣）：外部笔记/文件承载状态（M-014）、"少而高信号"（M-007，张力见下）、"窗口扩容不吸收上下文治理"（Q-001）。
- 与 M-002 分歧：工具结果取舍（tool result clearing vs 错误轨迹保留，D1 具名）；工具治理（最小工具集 vs mask 管理膨胀，D5）；压缩策略（compaction 删旧 vs mask+可恢复压缩）。
- 与 M-001 分歧：BEA 五模式学本文完全不用（单 agent+循环派），间接支持 Q-002 的"单 agent 可行"一侧。

## 后续动作

- [ ] 需要复现的主张：todo.md复述另拟对照（不沿用E-04结果）、E-05（缓存命中率→成本）、E-06（轨迹僵化）。
- [ ] 需要补读的反方/正方：Anthropic prompt caching 文档（断点与计价核实）；SWE-agent ACI（工具前缀分组相关论证）；含错误恢复语义的基准（核实"理想条件聚焦"批评）。
- [ ] 复核触发器：Claude/API 缓存计价变更（K-003 时效）；推理栈更换；6 个月例行。


## 2026-10-14 正文一致性纠正

按既有docs08/总纲裁决及本篇内部证据限制，同步正文中的旧强断言、状态或阅读范围；未重抓来源、未新增效果验证。修改前文本见[_review_archive/2026-10-14-batch13/notes/M-003_manus_context_engineering.md](_review_archive/2026-10-14-batch13/notes/M-003_manus_context_engineering.md)，仅供历史追溯。
