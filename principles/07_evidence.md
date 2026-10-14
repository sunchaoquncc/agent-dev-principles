# 证据与适用性登记 v0.13

> 2026-10-13状态纠正：以下登记是草案依据线索，并非12条均由来源直接推出。核心和细则中的方法步骤、默认工件及组织结构包含助手工程提案。原文存在、建议合理与效果已验证必须分开；当前暂停仅凭结构讨论扩写原则，后续逐条依据采集结果审定。

本附录供维护者读取。首轮文献审查为2026-10-13，本轮选定来源复核为2026-10-14；本项目尚无目标业务验证。D规则是工程工作要求，不代表某种实现已被跨模型证明有效。研究编号不需要业务开发者查阅私有知识库才能理解正文。

## 逐条登记

| 规则 | 适用模型/环境 | 验证日期 | 证据与性质 | 复核触发器 |
|---|---|---|---|---|
| D01 | 泛；生成/分析/执行任务 | 未验证 | S1方法；硬约束与偏好区分为我方设计 | 目标/质量定义变化 |
| D02 | 泛；单调用至编排任务 | 未验证 | S5相邻经验；结构比较为我方工程设计 | 任务/编排/模型变化 |
| D03 | 泛；需模型参与的任务 | 未验证 | S3部分支持；提示构建与责任划分为我方设计，S7仅当前文档参照；S9/S10补规划与规则执行反例，具体流程仍为综合 | 故障/需求/模型变化 |
| D04 | 泛；模型输入与工具结果 | 未验证 | S2支持精简payload的实验方向，非收益证明；S8仅接口事实，表示保真为我方要求；S10/S12仅补表示与有限动作案例 | 数据表示/任务/预算/模型变化 |
| D05 | 泛；工具驱动，副作用要求条件启用 | 未验证 | S1/S2部分支持；返回量/继续读取及重复处理为工程设计 | 工具语义/返回分布变化 |
| D06 | 泛；有跨步依赖或恢复需求 | 未验证 | S1部分支持；持久化/并发为工程推导，旧M-014/M-023仅历史线索 | 状态/存储/编排变化 |
| D07 | 泛；受限数据或动作 | 未验证 | S6高风险相邻案例；鉴权/审批绑定为工程要求 | 身份/工具/威胁变化 |
| D08 | 泛；缺信息、超预算、停止或接管 | 未验证 | S1+S2支持接管；自动退出边界为工程设计；S9/S10补追问成本，S13支持条件性失败策略 | 预算/退出/接管流程变化 |
| D09 | 泛；从单调用到工具流 | 未验证 | S1+S3；诊断方法，最小记录范围为我方设计 | 信息/模型/故障变化 |
| D10 | 泛；生成/分析/执行测试 | 未验证 | S1+S5；按任务检查质量与必要约束 | 真值/评分器/分布变化 |
| D11 | 泛；有比较样例 | 未验证 | S2+S3；质量/成本权衡，维护复杂度为设计要求；S12限制分数/单次成本外推，人工投入为我方综合 | 成本/模型/评分器变化 |
| D12 | 泛；原型交付至目标部署 | 未验证 | S4+S6部分支持；交付深度按范围裁剪为我方设计；S11支持交互状态设计，未验证用户收益 | 模型/客户端/权限/部署变化 |

所有模型相关实现还须在下一代模型发布时复核；所有条目在证据超过6个月且无实质新据时重新评估，不把访问日期算成新证据。上表中的“泛”是建议用途，不是跨模型已验证。

## 来源目录与限制

