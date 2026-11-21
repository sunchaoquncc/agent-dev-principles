# M-114 LLM-as-a-Verifier：验证作为新的可扩展计算轴

## 元信息

- 来源链接：[arXiv:2607.05391v2](https://arxiv.org/abs/2607.05391)
- 原文快照：[_snapshots_local/batch17/llm_verifier.pdf](_snapshots_local/batch17/llm_verifier.pdf)，哈希见同名.pdf.json；pypdf提取txt（31页，行号以txt计）。
- 发布日期：v2 2026-07-07（v1 2026-06；约4.5个月前，窗口内）。
- 检索/审查日期：2026-11-21；验证日期：未复现。
- 作者/机构：Jacky Kwok、Shulu Li 等，含 Chelsea Finn、Ion Stoica、Azalia Mirhoseini / 斯坦福、UC Berkeley、NVIDIA Research。
- 适用模型：被验候选 GPT-5.5（主）；verifier Gemini 2.5 Flash（L530）；对照 Opus 4.7、Gemini 3.1 Pro。下一代模型发布触发复核。
- 来源类型与利益关系：预印本；学术为主。
- 阅读覆盖与媒介限制：摘要/图1/关键数字定位段精读（L461-532）；方法细节与全部表格未逐项核——**摘要级+定位段精读**。
- 渠道路径：B站UP主08-26视频发现（docs/39 A12）；内容取自论文原文。UP主转述的平局率 26.7%、83.1%/86.5%/92.1% 与正文一致（已核）。

## 一句话

把"验证"确立为独立于预训练/后训练/测试时的第四条 scaling 轴：不用离散分数而取评分 token logits 分布的期望得连续分，沿粒度/重复评估/标准分解三个方向扩展验证计算——在 Terminal-Bench V2 等四域取得 SOTA，并给出省成本的排序算法。

## C1 来源记载（摘要+定位段直述）

- 命题：verification 是新 scaling 轴（摘要）；与标准 LM judge 的区别："computes the expectation over the distribution of scoring token logits to generate continuous scores"——离散评分在复杂解比较时大量平局（"tie rates"），连续概率分显著降低。
- 三扩展维度：score granularity（粒度越细正负解分离越好、比较更校准）、repeated evaluation（方差缩减）、criteria decomposition（复杂度缩减）。
- 关键数字：离散步进下 k=1 平局率 26.7% → **k=16 次重复评估下 5.5%（"as averaging breaks ties"，机制为重复评估取平均破平局，非粒度细化；L468-472）**；Terminal-Bench V2：GPT-5.5 Pass@1 83.1%、oracle Pass@5 上界 92.1%、LLM-as-a-Verifier 从候选池选出 86.5%（L522-532），超其他配置（Claude Mythos+Terminus-2 82.0% 等）；SWE-Bench Verified 78.2%、RoboRewardBench 87.4%、MedAgentBench 73.3%（图1）。
- 排序算法：Probabilistic Pivot Tournament——用偏好概率做预算高效的最优候选选取（摘要"cost-efficient ranking"）。
- 附加（摘要两处分开登记）：细粒度信号"can also serve as a proxy for estimating task progress"（摘要倒数第三句）；末句称可用作"dense reward signal for RL"，提升 SAC 与 GRPO 的样本效率（未展开读）。

## C3 我方推导与比较（工作草案）

1. **评测横切的新轴**：项目已有"评测=可度量"横切，本篇给"验证计算本身可扩展"的实证——与 M-108（LLM 生成测试）互补：M-108 解决"验证器形态"（生成测试 vs 判轨迹），本篇解决"评分粒度"（连续 vs 离散）——两者正交，共同支撑"评测器设计是独立工程变量"。
2. 与 M-104"更强模型作弊更多"的连接：验证 scaling 是对抗 reward hacking 的候选手段（从多条轨迹中挑可靠者），但本篇未测对抗性候选，不外推。
3. "无需训练的验证扩展"与 M-109（训练 harness 生成器）是评测/生成两侧的对应做法；M-110 AOEP 的确定性校验仍不可被本篇替代（治理字段检查 vs 质量排序是两类问题）。

## C4 限制

- 摘要级阅读；四域 SOTA 均为自报，未第三方复现；verifier 单一模型（Gemini 2.5 Flash）为主。
- 候选池来自 GPT-5.5 自采样，oracle 上界受池质量限制。

## C5 下次复核触发

- 第三方复现或反驳；verifier 换代；与 M-108 生成测试的组合研究。

## C6 来源去向

- 纳入知识库（A12，摘要级+定位段）；评测横切"验证 scaling"证据。

## C7 勘误与核对记录

- 2026-11-21：UP主简介数字（26.7%、83.1/86.5/92.1）逐项核对一致；"DeepSeek 自验证超 Fable5"（视频标题部分）未在所读段落找到，登记未核。
