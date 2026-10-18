# 项目 E 已有纠错案例：两处纯社保正文被改成公积金流程后，正确删除修订如何被挡住

整理日期：2026-10-18（北京时间）。整理人：本项目开发助手。只整理既有文件、历史函数输入输出、保存回读、版本快照和测试回执；首次整理没有执行产品代码、测试、模型/API 调用或生产工具，也没有修改产品。

转交说明：首次交付后，用户明确授权将这一材料包移入 `D:/Project/agent-dev-principles` 并增量推送 GitHub。本次转交以知识库远端最新提交 `97f8269f64e50ee10cf530d168d367e3eb7a24da`（v0.18）为基线，仅新增本目录；现有原则、原报告及发布清单沿 Git 最新版本保留。文中历史版本和首次整理的证据边界不变。

**可成立的小结论：**真实 T161 记录中，Main 曾把两处纯社保正文改成公积金业务，随后提出删除修订。旧运行先隐藏纠错工具，再拒绝“共同合同＋两项修订”，最终保存了旧错误改法。历史离线重放使用这组实际参数，在重建的起始状态下，A 不更新判断并拒绝混合合同，候选接纳，断言两项改法替换、另46项改法字段保持。它证明一个有界机制改善，不能作为完整运行已修好或正文业务通过的证据。

本包同时保留反证：后续 **R1 真实整案仍有一次纠错工具不可用**；A/R1 整案均未业务通过；R1.1 只有离线验证。原反馈的主要数字有历史依据，但“同参数”的状态条件、“46项保持”的字段范围和“旧计划退出”的证据来源需要补清。

## 1. 问题、用户目标与版本

原客户目标为：

> 不需要包含社会保险，不需要包含招聘

隔离测试清单中的实际请求为上述原话加一行既定确认：

> 用户已确认：连同社保责任、工资扣缴说明一起删除。

任务是修改正文，保留目录及其他独立内容。这里需要删除的是本节原有的社保业务，不授权把它换成新公积金业务；其他小节本来存在的公积金独立义务仍应保留。本案依据两节完整原文及当时修订理由作此判断，不把客户删除要求解释为法律建议。

原任务源 CID：`94ca37cfa64746f4965791174b87059a`；真实错误轨迹的 TEST CID：`da86ed863b8444e9abf2498a6746f11b`。请求摘录在 [原请求与两节完整正文](01-original-trace/two-bodies-and-requests.json)。省略了无关客户材料、其他47个候选的长正文、模型内部思考、账号凭据；其余候选的判断及改法保留在清单中。

| 名称 | 准确含义 | 证据与边界 |
| --- | --- | --- |
| 原错误轨迹 D | 前一轮 T161 真实隔离 TEST，运行标签 `c793d10b + P1.1 + P2 deletion contract` | 是修订参数来源；不是后续 A 或候选的同一次运行 |
| A | `c793d10b9c983ccaf2ed757b482d45cd138c8fd7` 加当时18项既有工作区变更，封存在 `baseline.tar.gz` | 不是裸 Git 提交，也不是生产冻结版；18项清单附于 [BASELINE.json](02-offline-replay/BASELINE.json) |
| R1 | `candidate-R1.tar.gz`，在 A 上加入完成审查后的改判、混合合同承接及冻结后局部修订 | 后续真实整案 B 的 `sourceLabel` 指向此包；也有 R1 阶段离线接纳回执 |
| R1.1 中间版 | `candidate-R1.1.tar.gz` | 增补遗漏目标保护等；仍非最终包，不能与 R1 整案合称 |
| R1.1 最终版 | `candidate-R1.1-final.tar.gz` | 补齐共享选择形式下的目标遗漏保护和恢复说明；有离线测试，未再完整保存实跑 |
| 本次读取的工作区 | HEAD `a6036f63c4fa6c72fbc043bf34dee003600b3f39` | 本次静态比较的4个纠错实现文件及1个测试文件，与 R1.1 最终快照相同；未声称整个仓库或运行配置相同 |

