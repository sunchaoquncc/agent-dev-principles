# K-012 LangChain《State of Agent Engineering》年度调查（2026）

> **2026-10-13审查勘误/适用范围（优先于下文历史解读）**：发布日期不刷新2025-11/12调查窗口；自报样本采用率不能当2026-10现状，也不能验证处方有效。

## 元信息

- 来源链接：https://www.langchain.com/state-of-agent-engineering
- 原文快照（供复核）：https://web.archive.org/web/20261013080633/https://www.langchain.com/state-of-agent-engineering
- 发布日期：2026-06-12（调查窗口 2025-11-18 ~ 2025-12-02，1340 份回复）
- 检索日期：2026-10-13
- 作者/机构：LangChain（商业调查，受众有自选择偏差，见反证节）
- 适用模型：不适用（行业调查，非模型特定）
- 证据等级：可检验结论（调查方法学与分母公开；但样本代表性有限——按"跨厂商工程调查"类证据使用，不按测量数据使用）
- 框架落点：评测横切为主（观测性/评测采用率是本文最有价值的数据）；harness 治理（模型路由/多模型）
- 关联条目：M-024（evals-first）；Q-001（fine-tuning 采用率侧证）；另：LangChain《Agent Engineering: A New Discipline》（2025-12-09，docs/02 在册、未建条目）为本报告学科定义的同源前篇——同源不算独立信源

## 一句话结论

2026年发布的2025年末自报样本：57% 已有 agent 上生产，观测性普及远超评测（原文对照句："Nearly 89% of respondents have implemented observability for their agents, outpacing evals adoption at 52%"；差值约 37 个百分点 [我方推导]）——看得见普及了、判得好没有，这是评测使用状况的研究线索，不证明评测先行的因果收益。

## 要点摘录（引文与数字逐字取自当次抓取）

- 学科定义（LangChain 自家话语，同源前篇为《Agent Engineering: A New Discipline》，未建条目）："Agent engineering is the iterative process of harnessing LLMs into reliable systems."
- 生产采用：57.3% 已上生产、30.4% 开发中；上年为 51%。
- 用例分布（单选）：customer service 26.5%、research & data analysis 24.4%、内部流程自动化 18%。
- **生产障碍排序**：质量第一（约 1/3，"one third of respondents cited quality as their primary blocker"）；latency 第二（20%）；"cost is less frequently cited as a concern than in previous years"。
- **观测性 vs 评测（核心数据）**：89% 有某种观测性（62% 有逐步 tracing）；生产者子群 94%/71.5%。评测：offline evals 52.4%、online evals 37.3%；"not evaluating" 总体 29.5% → 生产子群 22.8%；跑评测的组织中近 1/4 同时用 offline+online。
- 评测手段：human review 59.8%、LLM-as-judge 53.3%；"traditional ML metrics like ROUGE and BLEU see limited adoption"。
- 模型面：>2/3 用 OpenAI GPT 系；>3/4 多模型并用；约 1/3 自建（in-house）模型部署；**57% 不做 fine-tuning**（"instead relying on base models combined with prompt engineering and RAG"）。
- 规模效应：10k+ 人组织 67% 上生产，顶部用例变为 internal productivity（26.8%）；2k+ 人企业中安全升为第二障碍（24.9%）；10k+ 组织的填空回答集中于 hallucinations、输出一致性、以及"context engineering and managing context at scale"。
- 日常使用：编码类 agent 占绝对主导（Claude Code、Cursor、GitHub Copilot、Amazon Q、Windsurf、Antigravity），其次 deep research 类，再次自建 LangChain/LangGraph 类。
- 方法与样本：公开问卷 2 周（2025-11-18~12-02），1340 份；Tech 行业 63%、<100 人公司 49%。

## 案例区块

- 实践者与约束：自我选择的从业者样本（LangChain 受众偏斜：小公司+科技行业过半）。
- 具体做法：问卷（单选主用例+填空）。
- 报告的效果：N/A（调查本身即产出）。
- 对我们的可复现性：数字可直接引用（注明样本与窗口）；无需复现。与我们原则层的对接点：观测性/评测缺口、质量第一障碍、企业侧安全第二障碍。

## 适用条件与反证

- 适用条件：英文社区、LangChain 受众、2025 年末快照；绝对值有偏，相对排序也只描述本样本，不能未经代表性验证推广全行业。
- 反证/局限：
  - 抽样偏差（作者公开了人口学，诚实但偏差仍在）：63% Tech、49% <100 人——生产率数字可能高估全行业。
  - 观测性 89% 的口径含浅层实现（仅 62% 有逐步 tracing），口径宽。
  - 我方怀疑：问卷自报的"已上生产"无验证；与 METR 类行为测量不同属自报类证据。
- 时间性：下一年度报告（2027 中）是自然对照点。

## 与已有条目的关系

- **M-024（evals-first）**：样本中观测性与评测自报采用率不同；不能把比例差当方法有效性证据或全行业认知调查。
- 学科化话语的年度数据续篇：本报告与《Agent Engineering: A New Discipline》（2025-12-09，docs/02 在册、未建条目）同出 LangChain，同源不算独立信源，引用时注明。
- **Q-001**：57% 不做 fine-tuning、以 prompt engineering 与 RAG 为主（原文："instead relying on base models combined with prompt engineering and RAG"）——脚手架（而非训练）仍是主流工作方式；与"吸收假设"互补的另一个视角：用户侧也在把复杂度下放给平台。
- **M-025**：企业规模越大安全位次越高（2k+ 第二障碍）——本问卷分组的自报排序，不能据此确定企业规模的因果影响。

## 后续动作

- [ ] 需要复现的主张：无（调查数据只引用不复现）。
- [ ] 需要补读的反方/正方：上一年度报告对照（51%→57% 的口径是否一致）；非英文社区/大企业侧独立调查交叉。
- [ ] 复核触发器：下一年度报告发布；口径变化时重估趋势。


## 2026-10-14 正文一致性纠正

按既有docs08/总纲裁决及本篇内部证据限制，同步正文中的旧强断言、状态或阅读范围；未重抓来源、未新增效果验证。修改前文本见[_review_archive/2026-10-14-batch13/notes/K-012_langchain_soae_2026.md](_review_archive/2026-10-14-batch13/notes/K-012_langchain_soae_2026.md)，仅供历史追溯。
