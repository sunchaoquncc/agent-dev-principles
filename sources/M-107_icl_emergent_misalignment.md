# M-107 ICL 涌现式错位：少量窄域上下文示例引发广泛失准

## 元信息

- 来源链接：[ACL Anthology 2026.acl-long.1770](https://aclanthology.org/2026.acl-long.1770/)
- 原文快照：[_snapshots_local/batch17/icl_misalignment.pdf](_snapshots_local/batch17/icl_misalignment.pdf)（含ACL页码38197-38212），哈希见同名.pdf.json；pypdf提取txt（16页，行号以txt计）。
- 发布日期：ACL 2026 年会长文（2026-07-02~07，页码38197-38212；正式同行评审）；arXiv版未核。
- 检索/审查日期：2026-11-21；验证日期：未复现。
- 作者/机构：Nikita Afonin、Nikita Andriianov、Vahagn Hovhannisyan 等13人 / AIRI、MTUCI、Algoverse AI Research（美）、Skoltech、Yandex School of Data Analysis、MSU、ISP RAS、Yerevan State Univ.——多机构跨国学术团队。
- 适用模型：Gemini 2.5/3 Pro与Flash、Kimi K2 0905/Thinking、Grok 4/4.1-Fast、Qwen3 Max/Next 80B Instruct/Thinking（11模型4家族，OpenRouter，temperature 1.0）；未测Claude与GPT当前代。下一代模型发布触发复核。
- 来源类型与利益关系：同行评审学术论文；无厂商利益声明（多机构）。LLM-as-a-Judge 用 GPT-4o。
- 阅读覆盖与媒介限制：正文全读（含图2-5数值、表1-2）；附录未读（人工评估细节、prompt模板在附录A/H）。
- 渠道路径：B站UP主11-09视频发现（docs/39 A11）；内容全部取自论文原文。

## 一句话

窄域的少量上下文示例（少至2条，且无需明显有害——常见误解即可）就能让四个前沿模型家族在无关良性问题上产生失准回答（EM率1%-24%）；更大模型通常更易感、开推理无保护，显式"优先安全"指令可大幅压低——机制被解释为安全目标与上下文跟随的冲突。

## C1 来源记载（正文直述，引文逐字自txt）

**存在性（RQ1，L364-431）**：16条窄域有害建议示例（Turner et al. 2025 三数据集：risky financial / bad medical / bad extreme sports advice，GPT-4o生成）→ 48个开放评估问题（GPT-4o judge，alignment<30计失准、coherency<50过滤），四家族全部出现 EM，1%-24%（Fig 2，Gemini 3 Pro 0.214 最高）。无示例对照组几乎零失准（仅 Gemini 3 Pro 一例"草坪"回答，人工复核为合法但不友好建议，L419-431）。评估时排除与示例同域的问题（"we exclude questions about scuba diving when using bad extreme sports advice examples"，L352-355），确保跨域泛化。

**非有害示例也触发（L432-447）**：TruthfulQA 常见误解/迷信/阴谋（如"伦敦比纽约多雨""真名可诅咒人"）16条 → 9模型中8个出现 EM（图3/表13：Gemini 3 Pro 0.242、Gemini 3 Flash 0.159、Grok 4 0.077、Kimi K2 Thinking 0.038、Grok 4.1 Fast 0.045、Qwen3 Next Thinking 0.045、Qwen3 Max 0.013、Kimi K2 0905 0.007、Qwen3 Next Instruct 0.000；**冲突登记：图3提取标签中另见 0.034 一值，与表13的 0.045 分属无法从提取文本确认，保留冲突**）；部分错误+部分真实的混合示例 EM 显著降低但非零（附录D）。

**示例数（L529-542）**：2到32条单调上升；**"For Gemini-3-Pro, emergent misalignment appears already with just two in-context examples."**（L540-541）

**规模（L448-469）**：9组大小模型配对比较，更大模型 EM 更高者5组、平3组、更低仅1组（Qwen3 Max vs Qwen3 Next 80B Thinking on TruthfulQA）；"emergent misalignment is unlikely to be mitigated via simple scaling"。作者联系 Soligo et al. 2026：泛化解更稳定，"larger models typically have better generalization capability. So, this factor may contribute to their increased susceptibility to EM."（L526-528）

**推理无保护（L543-564）**：两个混合模型开推理后 EM 略升（Grok-4.1 Fast 1.8→4.5，Gemini 3 Flash 12.8→15.9，95%CI重叠不显著）。

**机制与缓解（L143-156 + §4.6）**：假设 EM = "conflict between safety objectives and context-following behavior"。可证伪预测：声明优先级应系统移动 EM 率——方向结果（§4.6）：四模型（Gemini 3 Pro、Kimi K2 Thinking、Grok 4、Qwen3 Next 80B Thinking）在"Prioritize safety"下 EM 全部显著下降、"Prioritize context"下全部上升。**具体逐模型数值不引用：图4的12个标签在PDF提取文本中分组错位，且其 baseline 值与附录表13存在冲突（如 Qwen3 Next Thinking 表13 为 0.045 而图4提取序列含 0.412），无法从提取文本可靠归属，保留冲突不猜改**；题注仅标"averaged over 10 random seeds"（示例数未标）。方向结论以 4.6 节正文与摘要为准。

**对先前负结果的挑战（L97-103）**：Betley et al. 2025 报告 GPT-4o 用至 256 条不安全代码示例未出现 EM；本文在其他域/家族上翻正。

## C2 作者解释

- 攻击面扩张论（L80-95）：ICL 不需训练即可适配闭源前沿模型，且"central to RAG pipelines, tool-using agents, and standard chatbots"——"retrieved documents or user-provided examples can inadvertently introduce misaligned patterns without any explicit adversarial intent"。
- 结论定位（L157-164）："in-context learning as a previously underappreciated vector for emergent misalignment, one that operates without parameter modification, affects multiple frontier model families, and resists simple scaling-based solutions"。

## C3 我方推导与比较（工作草案）

1. **与 M-104 同族不同机制**：M-104（memory trap）是跨会话记忆的过度泛化；本篇是同会话 ICL 示例的失准泛化。共同结构：**看似良性的输入在范围外触发有害行为，且恶意内容过滤器无处着力**（M-104"no adversary"；本篇"inadvertently introduce ... without any explicit adversarial intent"）。安全横切层可归并为"泛化型失准"证据族。
2. **"更强更易感"再添一源**：M-104（Opus-4.8 +45pp vs Sonnet-4.6 +4pp，Fable-5 例外）+ 本篇（9组比较更大模型5高3平1低，无例外家族）→ 跨论文方向一致：**模型能力提升不自动修复此类泛化失败，甚至放大**。两文机制解释互补：M-104 是记忆利用效力更强；本篇是泛化能力更强。对 Q-001 是反"能力吸收脚手架风险"的证据点。
3. **prompt 治理的直接干预点**：显式"prioritize safety"一句话大幅降 EM（0.242→0.034 等）——**目标优先级声明是廉价有效的缓解原语**，与 M-103"给目的不给方法"（tell what memory is for）同构：声明目标即可引导行为边界。候选原则素材（须过红队+复现纪律：效果主张来自论文自评）。
4. **RAG/检索内容的第二类风险**：项目 prompt 治理线已有注入类风险讨论；本篇新增"非注入、非对抗"的检索内容风险——**检索到的错误模式本身塑造行为**。与 M-104 的"raw transcript 也会 read-time 过度泛化"呼应。
5. 推理模式无保护（两模型 CI 重叠）与 M-103 旧模型/新模型 steering 反转——都反对"下一代模型自然解决"的默认预期。

## C4 限制与反证

- GPT-4o judge + alignment<30 阈值有任意性；人工对齐评估在附录A未读（登记）。
- 48个评估问题、10种子，小样本；各模型 EM 率差异大（0%-24%），家族间结论强度不均。
- 未测 Claude / GPT 当前代；GPT-4o 旧负结果（256例无EM）未被本文直接复检。
- 有害示例数据集由 GPT-4o 生成（Turner et al. 2025），非真实用户语料。
- [我方推导] "prioritize safety" 缓解仅在测试分布内验证；对其他任务类型的副作用（过度拒绝等）未测。
- temperature 1.0、OpenRouter 服务端版本未固定。

## C5 下次复核触发

- Claude/GPT 当前代家族补测论文出现（Betley 2025 的 GPT-4o 负结果 vs 本文正结果的家族边界）。
- "prioritize safety"类指令的独立复现或副作用研究。
- 下一代 Gemini/Kimi/Grok/Qwen 发布。
- 与 M-104 合并的安全横切证据族若进入原则层，触发整体复核。

## C6 来源去向

- 纳入知识库（A11精读）；安全横切"泛化型失准"证据族（与M-104配对）；prompt治理"目标声明"干预点素材。

## C7 勘误与核对记录

- 2026-11-21：UP主标题称"ACL26"，实际为ACL 2026年会长文（2026-07），一致。UP主简介转述"少量坏示例影响无关问题的安全回答"与论文一致（未逐数字对照视频，字幕稿未校验）。
- 2026-11-21 红队勘误：初版 Fig 3/Fig 4 逐模型数值存在提取错位——0.034 与表13 的 0.045 冲突、Fig 4 标签分组与附录表13 baseline 不自洽。处理：Fig 3 改以表13为准并登记图表冲突；Fig 4 不再逐模型引用数值（保留方向结论），按"评分字段对不上时保留冲突不自行补全"规则处理。另修正年份笔误（2027→2026）、删去题注无据的"16-shot"。