快照、标签及当前文件比较见 [版本边界](03-implementation-and-tests/version-boundaries.json)。两段相关差异见 [A→R1](03-implementation-and-tests/A-to-R1.patch)、[R1→R1.1最终版](03-implementation-and-tests/R1-to-R1.1-final.patch)。后续提交 `b23b525c` 汇入过这些修复及其他材料交接改动，不能把该提交整体当作当时单一候选。

原反馈按用户指定提交 `4c19244f03f872c911428d7e05dae073b9a1ac71` 直接从本地知识库 Git 对象导出，附 [原报告](00-published-report/2026-10-18-project-e-decision-changes-and-limits.md) 和 [原证据摘要](00-published-report/2026-10-18-project-e-evidence.json)，没有改写或发布它们。

## 2. 两项对象、实际请求与起始状态

全部候选共有 **49项：48项 repair、1项 preserve**；“48项”指写入目标，不是候选总数。三组审查提交为17、16、16项，最后一组返回完成。另46项仍需按原改法处理，“保持”不是46节不写入。

| 对象 | 社保停保执行流程 | 社保参保完整性评估 |
| --- | --- | --- |
| 原目录路径 | 第二章 质量保证与售后服务等服务承诺 / 第七节 工龄管控与人员流动管理服务承诺 / 四、未达标人员分流安置 / （四）社保停保执行流程 | 第三章 证据链与合规保障方案 / 第五节 劳动争议处置方案 / 一、争议预警机制 / （四）社保参保完整性评估 |
| 真实句柄 | `rewrite-candidate:914d6dcadd48c083f4948f8b` | `rewrite-candidate:f8fa7abca0291e03573edee9` |
| 原节点 ID | `6ad19ee5a5906b647c75e3c7` | `6ad19ee4a5906b647c75e385` |
| D 副本节点 ID | `6ad455112648c2c609d3ded8` | `6ad455112648c2c609d3dec8` |
| 原正文版本 | `V20261016_1792122814387` | `V20261016_1792122814299` |
| 原判断 | 整节社保停保流程；因其他节保留公积金，本节也改为公积金停缴 | 整节社保参保评估；改为公积金缴存完整性评估 |
| 旧改法原文摘录 | “将本节停保条件、停保操作、停保记录整体改为公积金停缴流程” | “将评估范围、评估指标、补救措施整体改为公积金缴存完整性评估” |
| 后来明确修订 | 删除本节全部目标正文和表格，不新增公积金停缴等替代业务 | 删除本节全部评估正文、核查表及填表说明，不新增替代业务 |

这两节完整原文分别只涉及社保停保和社保参保核查。把“其他小节有公积金义务”推成“这两节也应新增公积金流程”，超出了删除目标。原判断、完整新参数及版本/hash都随包保留，不依靠本表重建输入。

**同一修订意图实际走了两步，不能合并成一次两项分组调用：**

1. `review_recall_candidate_group`：沿原 `group_id=recall-group:cf53a086d75aa77839bc`，只提交“停保执行流程”这 **1项**完整新判断。`decision=repair`、`preserveFacts=[]`，具体改法为删除整节目标正文，不换主题。
2. 补读两节完整正文后，调用 `record_rewrite_problem_set`：`sharedProblem` 提交全任务共同来源/保护边界，`problems` 显式列出上述 **2项**完整修订合同，各自 `preserveFacts=[]`、`basisRoute=body_dirty_basis_clean`，禁止新增替代业务；另46项应沿此前已审改法承接。

第二步两项 `expectedChange` 原文：

> 删除本节全部正文（停保条件、停保操作、停保记录表及表格内容），本节不再保留社保停保流程及相关表格文字。

> 删除本节全部正文（评估范围、评估指标、补救措施、参保核查表及填表说明），本节不再保留社保参保评估内容。

D 中提出这两步修订时，审查已完成，**尚未冻结 ProblemSet、绑定可执行计划或派发写入**。前面的 planning_only 登记只是目标范围。其后才有冻结、计划、`section_rewrite`。没有“部分已经写入后覆盖旧事实”的实际场景。

## 3. 实际前后记录与后续状态

