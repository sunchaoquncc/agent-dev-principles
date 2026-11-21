# M-101 Nova Escola 评测生产案例：错误分析先于 rubric 与"不值得建评估器"的失败

## 元信息

- 来源链接：[Case Study: Putting Evals Into Production](https://hamel.dev/notes/llm/ai-product-engineering/evals-production.html)
- 原文快照（供复核）：`_snapshots_local/batch16_glm_20261018/nova_escola.html`（SHA-256 5094647b…，见同名 .json）、提取文本 `nova_escola.txt`（JS 站提取密排但正文完整；四条关键引文均在本地快照内，另经 WebFetch 第二通道互证一致）
- 发布日期：2026-07-09（页面标注）；主张实质更新日期：未知
- 数据/事件观测窗口：Lucas 的会期为 AI Product Engineering 系列（具体录制日期未给）；生产 2% 流量评测为文中描述的持续状态
- 当前适用状态：候选（二手蒸馏：Hamel 记录 Lucas 演讲的笔记页，非原始工件）
- 工件/配置/预算及复现范围：笔记页全文（很短）；文内链接的 eval 电子表格截图、YouTube 端到端视频（youtu.be/mF4CaijvJos）未打开；原始会话材料未取得
- 阅读覆盖与媒介限制：笔记全文文字（四条引文快照内核对）；截图/视频未核
- 版本日期：2026-10-18 抓取版本
- 利益关系与独立性：Hamel Husain 记录（页面显式推广其 AI Evals 课程——蒸馏与导流利益）；一手内容来自 Lucas Machado Rocha（Nova Escola，巴西非营利教育平台，~1M MAU/200,000 教师）；两级归属分开说明，不计作两个独立来源
- 复核触发器：原始视频/材料核对；其他团队重复"rubric 先于错误分析"失败；课程FAQ口径变化
- 检索日期：2026-10-18（A 类筛选子代理发现）
- 作者/机构：Lucas Machado Rocha（一手）/ Hamel Husain（记录）
- 适用模型：未提及具体模型
- 证据等级：经验断言（从业者会话，经二级蒸馏；无数据工件）
- 框架落点：评测（评测构建顺序、标注一致性、生产流量回归）；A 类（何时改提示就够）
- 关联条目：M-032（评测方法论）、M-052（AQuA 失败定位）、D01/D10

## 一句话结论

真实产品团队（教育平台课程规划器）的三个决策边界教训：先写 rubric 后做错误分析导致标注了不需要的数据；有的失败（输出两个学习目标）据笔记改提示后停止；未披露改动行数、评估器撤回动作或长期效果；两名标注员一致率"低于随机"暴露"好"未定义，与教学法专家重写 rubric 后重新标注——错误分析先行、按失败选修复层、真值口径先于采集，三件事都有了从业者会话（经二级蒸馏）的对应物。

## 要点摘录

（引号内逐字取自 2026-10-18 抓取正文，双通道核对一致。）

- "He wrote a rubric before doing error analysis. Since most of his criteria never appeared as failures, his team spent time labeling data they did not need."
- "He built an eval for a problem that needed a simple fix. The assistant sometimes emitted two learning goals when it should emit one. His team changed the prompt and the problem stopped."
- 标注一致率："Lucas used two annotators, and they agreed less often than chance. The team had not defined what good looked like clearly enough, so they rewrote the rubric with their pedagogical experts and relabeled the data."
- 生产回归："He catches regressions early by running a suite of evals daily against 2% of production traffic."

## 主张卡

| 主张ID | 归属 | 主张与环境范围 | 原文位置与短锚点 | 局限/缺失信息 | 与既有知识的关系 |
|---|---|---|---|---|---|
| NE-1 | 来源记载 | rubric 先于错误分析→标注浪费 | "never appeared as failures" | 二手蒸馏；无浪费量数字 | 支持 M-032 错误分析先行；D01"失败例"顺序 |
| NE-2 | 来源记载 | 笔记报告改提示后该问题停止；未说明改动行数或撤回评估器 | "changed the prompt and the problem stopped" | 无后续复发信息 | A 类核心反例：不是每个失败都值得建评估器；D03 修订粒度的最小化 |
| NE-3 | 来源记载 | 作者把两标注员一致率低于随机解释为标准不清，随后重写rubric并重标 | "less often than chance" | 一致率具体数字未给；两名标注员 | D10"人工校准"与 D01"谁判断好坏"的具体失败形态 |
| NE-4 | 来源记载 | 每日对 2% 生产流量跑评测套件抓回归 | "daily against 2% of production traffic" | 套件构成/成本/误报未述 | D10生产回归实践报告；成本未知，不以2%推断负担轻 |

## 适用条件与反证

- 适用条件：教育内容生成域、真实生产流量；教训为流程级（顺序/口径），非数字级
- 反证/局限：Hamel 蒸馏层级（原始会话未核）；无任何量化工件；"改提示即解决"无长期跟踪——复发未知；课程导流利益

## 与已有条目的关系

- M-032/M-052：评测构建顺序与失败定位的二手实践例
- M-100：两个来源的系统、失败定义、观察期和证据强度不同，并不构成同条件下的冲突。可以提出“按失败机制和后果选修复层”的工程假设；现有材料不能证明行为级改提示就够、机制族必需扫描器的划界。
- D01/D10：支持在扩大标注前核对标准与分歧的经验；不推出任何数据采集都须先冻结完整rubric。必要目标/约束可先有，观察到的错误再帮助细化判据。

## 后续动作

- [ ] 需要补读的：YouTube 原始会话与 eval 电子表格（外链）；Hamel FAQ"when to automate an evaluator"一节（被本文引用为该权衡的正式讨论）
- [ ] 复核触发器：原始材料核对后升级/修正本笔记

## 2026-10-18 主审修正

本地十行正文没有“一行提示”或“撤回评估器”记载，已删除该添加；二手笔记不标一手例，不将低一致率普遍等同目标未定义。无已见失败不意味着所有未命中判据都该删，必要合同与高后果约束仍需覆盖。视频/截图仍未核，不升级证据。
