# M-098 Vercel d0：删除 80% 工具改为文件系统 agent 的前后对比

## 元信息

- 来源链接：[We removed 80% of our agent's tools](https://vercel.com/blog/we-removed-80-percent-of-our-agents-tools)
- 原文快照（供复核）：`_snapshots_local/batch16_glm_20261018/vercel_tools.html`（SHA-256 e366f68f…，680,320B，见同名 .json）、提取文本 `vercel_tools.txt`（148 行全文）
- 发布日期：2025-12-22（正文标注 "22 Dec 2025"）；主张实质更新日期：未知
- 数据/事件观测窗口：基准对比运行日期未给（v1→v2 重构期间，约 2025 年内）
- 当前适用状态：**历史基线/时间序列证据**（发布已约 10 个月，超出 6 个月新鲜度窗口；模型为上一代 Opus 4.5）——不支撑现行原则升级，仅作 C 类案例与 Q-001 观察样本
- 工件/配置/预算及复现范围：博文全文阅读（含新旧两段配置代码、指标表、教训段）；5 条基准查询的原始数据、提示词、失败样例未公开；未运行
- 阅读覆盖与媒介限制：全文文字；配置代码只读不执行
- 版本日期：2026-10-18 抓取版本
- 利益关系与独立性：Vercel 厂商博客；新架构使用其自家产品（Vercel Sandbox/Gateway、ai-sdk、Next.js）——"简单架构"叙事与其商业利益同向；文中推广 eve 数据分析模板
- 复核触发器：d0 后续复盘或撤回披露；Vercel 发布新版本架构文章；当期模型上第三方重复"减工具"对照
- 检索日期：2026-10-18（C 类筛选子代理发现）
- 作者/机构：Andrew Qu / Vercel
- 适用模型：Claude Opus 4.5（旧一代；对比结论对 5.x 代模型需重测）
- 证据等级：经验断言/厂商自报（5 查询基准、自评成功率）；"3.5x faster / 100% success"不可独立核验
- 框架落点：harness 治理（工具数量/职责分配）；上下文治理（原始文件 vs 预过滤）
- 关联条目：M-047（删减系统提示方向）、M-051（重复探索固化）、D02/D05/D11、Q-001

## 一句话结论

Vercel 报告把内部 text-to-SQL agent 的17个专用工具改为两个工具与可导航的语义层文件后，五查询表现改善。但来源的均值约12步与同组单例100步无法按同一五查询口径同时成立；约102k→61k按表值算约下降40.2%，正文称37%。保留未解释冲突，不替作者补分母。两配置同为Opus 4.5，同时改变工具、检索/文件可见性与SDK示例版本；不能隔离删工具的效果或证明代际吸收。仅作历史架构案例。

## 要点摘录

（引号内逐字取自 2026-10-18 抓取正文。）

### 失败的旧配置（作者归因）

- "It worked… kind of. But it was fragile, slow, and required constant maintenance."
- 旧堆栈：17 个工具（GetEntityJoins、LoadCatalog、RecallContext、SearchSchema、ClarifyIntent、JoinPathFinder、SyntaxValidator、FinalizeQueryPlan…"every edge case meant another patch"；"We were spending more time maintaining the scaffolding than improving the agent."
- 作者对失败层的判断："We were doing the model's thinking for it"——预过滤上下文、约束选项、包裹验证逻辑。

### 新配置

- 两工具：ExecuteCommand（沙箱内任意 bash）+ ExecuteSQL；`instructions: ""`；模型 Claude Opus 4.5。
- 数据层：Cube 语义层以 YAML/Markdown/JSON 文件目录直接进沙箱，agent 用 grep/cat/find/ls 自行导航。
- 前提条件（作者自认）："This only worked because our semantic layer was already good documentation. … If your data layer is a mess of legacy naming conventions and undocumented joins, giving Claude raw file access won't save you. You'll just get faster bad queries."

### 前后对比（5 条查询，作者自报）

| 指标 | 旧（17 工具） | 新（文件系统） | 变化 |
|---|---|---|---|
| 平均执行时间 | 274.8s | 77.4s | 3.5x faster |
| 成功率 | 4/5 (80%) | 5/5 (100%) | +20个百分点（原表写+20%） |
| 平均 token | ~102k | ~61k | −37% |
| 平均步骤 | ~12 | ~7 | −42% |

- 最差个案："The old architecture's worst case took 724 seconds, 100 steps, and 145,463 tokens before failing. The file system agent completed the same query in 141 seconds with 19 steps and 67,483 tokens, and it actually succeeded."

### 教训（作者表述）

- "Don't fight gravity. … Grep is 50 years old and still does exactly what we need. We were building custom tools for what Unix already solves."
- "Every tool is a choice you're making for the model. Sometimes the model makes better choices."
- "Build for the model that you'll have in six months, not for the one that you have today."——[我方推导] 该建议本身是预测性立场，与本库"不靠预测管理失效"的规则相反，仅作作者观点记录。

## 主张卡

| 主张ID | 归属 | 主张与环境范围 | 原文位置与短锚点 | 局限/缺失信息 | 与既有知识的关系 |
|---|---|---|---|---|---|
| VC-1 | 来源记载 | 17 工具→2 工具在 5 查询报告改善，但步骤分母及token降幅存在源内冲突 | "3.5x faster, 37% fewer tokens, 100% success rate" 段 | 5 条查询；查询如何选定未说明；无未参与调优样例；自评成功 | 支持 D02"先最简结构"方向的带数字案例（厂商自报） |
| VC-2 | 来源记载 | 收益前提=数据层已是良构文档 | "This only worked because our semantic layer was already good documentation" | 未给反例数据；"mess"场景是作者假设 | 细化 D04：原始文件直接可见的前提是文件本身可读 |
| VC-3 | 作者解释 | 旧配置失败因"替模型思考" | "We were doing the model's thinking for it" | 观察模式归因；无逐失败例的层定位 | 与 M-047"删减旧补丁"同向；注意两篇都未隔离变量 |
| VC-4 | 我方推导 | 两段示例同为Opus 4.5，是历史同模型整套架构重构，不识别代际吸收；当期适用性未知 | 元信息层 | — | 同模型整套架构取舍的历史自报，不识别代际吸收 |

## 适用条件与反证

- 适用条件：内部数据问答类任务；语义层文档质量高；上一代模型；5 查询规模。任何一条不满足时不可直接迁移
- 反证/局限：
  - 作者自认：数据层乱则"只是更快得到坏查询"
  - [我方审查] 无失败披露（新架构何时仍输旧架构未讨论）；5 条查询的选择与代表性无说明；成功判定标准未定义；无第三方验证；Vercel 产品利益同向；发布超 6 个月窗口，模型已换代两代
  - 步骤/时间数字为均值，无方差

## 与已有条目的关系

- M-047（Claude Code 删减 80% 系统提示）：同"删除组件"家族，一个删提示一个删工具；两篇都是厂商一手、无独立复现
- M-051（重复探索固化）：反向案例——何时值得把探索固化成代码/结构
- Q-001：2025-12同模型架构取舍的历史观察，不识别能力随代际增长而吸收工具
- D02/D11：提供待比较的架构候选，不据这些数字升级原则

## 后续动作

- [ ] 需要复现的主张：在目标任务比较当前可用基线与最小有意义候选，不为复刻营销对照先造17工具旧架构
- [ ] 需要补读的：社区对本文的反响/失败复现（HN 讨论）；d0 后续文章
- [ ] 复核触发器：当期模型上第三方"减工具"对照出现；Vercel 撤回或修订该架构

## 2026-10-18 主审边界

两段示例均为空 instructions，不能作为新版独有改进。上述源内数值冲突不等于已证伪全部效果，但阻止“数字均已核清”的声明。无公开逐查询输入、输出、失败口径，不能以5查询自报推通用减工具指导。