### 3.1 原真实轨迹 D：正确修订被挡，旧错误进入保存

以下时间均已由原 UTC 加8小时，原始时间仍在 JSON 中。行号指原 `runs/editpro-priority-fixes-20261018/evidence/D/state/sdk-traces.private.jsonl`，必要输入输出已装入 [函数事件片段](01-original-trace/function-events.json)。

| 时间 | 原行 | 真实动作及返回 | 随后发生什么 |
| --- | --- | --- | --- |
| 13:14:07 | 84 | 最后一组审查 `complete=true` | 49候选完成，48 repair；旧两项均为公积金改法 |
| 13:14:31 | 94 | 分组修订被 SDK 替换成 `_editpro_rejected_call`；`tool_not_available_this_step`、`executed=false` | 修订没有执行，不能解释为模型始终未发现错误 |
| 13:14:33 | 104 | 补读两节全文成功 | 模型随后提交两项明确删除合同 |
| 13:14:47 | 114 | 混合合同被拒：`rewrite_problem_review_scope_conflict` | 恢复指引要求去掉显式 problems，只保留共同合同 |
| 13:14:52 | 124 | 按指引去掉两项显式修订，冻结48项成功 | 旧逐节改法成为实际合同；`newPlanRequired=true` |
| 13:14:59 | 134 | 新可执行计划通过，`boundToTransaction=true` | 开始执行的是旧合同，不是此前被拒的新删除合同 |
| 13:15:03 | 144 | `section_rewrite`，返回 running | 后续真实保存；终态 `needs_review`、`terminal=true`、后台静止 |

拒绝恢复原文关键句是：“去掉显式 problems，只保留一个……sharedProblem”。这会撤掉本次需要保留的局部修订。静态核对也确认 D 最后冻结48项的 `expectedChange` **全部仍等于原审查记录**。

保存结果能直接看到因果终点：

- 停保执行流程保存为 `V20261018_1792300728`，出现“我方将严格执行住房公积金停缴政策”等完整新公积金流程。
- 参保完整性评估保存为 `V20261018_1792300701`，出现“确保每位员工均纳入公积金缴存体系”等新公积金评估。

见 [D 四处选定正文前后](04-real-whole-task/D-selected-bodies.json)、[D 保存回读及终态](04-real-whole-task/D-status-and-readbacks.json)，对应实际回读 HTML 也在 `04-real-whole-task/D/saved-html/`。这部分有真实模型工具调用和业务保存产物，支持“正确修订被挡后旧错误落地”。它本身不证明候选已修好。

### 3.2 A 与候选：历史离线重放的实际结果

当时已有脚本 [replay_original_correction.py](02-offline-replay/replay_original_correction.py) 从 D 的原请求提取参数；本次只复制和阅读，没有再次执行。

| 项目 | A 已有结果 | 候选已有结果 |
| --- | --- | --- |
| 分组改判 | `correctionAcknowledged=true`、`alreadyComplete=true`、`actualDecisionChanged=false` | `realPreviouslyRejectedGroupCorrectionAccepted=true` |
| 共同合同＋2项修订 | `finalCorrectionRejected=true`，原因 `rewrite_problem_review_scope_conflict` | `realPreviouslyRejectedTwoFinalCorrectionsAccepted=true` |
| 目标数及改法 | 旧判断不更新 | `repairTargetsRetained=48`、`correctedTargets=2`、`other46ExpectedChangesUnchanged=true` |
| 去除旧替代业务 | 未取得新合同 | `oldRetargetingNotInCorrectedContracts=true`；脚本具体检查两项改法中不再有“公积金” |
| 后续状态 | 脚本结束，无派发、保存 | 同左；没有实际新计划和正文产物 |

上表为当时脚本的**真实历史输出字段**，不是本次生成的 A/B 输出。原结果文件见 [A 回执](02-offline-replay/ORIGINAL-CORRECTION-BASELINE.json)、[候选回执](02-offline-replay/ORIGINAL-CORRECTION-REPLAY.json)。历史终端记录也独立找回：16:11:42 有早期候选成功输出；16:40:45 有 A 输出；16:41:10 有后来候选输出，均见 [原命令与 stdout](03-implementation-and-tests/historical-commands-and-stdout.json)。默认脚本导入的是当时工作区，后一次属于 R1.1 阶段；并非每次都由归档包直接启动，不能把后一次输出倒称 R1 整案结果。