- S1 / M-038：[业务评测与完整用户旅程](https://hamel.dev/blog/posts/evals-faq/index.html)，发表2026-09-18。
- S2 / M-039：[客服质量与成本：模拟教程的适用边界](https://developers.openai.com/cookbook/examples/agent_optimization/optimizing_agents_for_cost_and_quality.md)，发表2026-09-14。
- S3 / M-040：[从失败轨迹到可回退配置](https://commandline.microsoft.com/the-agent-optimization-loop-and-how-we-built-it-in-foundry/)，发表2026-06-02。
- S4 / M-041：[插件评测与目标运行环境](https://developers.openai.com/cookbook/examples/partners/harness_aware_plugin_evals/harness_aware_plugin_evals.md)，发表2026-09-23。
- S5 / M-042：[结果与必要行为约束](https://developers.googleblog.com/en/the-anatomy-of-harness-engineering-how-to-evaluate-iterate-and-guard-ai-coding-agents/)，发表2026-09-09。
- S6 / M-043：[事故后整改：部署前与执行前的控制](https://www.aisi.gov.uk/blog/building-a-more-secure-environment-for-evaluating-dangerous-capabilities)，发表2026-10-01。
- S6背景：[AISI事故披露](https://www.aisi.gov.uk/blog/incident-report-unsanctioned-agent-behaviour-during-cyber-testing)，发表2026-08-04；与整改同源。

S1为实践者经验且有咨询/课程利益；S2、S3、S5为厂商工程内容；S4为平台与合作方联合案例；S6为政府机构自身事件与整改披露。S2/S4合计一个机构组，不当独立重复。上述日期是发表日期，不等于统一实验日期。

S2默认模拟，不能证明模型路由、缓存或异步节省；正文参考核验日与标题发表日分别核对。S3没有公开reflector优势消融，A/B部署在文中仍属计划。S4公开五例与未公开108题评测不同，比较存在指令混杂。S5为编码场景；S6为特殊危险能力评估，均不能直接推断普通业务效果或风险概率。

## 维护规则

S7 [Prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering.md)、S8 [Agent definitions](https://developers.openai.com/api/docs/guides/agents/define-agents.md)：2026-10-13抓取的滚动官方文档，发表/实质更新日期未知，只核对提示组织及本地context不必发送给模型的接口说明，不单独作为近6个月效果证据，不提升原则验证等级。与S2/S4同机构计源。

v0.8方向裁决：用户实例揭示覆盖缺口，不证明它们是所有项目最高频问题。核心回到任务决策、职责分配、信息设计和有约束的比较；幂等/恢复按条件启用。12条编号延续，D03/04/05/09/10/12适用范围扩展；新增做法是待验证工程设计，没有凭近期文章包装成已证实通用规律。

本地HTML提取探针只显示4个合成样例的字符变化和链接/alt/表格结构丢失；没有token或模型质量结论，不用于声明生产收益。

原则改动保留版本、原因和证据。生产验收需另记录实际模型、配置、数据、日期、评分方式与结果；原文核对和文档检查只验证出处与一致性。旧模型技巧、历史实验与研究争议不放核心运行上下文。


## v0.9：全文复读后的局部修订

2026-10-13文献复读，效果仍未验证。以下链接集中供维护者复核，不进入核心运行上下文。

- S9 / M055：[Pocock Skills访谈](https://newsletter.pragmaticengineer.com/p/ai-skills-with-matt-pocock)，2026-09-17。全文文字复读；71:53—73:44限制所有任务先追问，74:39—75:19补原型规划。个人经验，课程利益，无对照数据。
- S10 / M056：[Appleton设计访谈](https://newsletter.pragmaticengineer.com/p/design-engineering-with-maggie-appleton)，2026-09-23。全文文字复读；38:25—39:18可操作反馈，68:03—68:43报告Skills仍不一致执行。原型经验，未观看画面，历史Elicit经历不算2026实验。
- S11 / M058：[Cornell/Muse访谈](https://www.lennysnewsletter.com/p/how-meta-designed-muse-an-ai-agent)，2026-10-12。全文文字复读；6:24—14:24状态与按需详情，产品方经验，无用户效果验证。
- S12 / M069：[Lindquist/Jev访谈](https://www.lennysnewsletter.com/p/jev-8-real-use-cases-for-the-fastest)，2026-09-30。全文文字复读；有限动作的分层语义判断案例，使用时间短且缺系统性失败分析。厂商辅助说明日期未知，仅限制营销解释，不作新鲜效果证据。
- S13 / M070：[Newman可靠性访谈](https://newsletter.pragmaticengineer.com/p/building-resilient-systems-with-sam)，2026-10-07 UTC。全文文字复读；同参数新请求、结果未知、条件降级。分布式系统经验迁移，不是Agent实验；片头与正文幂等键表述冲突，按正文展开判断，未核听。

S9/S10/S13同发布频道但不同嘉宾；S11/S12同节目。频道数量、嘉宾数量均不等于独立验证数量。所有公开稿有转录/缺段风险。

D03的实际纠正记录还参考第十批Eugene工作法M065；D04相关细则参考M064上下文外计算、M068按需工具；D11指标限制参考M066/M067的效果口径审查。这些也是经验/厂商报告，不是新增复现。具体标题、日期及快照由研究笔记和本轮报告登记；核心要求是我方综合，不能由一个来源替整条背书。

本轮D03/D08补反馈与追问成本，D11补人的投入与指标距离，D12补状态呈现；01—04、06、08同步案例和条件。幂等仍按副作用后果启用，D06不升级。保留v0.8历史，候选状态不变。


本轮细则的其他直接来源（均未复现）：
- M064：[上下文外计算](https://www.philschmid.de/superhuman-bash)，2026-09-01；作者自我修订，模型/任务集未公开，不推出Shell普遍最优。
- M065：[从工作反馈形成可复用方法](https://eugeneyan.com/writing/working-with-ai/)，2026-05-03；个人经验，已近六个月，2026-11-03前须复核新据。
- M066：[Snyk客服案例](https://www.langchain.com/blog/how-snyk-turned-an-internal-support-agent-into-a-customer-feature)，2026-10-08；统计自4月上线起，无工单不等于真实解决。
- M067：[Harness模型路由](https://www.langchain.com/blog/how-to-build-a-model-router-in-the-harness)，2026-10-01；厂商试验，未检出质量差异不证明等效。
- M068：[按需Skills与工具](https://www.langchain.com/blog/revamping-skills-in-deep-agents)，2026-10-07；框架及模型缓存条件限制，未运行SDK。


## 第十二批逐项复核（2026-10-14）

仍为12条候选，业务效果未验证。D04只补权威来源/版本，D09补方向与执行两种失败；其他核心保留，细则与案例按下表补充。没有用一期访谈或一次静态审查替整套规则背书。

| 条目/细则 | 本轮依据与处理 | 性质及限制 |
|---|---|---|
| D01/D02 | Thoughtworks产品/执行反馈、E248业务部署补案例；核心不改 | 实践者解释，未证通用结构胜出 |
| D03/提示01 | Pocock固定Skill入口、Eugene全文、AWS反思模板 | 提取条件与反例，自动追加不是自动验收 |
| D04/上下文02 | Thoughtworks现行组织知识、CLM说明、Datawhale反例 | 当前事实与完整请求检查为我方迁移；Datawhale日期未知不作新据 |
| D05/D06/编排03 | Codex核心/UI/不变量；E248既有系统工具 | 核心不改，保留条件性恢复；不强建抽象层 |
| D07/安全05 | CLM trace与缓存残留、Datawhale执行片段 | 静态边界，非漏洞复现；按实际工具风险检查 |
| D08（保持） | Pocock不同入口、Dialkit可调原型 | 核心不改，原型不等于生产，不强制盘问 |
| D09/D10/评测04 | Eugene轻模式/方向偏离、Thoughtworks反馈、AQuA及Harvey代码 | 目标与实现区分，评审通过不等于真实成功 |
| D11（保持） | M046公开CSV/统计审计、CLM分预算、当前路由与旧试验区别 | 不能复算时保留未知；当前源码不替旧效果背书 |
| D12/检查单08 | Dialkit选择落地、E248模型升级再验证 | 核心不改，按实际风险验证版本变化 |

可访问工件：

- [Pocock Skills固定版](https://github.com/mattpocock/skills/tree/49dd158d1076134a641b33efb035946536778336)，版本提交2026-10-09；与九月访谈同作者，不计独立重复。
- [Dialkit固定版](https://github.com/joshpuckett/dialkit/tree/0301abdf0b84fc3d60a4c4fa3a99bfb2044959e3)，提交09-25；React接口/测试静态检查，非运行验证。
- [Thoughtworks访谈](https://www.thoughtworks.com/en-in/insights/podcasts/technology-podcasts/rethinking-the-software-development-process-for-an-era-of-specs-and-ai-agents)，09-17，嘉宾推广Praxa；全文公开稿，非业务对照。
- [AWS优化器](https://github.com/strands-labs/harness-optimizer/tree/da3dd085e987a2105382f9a883b145b26b06608a)，09-21提交；[CLM](https://github.com/facebookresearch/context-language-models/tree/648a48b2b2305624b58204288367026823911828)，10-11提交；后者本轮五份README，不冒称完整源码已审。
- [AQuA](https://github.com/google/adk-recipes/tree/9252494a7aaafca8fe4d81a04f15392345a5779b)，10-13提交，仅两节点；[路由](https://github.com/langchain-ai/open-swe/tree/d1ada86e352cf406b1c07dbefd5275c53a407604)，10-13提交，仅middleware。
- [Harvey LAB](https://github.com/harveyai/harvey-labs/tree/a15650fe74bb20b86f160aaabdad75b87a91b6e8)，10-08提交；7工件含一个635项任务，不含配套原始法律材料；不是9月RLM实验版本。
- [上下文文件统计](https://github.com/codeprakhar25/context-files-coding-agents/tree/cfa048e5a83284ac1ba768c0928ec03e6f381865)，08-31提交，实验05—06；291行CSV揭示排除字段及判分口径未对齐。
- [Datawhale](https://github.com/datawhalechina/hello-agents/tree/36f583c233ea5cee4537ef93455702b55053af18)，章节日期未知，仅英文第九章静态反例；不能充当六个月新据。

仓库提交日仅标识观察版本，不是每个文件或方法的发表日期。上述源码和说明来自维护者，同一文章及仓库合并计源。统计复算只验证公开数据的内部关系，不是模型效果复现。

本轮全文复读及新增业务案例：

- [Codex参与者访谈](https://newsletter.pragmaticengineer.com/p/building-codex-with-tibo-sottiaux)，2026-09-09；发布方文字稿全文，未核听，模型/训练合作经验不能等同业务团队能力。
- [Airbnb访谈整理](https://www.latent.space/p/airbnb)，2026-10-02；全文，匿名/汇总成效仍自报。
- [Eugene工作法](https://eugeneyan.com/writing/working-with-ai/)，2026-05-03；全文，个人经验，2026-11-03需新据；轻模式及过拟合反例同时保留。
- [硅谷101 E248](https://sv101.fireside.fm/261)，2026-08-11；约64分钟机器稿全文，未核听；供应商业务部署自述，升级需业务再验证只作案例，收入及隐私强断言不采。

- [硅谷101 E249](https://sv101.fireside.fm/262)，2026-08-20发布；约87分钟机器稿全文，未核听；投资者/深度用户的经验，承认成本前后工作量混杂。仅给04/06补比较条件，不将自主决策信念、产品评价或事故根因当验证事实。

- [硅谷101 E253](https://sv101.fireside.fm/267)，2026-09-28；58分钟机器稿全文，末尾空块/未核听保留；专家数据伪造与多合法输出为项目参与者经验，不是独立量化证明。04增加标答复核，未扩核心。

- [硅谷101 E255](https://sv101.fireside.fm/269)，2026-10-09；46分钟机器稿全文，未核听。商业权限、反馈周期和系统比较为产品方经验；自动完成率及成本无独立复现。
- [CommerceAgentBench固定版](https://github.com/Accio-org/CommerceAgentBench/tree/d38bd1711aa3926653452458a1be02c1efd12930)，08-29提交；README及13份选定任务/评分工件静态全文审查，原始邮件/PDF未取齐。支持04/06检查判据覆盖的案例，不能证明榜单误判频率；与E255同源。逐任务原始运行数据缺失，效果等级不升。

- [晚点178](https://podcast.latepost.com/178)，2026年6月底录制、08-07发布；89分钟机器稿全文，未核听。研究参与者兼创业方自述，评价器权限/搜索预算未完整披露；仅补06科研与业务自改的边界案例，不升级效果，不增核心规则。发布方附录的防作弊解释不当嘉宾已验证的机制。

本轮补全文审查的既有来源（不重复计新增）：

- [RLM参与者访谈](https://www.latent.space/p/rlm)，2026-10-02；101分钟发布方文字稿全文，未核听。压缩与外部回查并用、过多输出无人消费均为参与者经验，Harvey例子不是额外独立验证。
- [Context Language Models论文v1](https://arxiv.org/html/2609.37725v1)，2026-09-29；全文抽取正文及附录，图像未全面核验，未跑模型。ContextBench禁预处理是实验条件；论文预算、后训练与当前仓库默认分别记录。
- [记忆与压缩教程](https://developers.openai.com/cookbook/examples/agents_sdk/building_reliable_agents_memory_compaction)，2026-05-01；全文及可见代码静态读取，示例gpt-5.5/压缩gpt-5.4-mini，SDK未固定。未见最终组合运行、恢复及下一次消费的完整实演；11-01前需近期新据。
- [Progressive Crystallization论文v1](https://arxiv.org/html/2607.07052v1)，2026-07-08；全文，未重跑。固件漂移触发解析回退不代表静默误解析也能被发现，局部token节省不等于总成本归零。


## v0.11：全库复核与读取引导

2026-10-14。12条核心语义保持；新增“问题—章节—决策”路由、读取停止/失效处理及动态工具绑定说明，细化D04/D05的执行入口。依据现有M048/M050/M068/M073及来源限制作我方实施设计，不计新来源，不升级效果。机器稿AI校验仅改善派生文本并显式标疑，不将模型修订视作核听或事实验证。全库覆盖和新发现另存本地批次报告；本包仍不能代表所有Agent开发知识已完备。

- [Hamel/Shreya错误发现文章公开预览](https://www.lennysnewsletter.com/p/advanced-evals-how-to-find-and-fix)，2026-09-22；仅导语至Step3开头全文已得部分，付费余文/插件未读。支持04中先描述失败再诊断的有条件经验，与S1同作者，不算独立复现；100轨迹、10条和30分钟不作通用门槛。

## v0.12：第十四批长产物与实务工件复核

2026-10-14核读。核心12条不变、业务效果未验证；以下只细化01/02/04的条件性方法并补06案例，03/05/08审查后保持。四篇研究正文及附录文字已读，关键表格按HTML保列核对；图片仅图注/正文解释，未核独有图像数据。实务材料降级保留，不以工件存在认定生产效果。

| 来源 | 学到的边界/本轮影响 | 证据限制 |
|---|---|---|
| [LongJudgeBench](https://arxiv.org/abs/2606.01629)，2026-06-01 | 04/06区分标签维度、事实核验与评分覆盖；rubric并非必有收益 | 人工标注口径不同、总体分有缺项；匿名仓库只取空页面，未读评分代码 |
| [DELEGATE-52](https://arxiv.org/abs/2604.15597)、[代码](https://github.com/microsoft/delegate52)，2026-04-17 | 04/06分别验修改目标与其余内容；静态Fiction评分不等于内容保留 | 只审四份选定工件，公开数据为实验子集，表文有冲突；10-17到六个月后保留历史基线，不据旧模型排名给新建议 |
| [压缩回查成本](https://arxiv.org/abs/2608.16370)，2026-08-17 | 02/04把质量、回查、真实用量分开 | 合成环境、小样本；ALFWorld阴性且低完成率；未取得对应代码/逐运行日志，工具次数非账单 |
| [PAIR](https://arxiv.org/abs/2609.36526)，2026-09-29 | 02局部同状态诊断；04离线适配与部署分账；06记录根因误判与负例 | 离线成本高，表1/D9/D10效果量冲突；未取自身代码/日志。模板中凭据指导冲突，不复制原始秘密 |
| [Tuco公开提示复盘](https://gist.github.com/raj-tuco/c934b988c5db3a9027ecbaecc66d6d91)，Gist2026-09-25 | 信息参与判断应与职责相符；现行提示与未建提案分开 | 作者/生产身份未独立核实；提案日期冲突、98/102与分类分母不符，收益不采为实证 |
| [SCARPA个人RAG工件](https://github.com/chasebarrett/scarpa-rag-n8n)，2026-09-06—08版本 | 01对齐提示与消费端schema；04用坏样例先查评分器 | 个人作品非品牌生产；有提示diff和50题，缺逐题结果。零API只运行选定JS/表达式的合成反例，不是业务效果复现 |

六源不能相互替代独立复现。四篇论文中的当前模型排名、固定窗口、采样次数不升级通用规则；两个个人工件的价值在可审过程和反例，不在自报收益。本地新增六笔记的模型/配置、快照、阅读账和复核触发单独登记；这里不要求开发者读取全部研究材料。低成本配对试验是我方方案，尚未在用户项目执行。

## v0.13：跨项目试用包

2026-10-14新增独立trial目录的使用说明、任务说明和脱敏反馈模板；核心及细则判断保持v0.12，版本统一为v0.13。试用方法是我方实验设计，未取得真实项目反馈；前后收益不能全部归因于本库，更强对照须控制开发投入与上下文污染。
