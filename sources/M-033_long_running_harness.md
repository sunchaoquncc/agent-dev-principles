# M-033 Effective Harnesses for Long-Running Agents（跨上下文窗口的 harness 设计）

> 当前用途（2026-10-14）：以下保留来源当时的做法与作者主张，仅作历史/自我修订对照；不将旧型号处方或旧“认可”记录作为现行要求。当前原则状态见[证据登记](../principles/07_evidence.md)，效果仍未验证。

> **2026-10-13审查勘误/适用范围（优先于下文历史解读）**：2025-11-26超6个月；JSON优于Markdown、固定仪式仅旧Claude生产经验，当前模型/任务须验证。

## 元信息

- 来源链接：https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- 原文快照（供复核）：http://web.archive.org/web/20261012070211/https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents（2026-10-12 捕获；检索日期 2026-10-13，本地抓取文本在案）
- 发布日期：2025-11-26
- 检索日期：2026-10-13
- 作者/机构：Justin Young（Anthropic）
- 适用模型：Claude 系（Opus 4.5 实证）；机制对长时程任务泛
- 证据等级：可检验结论（厂商工程实践+具名失败模式；内部实验自述，无第三方复现）
- 框架落点：harness 治理（跨会话结构）为主；上下文治理（状态外置）；评测（特征清单=内嵌回归测试）
- 关联条目：M-014（外部笔记+复述——本篇是其第三个实践语境）；M-004（增量推进）；M-010（compaction 局限的厂商自认）；M-024/M-032（特征清单=评测思想内嵌）；M-031（与 M-029 元脚手架互补的实现层）；Q-002（单 agent vs 多 agent 开放问题）

## 一句话结论

作者在当时跨窗口编码任务中发现单靠compaction不足，另加交接工件：初始化代理铺特征清单（JSON、全标 failing）+环境脚本，每个编码代理会话先读进度文件与 git log、先跑端到端测试再动新功能、一次只做一个特征、收尾留干净提交——把"换班失忆"变成"换班读交接文档"。

## 要点摘录（正文级精读，引文逐字取自当次抓取）

### 问题定义与 compaction 的不足

- 核心比喻："Imagine a software project staffed by engineers working in shifts, where each new engineer arrives with no memory of what happened on the previous shift."
- "However, compaction isn't sufficient."——即便 Opus 4.5 + Agent SDK 循环，只给高层 prompt（"build a clone of claude.ai"）做不出生产级应用。

### 两个具名失败模式

1. 一次做太多："the agent tended to try to do too much at once—essentially to attempt to one-shot the app"——上下文中途耗尽，"leaving the next session to start with a feature half-implemented and undocumented"。
2. 过早宣布完成："a later agent instance would look around, see that progress had been made, and declare the job done."

### 解法：双代理交接结构

- 结构："an initializer agent that sets up the environment on the first run, and a coding agent that is tasked with making incremental progress in every session, while leaving clear artifacts for the next session."
- 脚注澄清（方法论上重要）：两个"agent"仅初始用户提示不同——"The system prompt, set of tools, and overall agent harness was otherwise identical."（同一 harness 的两种会话角色，非多 agent 编排）
- 初始化产物：init.sh（起开发服务器）、claude-progress.txt（进度日志）、初始 git commit。

### 特征清单（把评测内嵌进 harness）

- 初始化代理把高层需求展开为特征文件——claude.ai 克隆例中"over 200 features"；全部初始标记 "passes": false，使后续会话"have a clear outline of what full functionality looked like"。
- **作者当时的JSON/Markdown改写观察**："the model is less likely to inappropriately change or overwrite JSON files compared to Markdown files."
- 强措辞护栏："It is unacceptable to remove or edit tests because this could lead to missing or buggy functionality."

### 增量推进与干净收尾

- "asked to work on only one feature at a time. This incremental approach turned out to be critical"。
- 干净状态的定义："the kind of code that would be appropriate for merging to a main branch: there are no major bugs, the code is orderly and well-documented"。
- git 双用途：描述性提交+进度文件；"use git to revert bad code changes and recover working states of the code base."

### 测试纪律（第三失败模式的对策）