**输入相同的范围及实际差异：**A/候选重放用同一脚本、同一 D 请求、判断和版本/hash来源，但原运行状态被脚本重建。脚本显式设置 `complete=True`、`mainReviewRequired=True`，以49项历史判断构造审查；组内候选正文列表为空，从后来的冻结事务补48项版本/hash，使用 `SimpleNamespace` 和空结构上下文；把原扁平改法另放入 `nodeEdit`。它直接调用 `apply_recall_group_review` 与 `expand_shared_problem_contracts`，没有走原 SDK 可用性检查、完整 handler、执行计划或 Java 保存。

因此可以称为 **同实际修订参数、同重建状态的离线函数对照**；不能称为同一实时状态、同一 SDK 完整链路的严格 A/B。它也不是完全合成的业务输入；真实请求与判断来自 D，测试上下文由脚本组装。详细变换见 [重放起点说明](02-offline-replay/reconstructed-input-notes.json)。

候选展开后的48项完整合同当时没有独立保存到结果文件；现有的是脚本断言、实际 stdout和汇总回执。本次没有补跑生成一份合同冒充历史输出。

### 3.3 后来的 A/R1 完整任务：有保存，仍不通过

两臂从同一 T161 原材料生成新 TEST 副本，请求清单原文相同。选出的四个节点已按原节点 ID 静态核对，起始正文相同；不据此宣称全仓、整段模型历史或运行中间状态完全一致。

| 指标 | A 真实整案 | B＝R1 真实整案 |
| --- | --- | --- |
| TEST CID | `55a52a4e6205423e94bb7d1084475af9` | `4809d87e11de4f56b29483e3591a4663` |
| 有效正文 / 保存节数 | 249 / 49，历史回读均 exactEqual | 249 / 46，历史回读均 exactEqual |
| 两处纯社保正文 | 清掉业务文字，留下空表结构 | 清掉主要业务内容，仍留“1.停保条件、2.停保操作、3.停保记录”等小标题和空表 |
| 独立公积金义务 | 劳动合同第6条公积金缴纳义务被一起删去 | 第6条保住；“离职手续规范性检测”中的公积金停缴义务仍被一起删去 |
| 最终状态 | `needs_review`、terminal、后台静止；业务未通过 | 同左 |
| 额外交互 | 无该次确认 | 一次保留小节/删除目录选择，由 TEST 操作员按既定正文范围选择 `keep_sections` |

**额外反证：**R1 的 `state/sdk-traces.private.jsonl:149` 中，另一次完成审查后的5项修订（包括两处纯社保节的对应副本）仍被 `_editpro_rejected_call` 拒绝，原因也是 `tool_not_available_this_step`。见 [R1 实际拒绝输入输出](04-real-whole-task/R1-correction-still-rejected.json)。它不是上述 D 参数的同一句柄对照，起点还受确认恢复影响；足以限制“R1 已消除所有此类拒绝”的表述，**具体残余原因本次未核定**。

操作员续请求为“保留小节，只删节内社保内容。”，不是原客户新增答复。故后续真实 A/R1 比较存在额外输入、目标取舍、模型波动等差异，不是严格同输入质量/性能对照。完整确认卡及请求日志摘录随包附上。

两处在 A 也消除了主要业务文字，不能独占归因于 R1；R1 保留了小标题和表格，也不能写成“全部正文已是空文本”。本案候选合同要求与真实落地是两层证据。

## 4. 改动与验收依据：逐项说明证明到哪里

### 4.1 相关实现

A 在审查完成时直接返回已完成，不更新原决定；原混合合同校验把显式两项与已审目标视为冲突。R1 接入有界修订：

```diff
- return not review_manifest_completion_valid(review)
+ return (not _body_contract_execution_started(run_context.context)
+         and not active_rewrite_problem_transaction(run_context.context))
```

