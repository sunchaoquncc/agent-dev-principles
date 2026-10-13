# 证据与适用性登记 v0.9

> 2026-10-13状态纠正：以下登记是草案依据线索，并非12条均由来源直接推出。核心和细则中的方法步骤、默认工件及组织结构包含助手工程提案。原文存在、建议合理与效果已验证必须分开；当前暂停仅凭结构讨论扩写原则，后续逐条依据采集结果审定。

本附录供维护者读取。2026-10-13为文献审查日期；本项目尚无目标业务验证。D规则是工程工作要求，不代表某种实现已被跨模型证明有效。研究编号不需要业务开发者查阅私有知识库才能理解正文。

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