- "Claude's tendency to mark a feature as complete without proper testing"——做了单测/curl 但 "but would fail recognize that the feature didn't work end-to-end"（原文如此，"fail recognize" 疑为作者笔误，语义=未能认识到功能端到端不工作）。
- 端到端验证靠浏览器自动化（Puppeteer MCP）"and do all testing as a human user would"。
- 工具边界：浏览器原生 alert 弹窗 Puppeteer MCP 看不见——"features relying on these modals tended to be buggier as a result."

### 会话启动仪式（复述机制的落地）

- 固定四步：pwd 定位 → 读 git log 与进度文件 → 读特征清单选最高优先级未完成项 → init.sh 起服务器并**先跑基础端到端测试**（原文："immediately fix any existing bugs. If the agent had instead started implementing a new feature, it would likely make the problem worse."）。

### 开放问题

- 单一通用编码 agent vs 专业化多 agent（testing/QA/cleanup）未决——Q-002 的厂商侧开放记录。

## 案例区块

- 实践者与约束：Anthropic 内部实验；Claude Agent SDK；全栈 web 应用开发域。
- 具体做法：见上（双代理+四件套产物+一次一特征）。
- 报告的效果：定性（两失败模式被抑制）；无量化对比数字（自述）。
- 对我们的可复现性：**高**——机制需要对应执行环境和工具；E-04仅测要求位置且有截断/评分限制，未验证复述或持久恢复；本设计可直接改造为 E-03/E-08 的实验骨架（长任务拆窗对照）。

## 适用条件与反证

- 适用条件：跨多上下文窗口的构建类任务（web app 实证）；单机文件系统友好域。
- 反证/局限：
  - 厂商语境（Claude Agent SDK + Puppeteer MCP 生态）；"200+ 特征"的初始化本身成本未报。
  - JSON 优于 Markdown 的主张是内部观察，无消融数据；适用性可能随模型对两种格式的改写倾向变化（复核触发器）。
  - 我方怀疑：特征清单粒度（200+）与真实需求漂移（需求中途变化）未讨论；"declare the job done"的对策依赖清单完备性。
  - 多 agent 开放问题自认未决。
- 与 Q-001 关系：compaction 不足的厂商自认（M-010 相邻）；但解法是**结构性交接**而非等待模型吸收——这是一类工程应对案例；METR历史时域不是对此机制的验证，也不能裁决Q-001。

## 与已有条目的关系

- **M-014**：第三个实践语境（Anthropic 工程实践，与 ECE 同厂商计 1 源；可加深案例理解，不增加独立来源数或现行验证等级）；新增机制细节：JSON 状态文件、启动四步仪式、先测后写。
- **M-010**："compaction isn't sufficient"的厂商直证——长时程三板斧中 compaction 单用不足。
- **M-004**：一次一特征的增量纪律是复杂度递增在会话内的微观版。
- **M-031/M-029**：实现层的配套（session 外置+接口化）。
- **Q-002**：开放问题记录（单一 vs 专业化多 agent）。
- 与 K-012 互证：行业调查里企业把大规模上下文工程列为痛点（K-012 填空回答：context engineering and managing context at scale），本篇是厂商侧答案之一。

## 后续动作

- [ ] 需要复现的主张：E-03 改造——用本篇骨架（progress+特征 JSON+先测后写）做有/无交接仪式的跨会话对照（glm-4-flash/deepseek 均可跑）。
- [ ] 需要补读的反方/正方：随附 quickstart 代码（结构细节）；Manus todo.md 与本模式的逐项对齐表（M-014 细则层）。
- [ ] 复核触发器：模型大版本（对 JSON/Markdown 改写倾向、端到端测试能力）；Puppeteer 类工具的弹窗可见性改进。


## 2026-10-14 正文一致性纠正

按既有docs08/总纲裁决及本篇内部证据限制，同步正文中的旧强断言、状态或阅读范围；未重抓来源、未新增效果验证。修改前文本见[_review_archive/2026-10-14-batch13/notes/M-033_long_running_harness.md](_review_archive/2026-10-14-batch13/notes/M-033_long_running_harness.md)，仅供历史追溯。