这是 `sdk_tools.py` 中 `mainReviewRequired` 分支的可用性改动，不能外推覆盖所有状态路径。混合合同承接按句柄覆盖指定改法，其他项取原已审记录；新修订先在临时状态完整校验，成功后才更新被改目标。冻结后的修订以当前冻结合同为原集合；R1.1 再补“没交代其余旧目标去向就拒绝”的保护。相关全段差异和最终修订模块已附，未拷贝整个仓库。

旧计划退出沿用原冻结 handler 的计划绑定检查和 `_invalidate_stale_problem_transaction_plan`，见 [原实现片段](03-implementation-and-tests/plan-invalidation-source.txt)。静态源码只用于解释机制，不算运行通过。

### 4.2 必查项与证据等级

| 核查问题 | 实际依据 | 可以确认 / 缺口 |
| --- | --- | --- |
| 2项怎样变 | D 原审查及修订全文；历史重放循环断言候选 `expectedChange` 等于显式两项，且不含“公积金” | 证明新合同改法接纳；缺展开后48项合同的独立历史快照，不能逐字段复核候选所有输出 |
| 其余46项怎样保持 | 历史重放对每个非修订项逐一比较原 `expectedChange`；合成48项测试另比较未改项完整 `dispositionRecords` | 真实参数重放只核改法字段；不能把保护事实、所有元数据、正文或全部运行状态都称为保持 |
| 旧计划/执行绑定退出 | 合成2目标的真实 SDK handler 测试先冻结、绑定旧计划，再修订；断言 superseded、newPlanRequired、active_task_action_plan 清空，且无 changed_node_ids | 证明该夹具内旧计划退出、尚无正文写入；原48项重放未种入旧计划，没有该次退出历史输出 |
| 下游使用新改法 | 同一合成 handler 测试构造编辑指令，断言含新改法与另一个原目标改法、不含第一项旧改法 | 是合成调用下的指令证据；不是上述48项实际发送给 Java 的新合同 |
| 修订失败不污染 | 重复句柄、未知句柄、改法缺失测试比较整个原依赖状态；冻结后遗漏目标拒绝测试比较原事务，handler还检查旧计划仍在 | 合成失败场景有测试定义及所在套件实际通过输出；未取得原48项真实非法修订前后完整状态快照 |
| 已派发后保护 | 合成测试设置 content_generation_started，SDK handler 返回 recall_revision_execution_started，原依赖状态相同 | 该测试保护已执行标志；本案实际修订发生在派发前，没有部分执行实案对照 |

### 4.3 一条有历史运行输出的针对性测试

`test_actual_final_contract_revision_keeps_second_target_and_invalidates_bound_plan` 是**合成测试**，名字中的 actual 表示调用真实 handler，不表示输入来自真实用户。完整定义见 [最终快照测试文件](03-implementation-and-tests/test_prewrite_review_revision.R1.1-final.py)，输入夹具定义见 [夹具片段](03-implementation-and-tests/synthetic-fixture-inputs.txt)。

其输入为夹具创建的两个节点，先给第一处设旧改法“第一处按旧决定保留专属办理流程”，冻结并绑定 `plan_id=before`；非法共享选择只列第一处时应拒绝，原合同与旧计划保持；合法修订用不带选择范围的共同合同＋第一项补丁：

```python
patch = {**_shared_contract(candidateHandle=first["candidateHandle"]),
         "expectedChange": "删除指定目标文字，保持其余内容",
         "preserveFacts": ["原有人员和面积"]}
```

关键断言（测试原文摘录）：

```python
assert revised["ok"] and revised["superseded"] and revised["newPlanRequired"]
assert not ctx.active_task_action_plan and not ctx.changed_node_ids
assert by_handle[second["candidateHandle"]]["expectedChange"] == second["expectedChange"]
assert patch["expectedChange"] in instruction
assert second["expectedChange"] in instruction
assert first["expectedChange"] not in instruction
```

历史命令包含此测试文件及另5个相关文件；2026-10-18 **16:45:36** 取回的终端输出为：

