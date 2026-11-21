# M-018 Amp《How to Build an Agent》

> 当前用途（2026-10-14）：以下保留来源当时的做法与作者主张，仅作历史/自我修订对照；不将旧型号处方或旧“认可”记录作为现行要求。当前原则状态见[证据登记](../principles/07_evidence.md)，效果仍未验证。

## 元信息

- 来源链接：https://ampcode.com/notes/how-to-build-an-agent（副题 "or: The Emperor Has No Clothes"）
- 原文快照（供复核）：https://web.archive.org/web/20261013061026/https://ampcode.com/notes/how-to-build-an-agent （SPA 页面，快照可能缺正文；机械校验未命中项以红队 2026-10-13 活页核验为准，见 _quote_check 日志）
- 发布日期：2025-04-15（页面标注 Thorsten Ball // April 15, 2025 ✅）
- 检索日期：2026-10-13
- 作者/机构：Thorsten Ball（Amp / Sourcegraph）
- 适用模型：Claude 3.7 Sonnet（原文点名；工具设计经验绑定该模型，"换模型试试"为作者原话的随意建议）
- 证据等级：经验断言（可检验性极高——全部代码可下载复现，但本文未附评测）
- 框架落点：harness 治理（agent 循环、工具定义）为主；prompt 治理（工具描述写法）
- 关联条目：M-004、M-006、M-023；K-001；Q-001
- 备注：docs/02 记录的配套 HN 讨论 ID 43992114 经 2026-10-13 核实**与本文无关**（指向无关评论串），已记冲突并从信源清单移除；真实 HN 讨论串待重新定位（Algolia API 当日不可用）。

## 一句话结论

作者用不到400行代码演示编码Agent的内循环；这说明一个简化演示可由模型、工具和循环组成，不说明生产系统全部复杂度只有这些。

## 要点摘录

（引号内为原文逐字引文。）

- 主张："It's not that hard to build a fully functioning, code-editing agent"；全部要素："It's an LLM, a loop, and enough tokens."
- agent 定义（本文版）："an LLM with access to tools, giving it the ability to modify something outside the context window"——LLM 借工具获得修改上下文窗口之外世界的能力。
- 实现拆解（code-editing agent）：
  - 工具四件套：get_files（读目录）、read_file、create_file、string_replacement（编辑）；
  - 工具定义="名称+描述+输入 schema+函数"（"a model's tool definitions... are equivalent to function signatures"——同构于函数签名）；
  - 循环：系统提示→LLM 输出 tool call→执行→结果回填→继续，直到 LLM 停止（模型在循环中跑：LLM 输出→执行工具→LLM 继续）；
- 关键工程发现（原文自述"试出来的"）：
  - "Claude 3.7 loves replacing strings"——字符串替换式编辑对该模型特别有效（发现方式：实验，不是理论）；作者对此的注解是随意的"try other models"。
  - 工具输出格式不重要、但需实验确认："Anything goes as long as Claude can make sense of it and whether it can you need to figure out by experimentation."
  - 工具描述的写法：给模型能理解的自然语言描述即可，不需要给"AI 特殊格式"。
- 界限声明："This is essentially all there is to the inner loop of a code-editing agent"；剩下的（语言检测、多文件 PR、lint 集成等）是"practical engineering and elbow grease"。
- 立场：全文是对 agent 框架/中间件的祛魅（"皇帝没穿衣服"）——内核极小，复杂性在工程细节而非架构神秘感。

## 案例区块

- 实践者与约束：Amp/Sourcegraph（生产级编码 agent 厂商）；演示目标是"最小可运行"，非生产配置。
- 具体做法：<400 行 Go；四工具；固定系统提示。
- 报告的效果：可完成代码编辑任务的演示（作者自述，附完整源码可复现）；无基准数字。
- 对我们的可复现性：**本批最高**——源码可下载，可用本地任意模型 API 重跑（E-08 候选：400 行 agent 复刻+换模型对比工具偏好，验证"Claude 3.7 loves replacing strings"是否模型特异）。

## 适用条件与反证

- 适用条件：编码类单 agent；Claude 3.7 系（工具偏好经验绑定单一模型）；演示级而非生产级（生产要加沙箱、错误恢复、上下文管理等——正是第一批笔记的内容）。
- 反证/局限：
  - 作者自认：只是 inner loop，生产化的其余部分一句带过。
  - 我方怀疑：样本量为 1 个模型的行为经验；"400 行"不含它引而不谈的生产复杂度——与 BEA/Manus/ECE 的治理内容不冲突，恰是 M-004 的最底层档位证据。
- 与 Q-001 的关系：可作简化内循环的历史案例；框架或工程层是否被模型吸收不是本文测得的结论。

## 与已有条目的关系

- 为M-004提供简化实现案例；与BEA/OpenAI为相邻经验，旧“升认可”记录不代表现行效果验证。单次调用与单Agent循环也不是同一复杂度档位。
- K-001（agent 定义收敛）的独立第二/三源："LLM with access to tools"+"loop" 与 BEA/ECE/OpenAI 表述同构。
- 与 M-006（ACI）：工具定义=函数签名的同构观 + "工具描述给模型能懂的自然语言" + 输出格式需实验确定——ACI 的实践派版本（无 SWE-agent 的理论化）。

## 后续动作

- [ ] 需要复现的主张：E-08（400 行 agent 复刻 + 跨模型工具偏好对比）。
- [ ] 需要补读的反方/正方：Amp 其他 notes（evals 相关）；HN 真实讨论串（定位后作红队）。
- [ ] 复核触发器：模型大版本（工具偏好经验随版本变化——作者自己都说"try other models"）；6 个月例行。


## 2026-10-14 正文一致性纠正

按既有docs08/总纲裁决及本篇内部证据限制，同步正文中的旧强断言、状态或阅读范围；未重抓来源、未新增效果验证。修改前文本见[_review_archive/2026-10-14-batch13/notes/M-018_amp_how_to_build_agent.md](_review_archive/2026-10-14-batch13/notes/M-018_amp_how_to_build_agent.md)，仅供历史追溯。
