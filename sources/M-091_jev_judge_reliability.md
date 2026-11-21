# M-091 Jev-as-a-Judge：冻结重放下的评分器一致性、准确性与营销口径

## 元信息

- 来源链接：[博客](https://www.langchain.com/blog/jev-agent-evals-langsmith)、[仓库](https://github.com/danielgshea/jev-as-a-judge)
- 原文快照（供复核）：`_snapshots_local/batch15/jev_blog.md/.html/.txt`（博客 HTML SHA-256 8df92061…）；仓库经 codeload tarball 固定于 main@adfea74905f7（2026-09-19），本地 `batch15/jev_repo/`
- 发布日期：博客 2026-09-20（正文标注）；仓库首次提交 2026-09-17、最后提交 2026-09-19（GitHub API 提交历史）
- 主张实质更新日期：未知（博客无修订记录）
- 数据/事件观测窗口：LangSmith 实验 6d08df72… 始于 2026-09-18T17:53:25Z（README 自述）
- 当前适用状态：有条件方法参照；效果数字为本实验内数字
- 工件/配置/预算及复现范围：博客全文+仓库选定代码静态审查（judges/llm.py、judges/system_one.py、judges/__init__.py、judge_reliability.py、dataset.py）+ 归档结果数据复算（benchmark.json/oracle-labels.json/accuracy.json）+定位草稿与提交历史核验；原批未读offline_evals.py、model.py、archive_benchmark.py、analysis/、tests/；主审独立复核补读model.py、archive_benchmark.py与analysis/common.py、visualize.py相关实现，其余未列文件/tests仍未核；未调用任何模型，未重跑实验；归档不含逐 trial 原始分数，方差/MAE/容差只能核对作者逐例摘要及加权关系，不能从原始序列独立重算
- 阅读覆盖与媒介限制：正文/代码/JSON 全文；SVG 图表未核像素
- 版本日期：main@adfea74905f7；依赖版本 README 自述（deepagents==0.7.15、langchain-typesafe==0.0.1a2 等）
- 利益关系与独立性：LangChain 员工（作者邮箱 daniel.shea@langchain.dev）用自家 LangSmith/LangSmith Gateway 评测 TypeSafe AI 的 Jev，博客末附双方联合直播活动；仓库内 `langsmith-positioning-draft.md` 为"把 LangSmith 编织进方法/结果/结论"的定位草稿——博客叙述经产品定位编辑的直接证据。博客、仓库、TypeSafe 相关材料按同源组处理
- 复核触发器：Jev/TypeSafe 模型更新、LangSmith 实验数据变化、第三方独立复现出现；最迟 2027-01-20 查新据
- 检索日期：2026-10-14
- 作者/机构：Daniel Shea、Seán Roche / LangChain
- 适用模型：judge=Jev（System One，服务版本不可见）、GPT-5.6 Luna/Terra、Claude Sonnet 4.6；被评 agent 模型未在 README 标明（WEATHER_AGENT_MODEL 环境变量）
- 证据等级：可检验结论（归档数据内部关系已复算）+经验断言（跨任务外推）
- 框架落点：评测（judge 校准/方差/成本）
- 关联条目：M-069（Jev 访谈）、M-083（LongJudge 评分器校准）、M-032（评测方法论）；D10/D11

## 一句话结论

在五个固定产物、单人oracle及作者归档口径下，Jev方差最低，但连续quality与该oracle数值距离最大（MAE约0.1064、±0.1比例60%）。可核对摘要关系，未独立重算原始评分。作者已区分quality可靠性与binary准确性；连续刻度距离不是概率校准或通用质量排名。

## 要点摘录

### 实验设计（代码级确认）

- 5 个天气请求（dataset.py），agent 输出冻结重放（`_frozen_output`），每 judge 每 case 重复 100 次；控制了被评产物变化；其余差异仍可能含网关/默认采样/服务状态，不证明随机性只来自模型内部
- 所有 judge 收到相同 state（judges/__init__.py `judge_state`：user_question、expected_behavior、final_answer、tool_calls、search_evidence）——字段名相同，不代表两种judge的输入表达、尺度或模型使用完全对称
- 方差口径（judge_reliability.py）：案例内无偏样本方差→跨案例平均；bootstrap 10k、单元=冻结案例——可读的实现口径；小样本与嵌套依赖限制保留
- README 自述限制："This is a small corpus with five agent runs and one human reviewer. The result describes this experiment; it is not a general ranking of judge accuracy."；"The result is observational, not evidence that the model architecture caused the lower variance."

### 复算核对（本批执行，数字逐字来自归档 JSON）

- 方差：Jev mean variance 1.49436e-05；Luna/Jev=432.9×、Terra/Jev=913.0×（benchmark.json 字段 912.96）、Claude/Jev=91.68×——与 README/博客"92–913×"一致 ✓
- binary accuracy：Jev 500/500；Terra 99.8%；Luna 96.4%；Claude 80.0% ✓（oracle：Dublin=fail，其余四案=pass，单评审员；案例顺序 Tokyo/Seattle/Springfield/Austin/Dublin）
- 成本/延迟与 README 表一致（$0.00035/call、0.44s；Claude $28.17 总额）✓
- 归档元数据两条未见于 README/博客：① experiment.metadata.judge_models 含第五个 judge `gemini/models/gemini-3.6-flash`——元数据有此标识但四judge结果表未列；是否实际调用/排除及原因未知；② `dirty: true`——记录dirty工作区，当时未提交差异未保存，单靠commit不能重建执行代码；不能推数据无效或永远不可复现

### 公开附件中的补充指标与摘要关系核对（正文未讨论该连续刻度差异）

- accuracy.json：Jev quality MAE=0.1064、quality_within_tolerance(±0.1)=60%——**四 judge 中最差**（Luna 0.0874/65%、Terra 0.0767/69%、Claude 0.0780/76%）
- does_pass 方差：Claude=0.0（与 Jev 同为零方差）但 Springfield case 100 次全判 fail（oracle=pass）——**零方差+系统性错误**并存，"稳定地错"的直接实例
- 两例观察：Dublin与Springfield均有澄清输出，但人工oracle分别fail/pass。Claude在这两个固定产物的100次重复中均判fail，其中Springfield与oracle全不一致；这不是对任意反问的通用行为规律，也不能证明未读取expected_behavior字段。Luna两例各9次不一致，Terra的1次不一致在Springfield（99/100），Dublin100/100。
- [待检假设] Jev平均三个Noul输出，LLM平均生成评分，尺度/评分方式差异可能影响方差；没有匹配尺度、温度和任务的消融，不能将概率平滑称已证原因。MAE只测与本oracle的数值贴近，不能直接解释概率校准或错误发现能力。
- 作者accuracy.json及公开quality-agreement.svg已含MAE/容差，README明确连续quality用于reliability、binary用于accuracy；可说博客未讨论该连续刻度差异，不能称作者未披露或未区分可靠性与准确性。

### 口径与公平性缺口

- README："We did not set temperature, top-p, seed, or max tokens for the LLM judges, so provider and gateway defaults applied."——未给 LLM judge 确定化机会，方差对比含该混杂
- "The experiment metadata did not expose the hosted Jev service version."——Jev版本不可见，当前材料不足重建其服务条件
- 归档无逐 trial 原始分数（benchmark.json 仅 analysis/experiment/frozen_cases），方差只能核对 summary 不能独立重构
- 博客 "signal value"（accuracy×repeatability）为自定义指标，无外部参照
- Jev 三问判据文本与 LLM 提示措辞近似但非逐字相同（如 is_grounded 两版本措辞不同）——轻微不对称

## 案例区块

- 实践者与约束：LangChain 员工在自家平台（LangSmith/Gateway/Deep Agents）上比较四种 judge；观察仓库提交覆盖09-17→09-19；提交窗口不等于实验时长
- 具体做法：冻结 agent 输出→同 state 重放 100 次→案例内方差+oracle 一致率+成本延迟分报
- 报告的效果：Jev方差最低、binary全对、最便宜最快（作者自述，摘要关系已核，原始评分/账单未重算）；quality MAE 最差（归档数据，正文未讨论）
- 对我们的可复现性：可核方差比、逐例摘要加权到总体的关系（已做），不能独立重算逐trial估计量或账单；重跑需 TypeSafe/LangSmith/Gateway 密钥（本批不调用）；冻结重放+案例内方差+oracle 分报的方法可按任务和判据比较借鉴，不保证所有judge类型都适用同一标尺与 D10/D11 细则

## 适用条件与反证

- 适用条件：小语料（5 案例）、单评审员 oracle、单任务域（天气问答）、judge 版本部分不可见；数字描述本实验，不外推 judge 排名（README 自认）
- 反证/局限：
  - 作者自认：观察性结论、小语料、单评审员、非通用排名、低成本会放大错误 judge
  - 本批补充：公开附件有quality MAE/容差，正文未讨论连续刻度差异、Claude 零方差系统性错判、LLM judge 未确定化、营销定位草稿存在
  - 未核：SVG 图表数据、tests/ 目录、TypeSafe 文档侧的 200x/400x 主张（博客引用，未见原始）

## 与已有条目的关系

- M-069（Jev 访谈"开放生成与有限决策分开"）：本篇是该主张的首个量化工件，同时给出其边界（有限决策稳定≠连续分数贴近人工）
- M-083（LongJudge 评分器校准）：新增同类证据——评分器自身需校准且方差与准确性是独立维度；补充"零方差系统错"实例
- M-032/D10/D11：冻结重放+分报方差/准确率/成本的模板可入细则（judge 比较口径）
- 与 M-090 无直接关系（不同证据组）

## 后续动作

- [ ] 需要复现的主张：无（本批已复算归档内部关系；跨任务外推不立项）
- [ ] 需要补读的反方/正方：TypeSafe 对 200x/400x 主张的原始评测；第三方独立 judge 比较；tests/ 目录内容
- [ ] 复核触发器：Jev 或对比模型换代；LangChain 修订博客/README；独立复现出现；2027-01-20 前查新据

## 2026-10-16 主审裁决

补正Terra案例归属、Claude机制归因、原始复算范围和Noul机制推断；MAE/容差是作者公开归档统计，本轮仅核逐例加权与总体相符。成本表只核作者自述一致，未核原始收费分母/账单。营销定位草稿不证明造假，Gemini元数据不证明实际参评或选择性隐瞒。详见docs26及独立报告；旧稿原样归档。