```text
134 passed, 1 warning in 7.71s
```

这是本次从旧 Codex 会话原 tool output 中找回的实际输出，不是重跑结果。此前16:40另有 `134 passed, 1 warning in 8.21s`，未重复计数。warning 为 dateutil 使用过期 UTC 时间接口。命令、退出码0、原会话路径与行号（最终输出9581）均附于原命令/stdout文件。

输出使用 `-q`，没有逐测试 verbose 回执；因此可说明这份文件在通过套件中，不能冒称取得每条断言独立日志。本次没有执行它来补验。134含其他机制，不能单凭总数证明本案每项业务目标。

## 5. 结论、原反馈修正和成本边界

可以保留：D 中存在真实正确纠错意图及机制拒绝，错误旧改法实际落地；历史函数对照支持指定条件下“修2项、另46项改法字段不动”；合成 SDK 测试支持旧计划失效、失败保护及编辑指令承接。R1.1 最终补充没有完整业务重跑。

原反馈无需撤销“48/2/46”数字或“134通过”，但应补充以下限定，避免扩大结论：

1. “同参数对照”应明确为**真实参数＋重建状态的离线函数对照**。原真实运行是 SDK 拒绝，A 的 alreadyComplete 是直接函数输出，不是同一个完整入口的返回。
2. “46项保持”在真实参数重放中只逐项核对改法 `expectedChange`；更广的状态保持主要来自合成测试。
3. “旧计划失效”及“对应编辑指令只用新改法”有合成2目标 handler 测试依据；没有取得同48项重放中的原计划、失效和发送新指令的完整历史链。
4. R1 真实整案仍有一次相同原因的工具拒绝，不能概括为所有未执行纠错路径已修；本次不进一步诊断或开发。
5. 两处纯目标内容在 A/R1 整案都曾被删除到只剩结构，R1还留小标题。不能称候选独有业务收益或字面“整节已完全空白”。

完整任务失败边界保持：A 误删原有公积金缴纳义务；R1 在离职手续仍误删公积金停缴义务。它们是本次真实同源正文片段可见的业务错误，不拿后台完成、保存成功或测试总数替代业务通过。

历史已有成本见随包 `COMPARISON.historical.json` 和原报告：A 到后台终态约762.683秒，Sidecar估算0.945871元；R1两次请求处理合计约829.819秒，含等待确认总历时约1075.142秒，Sidecar估算1.633912元。R1额外确认计入负担，续请求单独 HTTP 耗时漏记；Java模型费、开发助手费用、人工用时未知。这里只引用当时费率和 usage 的估算，不核当前价格、不称账单，也不声称降本。离线重放没有模型调用；本次整理新增模型/API调用为0，整理工时及本开发会话费用未单独计量。

**剩余缺口就此交付：**候选展开后48项完整合同的独立原输出；同48项带旧计划和失败污染的完整状态对照；真实 R1 残余拒绝的确切起因；逐测试 verbose 输出；R1.1 完整正文重跑。均未取得，不用静态阅读或新生成结果替代历史运行。现有材料已足以核查这个窄结论，本次不补跑、不新建开发项目。

## 6. 可转交材料清单与原位置

下表中的**包内路径**均随目录一起交付；原路径用于溯源，不要求维护者能读取本机。原项目根为 `D:/Project/bid-agent-sidecar-develop/`，下文原项目路径相对该根。历史会话根为 `C:/Users/45465/.codex/sessions/2026/10/17/`。

