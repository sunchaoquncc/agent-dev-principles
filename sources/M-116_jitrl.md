# M-116 JitRL：测试时策略优化（无梯度的即时强化学习）（超窗·历史对照用途）

## 元信息

- 来源链接：[arXiv:2601.18510](https://arxiv.org/abs/2601.18510)
- 原文快照：[_snapshots_local/batch17/jitrl.pdf](_snapshots_local/batch17/jitrl.pdf)，哈希见同名.pdf.json；pypdf提取txt（26页，行号以txt计）。
- 发布日期：arXiv 2601（2026-01，**约10个月前，超6个月窗口**；UP主标注 ICML26 Spotlight，会议归属未从文本核实）。
- 检索/审查日期：2026-11-21；验证日期：未复现。代码：github.com/liushiliushi/JitRL（未取）。
- 作者/机构：Yibo Li、Zijie Lin 等 / 新加坡国立大学；通讯作者 Shuo Ji（jitrl.txt L39-40，Bryan Hooi 为末位作者非通讯）。
- 发布日期与版本：**所据快照为 arXiv v4（2026-09-27 修订，窗口内）**；v1 首发为 2026-01。会议归属：ICML 2026（PMLR 306，文本有据 L41-43）；**仅"Spotlight"等级未从文本核实**。v1→v4 修订程度未逐版对比；按首发日期判级超窗（约10个月），若 v4 属主张实质更新则窗口归属待重新裁决。
- 适用模型：WebArena 与 Jericho 实验（模型构成未逐项核）；下一代模型发布触发复核。
- 来源类型与利益关系：预印本；学术。
- 阅读覆盖与媒介限制：摘要+引言开头精读——**摘要级精读**。
- 渠道路径：B站UP主08-22视频发现（docs/39 A14）。
- **用途限制（新鲜度纪律）**：超窗，仅作时间序列/对照用途，不充当现行指导、不支持原则层升级。

## 一句话

无梯度的测试时策略优化：维护非参数经验记忆、检索相关轨迹即时估计动作优势，把估计直接加到 LLM 输出 logits 上——理论上证明该加性更新是 KL 约束策略优化的精确闭式解；WebArena/Jericho 上超 training-free 方法、胜过微调方法（如 WebRL）且成本降 30× 以上。

## C1 来源记载（摘要直述）

- 机制："maintains a dynamic, non-parametric memory of experiences and retrieves relevant trajectories to estimate action advantages on-the-fly. These estimates are then used to directly modulate the LLM's output logits."
- 理论："this additive update rule is the exact closed-form solution to the KL-constrained policy optimization objective."
- 结果：WebArena/Jericho 上 training-free SOTA；超 WebRL 等微调方法且"reducing monetary costs by over 30×"。

## C3 我方推导与比较（限于对照用途）

1. 与 M-111 SSSM 提案同族（把"学习"压进推理时而非权重），但路径不同：JitRL 动 logits（外置记忆+闭式更新），SSSM 改后训练目标——测试时学习的两条技术路线快照（2026-01 vs 2026-11）。
2. 与 EvoTest（A15/M-119）同用 Jericho 类基准：JitRL 调 logits、EvoTest 调整个系统配置——"测试时学习"的粒度谱系两极。

## C4 限制

- 超窗+摘要级；数字未复核；ICML26 Spotlight 归属待核。

## C5 下次复核触发

- 会议版发布或后续工作时并入技能/测试时学习线合审。

## C6 来源去向

- 纳入知识库（A14，摘要级）；测试时学习线历史节点。

## C7 勘误与核对记录

- 2026-11-21：UP主"ICML26 Spotlight｜NUS爆火论文"——arXiv 为 2026-01（超窗），会议归属未核；同 M-112 教训：先核 arXiv 日期再定级。
