# M-119 EvoTest：进化式测试时学习（摘要级·正文未取得）

## 元信息

- 来源链接：[ICLR 2026 Poster 10010217](https://iclr.cc/virtual/2026/poster/10010217)（OpenReview forum id=JFnnajbkvP）
- 原文快照：[_snapshots_local/batch17/evotest_iclr.html](_snapshots_local/batch17/evotest_iclr.html)，哈希见同名.pdf.json；正文 PDF 经 openreview.net/pdf 抓取返回 403，**全文未取得**。
- 发布日期：ICLR 2026（会议页面标注 2026 Poster；arXiv 版未检索）。
- 检索/审查日期：2026-11-21；验证日期：未复现。
- 适用模型：未在会议页摘要披露（正文未取得）；不设换代触发器直至全文可得。
- 作者/机构：Yufei He、Juncheng Liu 等8人 [外注：机构页面未列；NUS 归属系据作者谱系跨篇推断（Bryan Hooi 等），非本快照证据]。
- 阅读覆盖与媒介限制：**仅会议页摘要级**；UP主简介提及的"UCB平衡探索与复用""生成多套改进配置"细节在摘要中未出现，未核。
- 渠道路径：B站UP主09-08视频发现（docs/39 A15）。

## 一句话

提出 J-TTL 基准（同一游戏连续多 episode 测试时学习）与 EvoTest 框架：Actor 玩游戏 + Evolver 分析 episode transcript 后改写下一轮完整配置（prompt、记忆记录有效状态-动作、超参、工具例程），无梯度微调——超反思/记忆/在线微调基线，且是唯一赢下两局（Detective、Library）的方法。

## C1 来源记载（会议页摘要直述，evotest_iclr.txt L8-22）

- 动机：现有 agent 无法在测试时学习复杂技能，"behaving like 'clever but clueless interns' in novel environments"。
- J-TTL 基准：同一游戏连续 episode、要求跨 episode 提升。
- 发现：既有适配方法（reflection、memory、RL）在 J-TTL 上挣扎。
- EvoTest 双角色：Actor Agent 执行；Evolver Agent "analyzes the episode transcript to propose a revised configuration for the next run. This configuration rewrites the prompt, updates memory by logging effective state-action choices, tunes hyperparameters, and learns the tool-use routines."
- 结果：超反思与纯记忆基线及在线微调；"our method is the only one capable of winning two games (Detective and Library), while all baselines fail to win any."

## C3 我方推导与比较（摘要级）

1. 自进化线节点：改写对象是"完整 agentic system 配置"（prompt+memory+超参+工具例程）——介于 M-108（runtime 组件）与 M-117（自身代码）之间；Evolver 分析 transcript 的做法与 M-108 trajectory analyzer 同构。
2. "episode transcript 作为改进信号"与 M-103 dreaming（对照 transcript 修正）、M-118（决策历史）同主题：transcript 的价值在改进回路而非仅执行。

## C4 限制

- **仅摘要级，正文未取得（403）**；UP主补充细节（UCB、多套配置）未核；不引用正文级数字。

## C5 下次复核触发

- arXiv 版本可得或 403 解除时补全文精读。

## C6 来源去向

- 纳入知识库（A15，摘要级线索正式登记）；自进化线节点。

## C7 勘误与核对记录

- 2026-11-21：OpenReview PDF 403 已记录；不以后续检索摘要补写正文内容。
