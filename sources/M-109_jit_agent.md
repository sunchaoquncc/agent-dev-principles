# M-109 JIT-Agent：按任务现场生成 Harness 的"Model-as-a-Harness"

## 元信息

- 来源链接：[arXiv:2608.25593v2](https://arxiv.org/abs/2608.25593)；代码声明 https://github.com/bingreeky/JIT（未取）。
- 原文快照：[_snapshots_local/batch17/jit_agent.pdf](_snapshots_local/batch17/jit_agent.pdf)，哈希见同名.pdf.json；pypdf提取txt（24页，行号以txt计）。
- 发布日期：arXiv v2 2026-09-03；主张实质更新日期：v1→v2 未逐版对比。
- 检索/审查日期：2026-11-21；验证日期：未复现。
- 作者/机构：署名 "JIT-Agent Team"（Contributors：Guibin Zhang、Leo Lu、Fangzhou Xie 等；通讯 Wangchunshu Zhou、Chuanrui Hu、Yafeng Deng、Shuicheng Yan）/ 新加坡国立大学、EverMind AI、南洋理工大学。
- 适用模型：JIT-Agent-27B 基于 Qwen3.6-27B 训练；被包裹 backbone：GLM-5.2、DeepSeek-V4-Flash/Pro、Qwen3.6、Mimo-V2.5；对照 GPT-5.6、Gemini 3.1 Pro/3.5 Flash、Kimi K2.7 Code。下一代模型发布触发复核。
- 来源类型与利益关系：预印本（v2，未见评审标记；无自述 Limitations 章节）；EverMind AI 参与商业利益可能；一手不等于独立验证。
- 阅读覆盖与媒介限制：摘要/方法/主结果表2-3/Pareto分析/迁移实验全读；附录与个别图表未逐项核读。
- 渠道路径：B站UP主09-01视频发现（docs/39 A6）；内容全部取自论文原文。

## 一句话

把 harness 生成从"事前优化持久工件"（AOT）改为"训练一个 27B 元模型按任务实例现场合成、修复、进化四模块 harness"（JIT）：18 个 backbone-基准配对全部提升、6 个固定 harness 对照中 4 项最佳且 6/6 成本最低——DeepSeek-V4-Flash 加 JIT harness 在两基准超过 GPT-5.6。

## C1 来源记载（正文直述，引文逐字自txt）

**AOT/JIT 范式对立（L38-68）**：既有方法（含 RHO 线，即 M-108 对比的基线家族）多为 AOT："the harness is treated as a durable artifact to be optimized over an experience stream, with the hope that the resulting artifact will generalize across future tasks"；JIT 立场："the appropriate harness is not only domain-dependent, but instance-dependent"（L63-64）。

**四模块协议（L163-196）**：h = (M,P,A,F)——memory（history→view）、planning（view→directive）、action（控制更新+动作发出）、capability-orchestration（按指令激活工具/skills 子集），运行时依赖序 M→P→F→A；协议同时维护不可变事件历史 ξ<t 与可变控制器状态 st（式3）。协议兼容空间 G ⊇ Hsyn ⊇ HΠ ⊇ Hexec。HARNESSFACTORY 把 13 个代表性 scaffold（ReAct/PlanAndExecute/ReSum/GAM/MemoBrain/AggAgent/OAgent/AgentFold/HiAgent/DeepAgent/ROMA/AOrchestra/FlashSearcher）统一重实现为种子库 B0。

**三阶段训练（L205-290 + 图2）**：Stage I 任务条件定制（冻结 teacher 生成协议合规 harness，SFT + reward/latency/cost 三轴偏好 DPO，偏好保留条件=reward 升+两效率轴不降+至少一轴严格升）；Stage II 修复轨迹（把编译错误/接口不匹配/运行时异常与诊断配对，仅保留 ≤2 轮内修复成功的轨迹作监督）；Stage III Evo-GDPO 在线进化（候选与 incumbent bank 同预算同种子对打，reward 主轴，效率增益仅在保持 reward 时激活；无效候选修复仍计成本）。

**主结果（Table 2，9基准）**：换默认 scaffold 后 18/18 配对提升：GLM-5.2 均分 74.1→81.8，DS-V4-Flash 66.7→75.5；最大增益在长程规划（DS-V4-Flash DeepPlanning-Shopping 59.1→83.9，GLM-5.2 Travel 62.8→83.0）。"the JIT-equipped systems lead eight of nine columns"（L416）——JIT 系在 9 列中 8 列领先（对全部对比模型；唯一例外列 DeepPlanning-Travel）。头对头对 GPT-5.6：JIT+GLM-5.2 与 JIT+DS-V4-Flash 在多数列领先（JIT+DS-V4-Flash 于 DeepSearchQA 85.1 vs 76.0、OdysseyBench 73.0 vs 68.7 等 5 列领先），但在 BC+（74.0 vs 76.9）、AgentIF（63.8 vs 68.0）、Travel（61.3 vs 84.9）、Office（63.4 vs 65.3）落后（表2逐列）。

**固定 harness 对照（Table 3，骨干固定）**：与 Claude Code/Codex/OpenCode/Hermes/NanoBot 比：6 设置中 4 项最佳（DSQA +4.7、xBench +4.0 等），另 2 项差 3.1/3.9 分但 token 大幅少；**"JIT-Agent has the lowest token consumption and cost in all six settings, reducing per-case cost by 14.9–54.1% relative to the cheapest fixed alternative, or 36.0% on average"**（L547-548）；例：xBench-DS tokens 527K→212K、成本 $0.075→$0.039 且性能 78.0→82.0。结论："The gains therefore arise from task-conditioned scaffolds rather than longer trajectories."（L551）

**跨家族迁移（L594-601）**：6 backbone × 4 基准 24 组配对全胜（均 +7.6；家族均值 DeepSeek +10.2 / Qwen +4.0 / Mimo +8.6）。

**结论（L620-621）**：harness intelligence——"the capacity to adapt the operational scaffold through which a model acts"——为"trainable and transferable source of agent capability beyond model weights alone"。

## C2 作者解释

- harness intelligence 三性质定义（L80-85）：adaptivity（匹配任务与 backbone）、reliability（可执行+合成失败可恢复）、evolvability（执行反馈转化为更强未来 harness）；"Intelligence about the harness begins where competence within a fixed harness ends."
- "code carries the harness"（L92-93）：harness 表示为结构化可执行模块而非无约束 agent 程序，使生成可行。

## C3 我方推导与比较（工作草案）

1. **与 M-108 组成 harness 治理"两种时间观"对照**：HarnessPro（AOT：持久工件离线进化出 lite/medium/heavy）vs JIT-Agent（实例化：每任务现场合成）。注意 JIT 论文把 RHO 家族整体归为 AOT。两篇同月相邻发表、结论互不引用，暂按并列范式登记；工程上可能混合（JIT 生成 + AOT 归档进化——JIT 自己的 harness archive 即雏形）。
2. **Q-001 最直接的"吸收"证据**：训练一个专门模型承担 harness 工程——脚手架设计本身被内化为模型能力。同时它又造出新外围层（元模型+协议+种子库）：**吸收与增厚并行**，与总纲 Q-001"没人能准确度量吸收了多少"的立场一致，登记为行为证据而非度量。
3. **"instance-dependent"主张**与 M-103（给目的不给方法）、M-105（schema 按域而非按任务）形成粒度谱系：域级 schema / 任务级 harness / 会话内自主判断——按什么粒度定制是 harness 设计的核心自由度，三源给出不同答案。
4. 成本-性能同向证据族第四源（6/6 成本最低 + 性能多数最佳），与 M-105/M-106/M-108 汇合。
5. Stage II 修复监督（失败→诊断→≤2轮有界修复）与 M-100 静默失败分类学（点修复→元规则）同族：把失败轨迹转化为训练/改进信号。

## C4 限制与反证

- **无自述 Limitations 章节**（我方登记的主要缺口）：v2 预印本，匿名团队署名，评审状态未知。
- 固定 harness 对照是作者在自家协议 kernel 下的重实现/移植，可能系统性低估 Claude Code/Codex 原生形态（表3中 Claude Code 每例成本 DS-V4-Flash 组 $0.079-$0.114、Qwen3.6-Flash 组 $0.128-$0.177，与产品订阅模式口径不同）。
- "surpasses GPT-5.6" 为选择性表述：仅两基准；GPT-5.6 在 DeepPlanning-Travel 仍领先 1.9 分（L419-420）。
- teacher 模型与训练数据细节未在此读数范围内披露；27B 元模型自身的部署/维护成本未计入 per-case 成本。
- [我方推导] Evo-GDPO 在线进化依赖真实 reward 信号来源，部署分布漂移下的 archive 退化未讨论。

## C5 下次复核触发

- GitHub 仓库（bingreeky/JIT）第三方复现或质疑。
- 与 HarnessPro/RHO/AHE 同线工作的横向对比研究出现。
- GPT-5.7/下一代 backbone 发布（Table 2 排名可能重排）。
- M-108 与本篇的 AOT/JIT 范式对照若进入原则层，触发两篇联合复核。

## C6 来源去向

- 纳入知识库（A6精读）；harness 治理线与 M-108 组对照对；Q-001 行为证据（吸收+增厚并行）；成本-性能同向证据族。

## C7 勘误与核对记录

- 2026-11-21：UP主称"按任务在线生成Harness，让DeepSeek-V4-Flash领先GPT-5.6"，与论文摘要一致（领先限于 DeepSearchQA +9.1 与 OdysseyBench +4.3 两基准，正文 L416-420 亦确认 Travel 例外）；未逐数字对照视频（字幕稿未校验）。
- 2026-11-21 红队勘误：初版把"唯一例外 DeepPlanning-Travel"误挂到对 GPT-5.6 的头对头比较上——原文"sole exception"指 JIT 系在 9 列中领先 8 列（对全部模型）；对 GPT-5.6 逐列实际 5 列领先 4 列落后，已按表2更正。Claude Code 成本区间同步更正（$0.079-$0.114 / Qwen 组 $0.128-$0.177）。
