# M-054 CLM：让模型编辑上下文的研究边界

## 元信息

- 来源链接：[原文](https://arxiv.org/html/2609.37725v1)
- 原文快照：[_snapshots_local/batch09/clm.html](_snapshots_local/batch09/clm.html)，哈希/检索时间见同名.html.json；txt仅定位辅助。
- 发布日期：2026-09-29；主张实质更新日期：未知。
- 检索/审查日期：2026-10-13；验证日期：未验证效果。
- 作者/机构：Rulin Shao等 / UW、Meta、MIT、Trillium Labs
- 适用模型：含Qwen3.6-27B、GPT-5.6-Sol；RL Qwen3.5-9B；不同实验配置不能混用
- 来源类型与利益关系：预印本，作者实验与开源链接；一手不等于独立验证。
- 数据/事件观测窗口：v1发表日明确，具体运行日期未核。
- 工件检查范围（当前）：提取文本911行含附录全文、五份README全文；未全面核图/公式、逐表复算或完整执行源码，未运行。首轮部分阅读已被文末补读范围扩展。
- 证据等级：经验断言/作者报告；当前状态：候选，原则升级为零。
- 复核触发器：下一代模型发布、原文修订、反例或新工件出现；超六个月补新据，不刷新旧数据日期。
- 框架落点：prompt / 上下文 / harness及评测安全；关联[总纲](../graph/overview.md)。

## 主张提取

### C1 来源记载

将实时上下文映射为模型可编辑的文件，修改同步到下一轮；上下文管理可以通过提示或训练改变。

范围与位置：Introduction / CLM机制；非无需harness。原文短锚点：each modification immediately synchronized

### C2 来源记载

论文另实现后缀缓存复用以减少编辑后的重算，且讨论可编辑上下文带来的注入风险。

范围与位置：SCR附录B与Discussion；近似缓存，不是无损等价。原文短锚点：approximates re-prefilling

## 局限与解释边界

[我方审查] FLOPs是文中计算口径，不等于API账单或延迟。SCR在原观察版采用SGLang改动；10-18已见vLLM扩展实现、复用旧状态，不能当普通托管API现成能力。小模型未训练时可落后摘要基线；零样本、优化技能和RL结果要分开。没有证明权限/指令可由模型任意改写仍安全。

## 与已有知识的比较

正文Figure 5的统一预算概括与附录E分任务配置存在差异：后者分别写TerminalBench的64轮、BrowseComp-Plus的23,560 token预算/100轮，且CLM编辑轮不计工具轮。这里保留原文口径差异，不表述为完全等预算。图表与附录需逐实验复核，不能仅凭摘要比较。

附录Figure 27另有反例：128K预算下，单代理CLM分数低于摘要方案，计算量也不同。不能把部分预算下的优势写成普遍优于摘要。

Q-001的新研究证据方向：模型承担部分上下文策略仍需要文件同步、执行环境与服务工程；不能解读为外部工程消失。X宣传与论文同源。

## 下一步

检查固定commit与分实验预算；先复算公开统计，再考虑目标任务复现。



## 2026-10-14 第十二批复核

关联[总纲](../graph/overview.md)及[工件审查](./_review_archive/batch12_code_review.md)。本次静态阅读全文/代码，不是运行效果验证；固定commit、文件哈希、范围见审查报告与batch12同名快照元数据。历史判断保留，以下限制优先。

全文核查五份README，未读完整执行源码。ContextBench配置max_steps100000、lm_call_cap0；通用Harness默认64steps、2*steps+24调用上限，不得混称统一预算。编辑回合可不占任务step但不因此零计算；论文/仓库分任务配置差异仍保留。RL需另补a_eff与role_mask管线，不能称一键完整重现。SCR保留旧KV/循环状态，是近似复用；删文字不证明清除信息（我方安全推导）。默认trace可能记录48个prompt token，不能称全服务不记内容。模型/版本、额外GPU内存、FLOPs与真实成本分别报告。


## 2026-10-14 论文抽取全文复读

本地clm.txt全部911行（正文、参考文献、A—G附录）已由独立审查者分七段读完。仅提取文本，部分图/公式和steering原提示未保留，不能称视觉核图或逐字提示审计。详见[全文红队](_review_archive/batch12_clm_full_review.md)。

- ContextBench禁止入模前截断/卸载，答案必须仍在上下文中，是刻意隔离live-context管理的合成诊断。不能迁移成生产应先摄入全部HTML再交模型压缩；业务仍可用模型外解析/字段投影。
- 附录G显示模型自估预算会失真，附录E默认环境提醒与关闭提醒的steering实验分开。模型承担策略不证明无需真实计数及执行约束。
- 保留正文/附录TB轮限、Edge子agent5/6、RL主配置/消融奖励差异；成本统计completed与solved不是同一分母。当前仓库不能填平论文口径。
- 数学单run，Edge从48可运行题选10题、best-of-three；小模型训练前可能落后summary，128K单体也有反例。不能从部分胜出写通用优越。
- SCR额外缓存复用主要来自reasoning stripping，不能把全部节省归主动编辑；FLOPs估算与API费/延迟分开。

可采的是预算信息、上下文职责和比较条件的检查方向；效果仍作者报告。Q001不升级。


## 2026-10-14 正文一致性纠正

按既有docs08/总纲裁决及本篇内部证据限制，同步正文中的旧强断言、状态或阅读范围；未重抓来源、未新增效果验证。修改前文本见[_review_archive/2026-10-14-batch13/notes/M-054_context_language_models.md](_review_archive/2026-10-14-batch13/notes/M-054_context_language_models.md)，仅供历史追溯。

## 2026-10-18 SCR 有界更新（docs29 附带项）

arXiv 仍为 v1（2026-09-29 提交，无修订）；仓库 [facebookresearch/context-language-models](https://github.com/facebookresearch/context-language-models) 在第十二批观察 commit `648a48b2`（2026-10-11）之后新增三笔 SCR 提交（2026-10-14，观察至 `4831982`）：

- 新增 vLLM 实现（`suffix_cache_reuse/vllm`，vLLM 0.19.1 v1 引擎）——**不修改 vLLM 源码**，通过 scheduler 子类与 KV connector 两个受支持扩展点接入。上文"SCR在原观察版采用SGLang改动；10-18已见vLLM扩展实现"限制收窄为"现有 SGLang 0.5.16 修改实现与 vLLM 0.19.1 扩展实现，均需自托管集成，非普通托管 API 能力"。
- 三种子 BrowseComp-Plus（830 题，Qwen3.6-27B，K=6）结果（README 自报，未复算逐例、未运行）：SGLang 版 SCR 以标准 serving 65.5% 的 prefix-reuse FLOPs 达到 accuracy 60.6% vs 59.0%；vLLM 版每题 prefix-reuse FLOPs −24.7%、时间 −12.5%，accuracy 58.88% vs 58.80%。数字为作者报告口径，"accuracy on par"属未检出差异，不是等价证明。
- K 敏感性（64 题）：K 间稳健，收益 K=6 附近饱和；README 新增线性注意力层循环状态仅在缓存请求边界保存导致前缀回退变短的限制说明——与"近似复用"判断同向。
- reasoning stripping 归因细化：830 题上 SCR 超出前缀命中的复用 token 占全部 prompt token 7.8%，其中 5.4 个百分点来自 reasoning stripping、2.4 来自其他编辑——**仅说明这组额外复用 token 多数来自 stripping，不解释全部端到端成本或 CLM 总收益**，且该机制对非 CLM 场景（推理模型模板剥离推理块）同样适用。

快照：`_snapshots_local/batch16_glm_20261018/clm_scr/scr_readme.source`（804267a3…，7836B）、`scr_vllm_readme.source`（99395d57…，12500B）。阅读范围：原GLM账为总README全文、vLLM仅前60行；10-18主审另补读vLLM全文213行（见主审补读账），不能追认为原批已全文；未读 sglang/vllm 源码 diff、未跑基准、未核图。刷新的是工件可得性，不刷新 v1 论文实验日期；Q-001 与本篇候选状态不变。

## 2026-10-18 HF 论文页团队后续（B 类深读补充）

[Hugging Face 论文页](https://huggingface.co/papers/2609.37725)社区讨论（快照 `_snapshots_local/batch16_glm_20261018/clm_hf.html`，SHA-256 见同名 .json；提取文本 131 行全文）。作者 Rulin Shao 两轮回复（页面相对时间"7 days ago"，按 10-18 抓取日折算约 2026-10-11，未独立核）+社区两问，全部读完：

- **服务化自报数字（作者回复，未独立验证）**：vLLM 移植 + Qwen3.6-27B 单张 H200、8 并发会话下"raises throughput from 1.14 to 1.78 requests/s and lowers median time to first token from 1.80 s to 1.09 s"；SGLang 自身计数器显示 BCP 服务计算 −35%（同精度）；TB2.1 上"CLM matches the strongest baseline at 70% of its FLOPs"。计算量比较采用 prefix-reuse FLOPs；吞吐/TTFT是另一组服务测量，不是FLOPs口径。作者认为wall-clock受实现及共享度影响。
- **审计工件设计（回应"编辑后能否审计"）**：发布 harness 每次试验记录——每调用的确切上下文快照（context_snapshots/）、编辑命令与模型所写理由（trajectory.json）、结构化中间上下文（trajectory.ctx.json，Harbor ATIF 的 ATIF-CTX 扩展）、每运行编辑计数（usage.json）；系统提示与初始任务受编辑保护；**后引入的会话内约束不受此保护**；作者认为"带显式模型理由的存储 diff"是好改进（尚无）。
- **作者承认的缺口（对社区批评 ykswang 的回复）**：交互式 p50/p95 延迟与生产负载成本"worth reporting"（未报）；更便宜的专用压缩小模型、重复工具输出的确定性过滤等基线"not among them…good comparisons to add"；**"Detection and recovery during a run: not addressed in this paper"**（编辑删掉关键约束/审计证据的检测与恢复未解决）；生产采用应在"full quality, latency, cost, and reliability trade-off"上决定。
- [我方审查] 该讨论直接回答 B 类"节省是否被回查/维护抵消"的当前答案：作者侧给出了审计工件与服务化数字，但便宜基线缺失与运行中恢复缺口仍在——与上文第十二批"当前仓库不能填平论文口径"的判断一致，不升级效果结论。批评者 ykswang 的质疑本身构成社区红队材料（独立个人，无机构信息）。

## 2026-10-18 主审补读：同表退化与部署边界

vLLM README服务微基准为单H200、约11K token/24节文档、6轮固定回复及工具结果、首轮后60%删改、固定64解码token；每并发槽两段会话，TTFT取2—6轮中位数，非生产流量。8/16并发正结果之外，Qwen3.6-27B **32并发**的标准/SCR/zero-copy吞吐为1.34/0.92/1.27 requests/s，TTFT为2.10/3.21/2.20秒，两种SCR均劣于标准。不能只摘8并发改善，或假定调优已消除退化。

BCP是另一组830题×3种子、8并发、28,672上下文、reasoning-stripping条件下的基准，非生产负载。README版本边界包括vLLM 0.19.1、scheduler hook检查、hybrid需align、单KV connector/单pipeline stage、prefill/decode同server、无speculative decoding及reasoning字段兼容shim；不改源码不等于零维护。仅核README，未读完整实现或运行复现。