| 材料（包内路径） | 原路径/版本 | 实际内容范围 | 支持的判断 | 缺失项 |
| --- | --- | --- | --- | --- |
| `00-published-report/` 两份报告及 provenance | `D:/Project/agent-dev-principles`；提交 `4c19244…` 的 `trial/feedback/2026-10-18-project-e-*` | 原报告及证据JSON，逐字导出 | 明确待核原反馈，没有事后改报告 | 不含知识库全仓 |
| `01-original-trace/function-events.json` | `runs/editpro-priority-fixes-20261018/evidence/D/state/sdk-traces.private.jsonl:64,74,84,94,104,114,124,134,144` | 三组完整判断输入；拒绝、补读、冻结、计划、派发片段；保留时间与原行号 | 先修订被拒，后沿旧合同派发的因果顺序 | 省略长投影、其他函数、模型内部思考 |
| `01-original-trace/two-bodies-and-requests.json` | 同 D 清单；上述 trace 74/84/94/104/114 | 两节完整原文、旧判断、1项分组修订、2项最终修订及共同合同 | 原业务问题、实际参数与身份 | 不复制其他候选长正文 |
| `01-original-trace/48-targets-and-one-preserve.json` | 同 D trace；`state/continuations/editpro-generation-task-da86ed863b8444e9abf2498a6746f11b-efedface6eb5-b5cb3b9eec3da452.json` 的 transaction | 48项句柄/节点/版本/hash/原改法/冻结改法，另1项保留 | 49候选与48写入目标分清；D最终48项沿原改法 | 不是候选重放展开输出 |
| `02-offline-replay/` 两份结果、原脚本、BASELINE与起点说明 | `runs/editpro-prewrite-revision-20261018/` 同名文件；当时A/候选工作区 | 原脚本和已有汇总回执，另附本次静态起点说明 | 指定参数接纳、2/46改法断言及离线边界 | 展开后的完整候选合同未留存 |
| `03-implementation-and-tests/A-to-R1.patch`、`R1-to-R1.1-final.patch`、版本JSON | 同 run 的 baseline/R1/R1.1最终 tar；当前 HEAD `a6036f63…` | 只比较4个纠错实现文件及1个测试文件 | 实际改动、版本增量与工作区关系 | 不代表完整运行版本相等 |
| `03-implementation-and-tests/` 最终测试、修订模块、夹具及计划退出片段 | `candidate-R1.1-final.tar.gz!` 相应源码与测试 | 合成48目标、合成2目标handler、非法/执行保护定义 | 哪条断言负责哪种机制 | 这些副本是定义，不是本次运行输出；不是独立可运行整套环境 |
| `03-implementation-and-tests/historical-commands-and-stdout.json` | 会话 `rollout-2026-10-17T00-21-24-01a143e0-5e5a-78d2-b0ad-d95aa9944934_01a14584-a882-7d62-95c1-c07d8aaafc82.jsonl`；9111/9504/9513/9581及9501/9577 | 实际历史stdout、命令、时间、退出码及源行号；无模型内部思考 | A/候选回执确有历史输出；134套件通过 | 无逐测试verbose、无每条断言独立日志 |
| `04-real-whole-task/{D,A,R1}-selected-bodies.json` 与各臂 `saved-html/` | D原run及后续run `evidence/{A,B}/T161/all-body-comparison.private.json` 和回读HTML | 每臂只取两纯社保节、劳动合同、离职手续共4处完整前后文本；12份保存回读HTML | D错误落地、A/R1两处删除及独立义务误删 | 不提供249节全文，也不声称全量人工复审 |
| `04-real-whole-task/*-status-and-readbacks.json`、请求摘录、R1确认与拒绝 | 对应各臂 runtime、清单、saved-readbacks、background-status、request-journal；R1 trace149 | 选定回读、保存总数、后台终态、请求确认、真实拒绝参数 | 实际运行身份、额外交互、仍失败及残余拒绝 | 不核定R1拒绝根因；无新查询 |
| `04-real-whole-task/COMPARISON.historical.json`、`RESULT.historical.md` | 原纠错run同名文件 | 原有完整阶段摘要及既有成本，不是本次重新运行结果 | 保留整案失败、R1.1离线及成本边界 | 原摘要中宽泛表述以本报告限定解释 |
| `05-static-audit.json` | 本次静态读取已有文件 | 计数、四节点同源正文、5文件与最终快照比较 | 新整理与历史运行分离，材料对应可核对 | 不构成产品运行通过 |

正文中的真实字段、业务原文与保存版本均按用户要求保留；与本案无关的凭据未带出。整个目录可转交维护者离线阅读，主文件和所有相对链接所需材料均在包中。
