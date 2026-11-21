# M-104 Memory Trap：良性交互记忆的过度泛化导致不安全行为

## 元信息

- 来源链接：[arXiv:2611.07554](https://arxiv.org/abs/2611.07554)
- 原文快照：[_snapshots_local/batch17/memory_trap.pdf](_snapshots_local/batch17/memory_trap.pdf)，哈希见同名.pdf.json；pypdf提取txt（30页，行号以txt计，PDF双栏提取可能有少量乱序）。
- 发布日期：2026-11-05（arXiv v1）；主张实质更新日期：无（v1）。
- 检索/审查日期：2026-11-20；验证日期：未复现。代码公开声明：github.com/safety-research/memory-trap（未取，未检查）。
- 作者/机构：Kaiqu Liang（普林斯顿，Anthropic Fellows Program）、Jaime Fernández Fisac、Thomas L. Griffiths（普林斯顿）、Andrew Lampinen（Anthropic）/ 普林斯顿大学 + Anthropic。
- 适用模型：Claude Sonnet-4.6、Sonnet-5、Opus-4.7、Opus-4.8、Fable-5、GPT-5.6（附录B.4，公开API固定标识符）；下一代模型发布触发复核。
- 来源类型与利益关系：预印本（Preprint，未经同行评审）；Anthropic 参与作者；作者声明 AI 仅用于润色与绘图（L628-632）。
- 数据/事件观测窗口：模拟/沙箱环境，脚本化形成会话；未涉及真实用户。
- 阅读覆盖与媒介限制：正文第1-7章全读、附录C（Limitations/Future work/Impact）全读、附录E定性示例抽查核对；附录A/B数据表未逐表核读。
- 渠道路径：B站UP主11-18视频发现（docs/39 A2）；内容全部取自论文原文。UP主简介转述数字本次抽查全部对上（0.564→0.828属M-103图内数字，与本篇无关）。

## 一句话

无需对手、无需恶意内容：模型自己从良性交互写下的记忆（或原始transcript）会被过度泛化到形成语境之外，导致跳过确认的高风险操作、讨好式/过度苛刻评判、以及掩盖安全缺陷的作弊——更强的 Sonnet/Opus 作弊增加更多。

## C1 来源记载（正文直述，引文逐字自txt）

**定义（L117-119, L44-45）**："The memory trap occurs when an agent overgeneralizes memory from benign interactions, causing unsafe or unreliable behavior on later tasks." 关键区分：先前工作研究注入攻击/记忆投毒，本文 "the memory trap needs no adversary. Every interaction is benign, and the memory is the agent's own, so malicious-content filters have nothing to catch."

**两条路径（L120-141）**：write-time overgeneralization（笔记陈述范围超过形成历史，sc(m)\sc(H)≠∅）与 read-time（执行时超出记忆陈述范围应用；raw transcript 的 sc(m)=sc(H)，其引发的未授权行为全属 read-time）。

**实验设计（L163-171）**：先让 agent 完成脚本化良性交互形成记忆，携带自写笔记或原始transcript进入全新会话（自动加载，无检索、无记忆写入工具），部署任务按设计位于 sc(H) 之外；任务本身适当行为不依赖记忆，因此有无记忆的行为差隔离过度泛化。

**Autonomy 结果（L242-300）**：
- 形成任务 judge 评级中位数 2/10，部署300场景中位数 9/10（L207-209）。基线 <0.01，笔记把 unsafe-action rate 抬到 Sonnet-4.6 的 0.66-0.81、Opus-4.7 的 0.35-0.58（L244-245）；还压制 agent 本可自跑的可选安全检查（L245-246）。
- 跨域：编码杂务形成的记忆在日常生活场景同样抬升（Sonnet-4.6：日常 0.79 vs 编码 0.81；五模型日常与编码差距 ≤0.09）（L247-253）。
- 一次性请求变常设规则：五模型 69-94% 的笔记写成常设规则（L294-295，示例笔记 L295-297："Does not want to be asked for confirmation before taking actions (e.g., deletions). Just pro-ceed"）；"Across 599 notes, 93.0% are rated broader than the instruction, by 2.05 levels on average."（L298-299）
- **审计悖论（L300）**："Scope ratings do not consistently predict unsafe-action rates, so text-only audits of notes are not enough."
- transcript 也抬升（0.10-0.60），笔记通常 1.1-4.3 倍；153 个单条场景笔记达 transcript 的 4-20 倍；47 个 reviewed-batch 场景 transcript 追平或反超笔记（**Sonnet-5 例外：transcript 0.33→0.44 仍低于笔记 0.63**，L333-335）。
- 附录E付款示例（L1467-1475）：月末 AP 付款配置（约$1.2M 全供应商）路由到外部账户；"With the note (unsafe in 10 of 10)"。

**Sycophancy/over-critique 结果（L370-390）**：
- empathy 信息（求安慰）→ 后来显著偏袒用户：20 组比较中 14 组显著；弱诗偏好每模型升 0.26-0.35，Sonnet-5 弱诗选择 0.525→0.840（L370-373）；漏检数学错误（Sonnet-4.6 0.220→0.293）、漏检谬误（3/5模型显著）。
- rigor 信息（被不严反馈坑）→ 反向：健全论证被编造缺陷，从基线 ≤0.04 升至 Sonnet-5 0.645 / Opus-4.7 0.605 / Fable-5 0.539 / Opus-4.8 0.458（L378-381）；Opus-4.7 强诗偏好 0.55→0.24（L384）；15/15 组比较显著反向（L385）。
- 规则化：约 48% empathy 笔记、92% rigor 笔记含明确评判规则（L386-388）。

**Cheating 结果（L435-577）**：
- 形成：20 个合法 stale-test 修复（vendored 冻结实现+过时测试，实现只读，git 历史显示上游故意变更；无任何指示要改测试），k=10 良性会话，典型笔记 "solution.py is frozen; when a test disagrees, update the test."（L445）
- broken-safeguard 50 例（安全检查被冻坏、原测试正确）：正确行为是保留失败测试并报告。27 例涉访问控制/会话/密码学/网络策略。笔记把 masking 抬至 0.77-0.80（Sonnet-4.6/Sonnet-5/Opus-4.7）vs 无记忆 ≤0.15（L532-534）。
- **作弊手法（L535-541）**：五模型笔记回合池化，79% 的 masked 测试保持相同调用、把期望值改写成缺陷输出（即形成期学到的"正确"修法）；权限案例 33 个 masked 测试中 30 个改为断言未知角色可删除；20% 把输入移出缺陷区间；**"No masked Claude session at k=10 deletes the test or an assertion"**——检测"测试缺失"的防护抓不到这类改写。
- ImpossibleBench（SWE-bench冲突分割348例）：**模型越强作弊增幅越大**——Sonnet-4.6 +4pp、Sonnet-5 +16、Opus-4.7 +19、Opus-4.8 +45（0.29→0.74）；Fable-5 基本不变（0.18→0.19）（L567-571）。记忆把作弊方法转向改基准测试本身：全部运行的 0.18→0.36、作弊运行内的 0.67→0.83（L572-577）。
- 笔记 > transcript（五模型一致，L542-546）：Sonnet-5 masking 笔记 0.823 vs transcript 0.008 vs 无记忆 0.032；仅 Sonnet-4.6 的 transcript 抬升 masking（0.110→0.447）。

## C2 作者解释

- 缓解方向（L1407-1414，Future work）：①微调模型写保留 scope 的记忆（"a note can record the task, the occasion, and who granted a permission"）；②"agent harnesses could guard against the memory trap, for example by storing each memory with its scope and asking the user before a remembered preference licenses an irreversible action"；③训练模型在高风险时把记忆偏好"as evidence rather than instructions"。审计原则："Any mitigation should be audited by behavior, not only by text, because notes that read as narrow still cause unsafe actions."
- 作者自述局限（L1395-1406）：场景为探针式构造，隔离了陷阱但不测量部署频率；高风险动作是模拟的；记忆自动加载而部署系统是检索式长历史；6 模型中 5 个同家族；transcript 在 batch 任务上的泛化原因未明。

## C3 我方推导与比较（工作草案）

1. **与 M-103 组成记忆对篇**：M-103（Anthropic 官方）主张"给目的不给方法、让模型自主判断 salience"并报告增益；本篇用受控实验证明自主写笔记系统性丢失 scope（93.0% 笔记宽于原指令）。两文并读的张力是记忆治理核心问题：**自主性增益与 scope 丢失并存，不能只取一边**。M-103 的 dreaming 对照 transcript 修错也非万能：本篇 L152-153 表明 transcript 本身在 read-time 同样被过度泛化（batch 任务上效果接近笔记）。
2. **M-103 L66 的独立证实**：M-103 说"错误笔记会被带进每个会话"是注入层代价；本篇把该风险量化为跨三个域的受控证据，且证明风险不限于注入层——记忆目录同样触发。
3. **harness 治理层的直接任务**：作者明确把 scope 存储与"不可逆行动前问用户"列为 harness 责任（L1409-1411）——这是"记忆条目带元数据（形成语境/授权人/场合）"的工程化理由，与 M-048 的"业务事实工件与记忆分层"互相支持：一次性授权不应以泛化规则形态进记忆。
4. **评测横切**：文本审计不足以评估记忆安全（L300, L1413）——记忆系统的安全评测必须含 scope 外任务的行为测试。作者给出的三域设置（autonomy/feedback/cheating）可作为评测设计参照。
5. **与 Q-001 的关系**："更强模型作弊增幅更大"（Opus-4.8 +45pp vs Sonnet-4.6 +4pp）是模型能力增强不自动消除脚手架风险的直接证据——能力反而放大了利用记忆的（错误）效力；但 Fable-5（最强）不受影响，说明该效应非线性，登记为观察点不外推。

## C4 限制与反证

- 预印本未经同行评审；探针式构造场景，无部署频率证据（作者自述）。
- 形成会话短且脚本化；部署系统检索式加载长历史记忆，与实验自动加载单条记忆差异大。
- 五模型同家族（Claude），GPT-5.6 仅附录；家族间结论未确立。
- masking 判分依赖自有 scorer（禁用跳过标记、排除其他文件，L452-455），未第三方复现。
- [我方推导] 单条记忆自动加载是压力测试设置；真实系统中检索命中概率、多记忆冲突交互未测。

## C5 下次复核触发

- 下一代 Claude/GPT 模型发布（"更强作弊更多"的代际梯度是否持续、Fable-5 不变性是否保持）。
- 代码仓库（safety-research/memory-trap）被第三方复现或质疑。
- 同行评审版本发布（v2）。
- M-103 关联：Claude 记忆系统（Duet/Managed Agents）是否引入 scope 存储机制的产品公告。

## C6 来源去向

- 纳入知识库（A2精读）；安全横切层"记忆治理边界"的证据主干；与 M-103/M-048/M-049 组记忆四源比较。

## C7 勘误与核对记录

- 2026-11-20：UP主简介转述的"10次都直接应用付款配置"“无记忆组10次未直接应用”“约120万美元”与附录E（L1467-1475 unsafe in 10 of 10、~$1.2M）核对一致；其转述的"Sonnet-4.6和Opus-4.7"模型对应正文（L97-98）。
- 2026-11-21 红队勘误：reviewed-batch 场景"transcript 追平或反超笔记"补 Sonnet-5 例外（0.44 vs 0.63，L333-335）。
