# Agent 开发原则与方法

> 当前为候选开发草案，包含来源迁移与助手工程提案，尚非已完成证据审定的通用标准。后续先持续学习外部开发经验，再按证据逐条更新；不以结构完整代表知识已经成熟。

v0.19 · 2026-10-18。帮助开发助手与工程团队决定如何分配模型判断和代码执行、写提示、组织上下文、设计工具与编排，并比较质量、成本和复杂度。适用于不同业务任务，不是某个领域的定制规则。v0.19 按独立试用修导航、按项目E选定工件补完整失败案例与证明边界，12条核心正文保持，尚未证明整体业务净收益。

日常开发先读核心中的“按当前决策读取”表，按问题进入对应章节；完成当前判断后停止扩读。评估本库收益时先走下方试用入口，记录项目初步诊断后再读核心。下面是目录，不是一次性加载清单。

## 在自己的项目试用

先看[跨项目试用说明](trial/README.md)，把[任务说明](trial/TASK_PROMPT.md)交给开发助手，再带回[反馈](trial/FEEDBACK_TEMPLATE.md)。默认先离线，围绕当前问题选择必要改动；没有明确问题时才做整体审查。不要覆盖业务项目AGENTS。发布完整性见[文件清单](RELEASE_MANIFEST.json)。

### 已收录的实践反馈

- [项目E：纠错案例及选定工件](https://github.com/sunchaoquncc/agent-dev-principles/blob/ab33042d9d8920d7a546fe37f998fbf5ded706ea/trial/feedback/2026-10-18-project-e-correction-case/project-e-correction-case.md)：原错误轨迹、历史离线对照、测试与真实保存反证；各层分别看，完整业务仍失败。

- [项目E：决定变化与无收益尝试](trial/feedback/2026-10-18-project-e-decision-changes-and-limits.md)、[吸收建议](trial/feedback/2026-10-18-project-e-integration-suggestions.md)、[证据摘要](trial/feedback/2026-10-18-project-e-evidence.json)：同项目追加，核心不增；诊断与工程收益不等于完整任务通过，2026-10-18。

- [项目E：上下文与错误恢复的前后试用](trial/feedback/2026-10-16-project-e-context-recovery.md)：局部工程收益、持平结果与未验证的模型行为，2026-10-16。
- [项目E：六条候选补充知识](trial/feedback/2026-10-16-project-e-proposed-additions.md)：结合开发标准和历史经验提出的条件性建议，尚未并入核心原则。

反馈提供项目内证据，不代表跨项目有效性或知识库独立因果收益。

## 从开发任务开始

- [核心12条](AGENTS.md)：默认设计要求、条件机制、比较与交付。
- [提示构建](principles/01_prompt.md)：从样例和决策边界写出第一版并迭代。
- [信息流与预算](principles/02_context.md)：输入表示、工具返回、按需加载和保真。
- [职责与编排](principles/03_harness.md)：模型、业务代码和Harness的协作与选择。
- [评测](principles/04_evaluation.md) / [安全](principles/05_security.md)：按任务与风险应用。
- [跨场景案例](principles/06_cases.md)：检验可迁移性，不限定适用业务。
- [轻量开发记录](principles/08_business_delivery_checklist.md)：五个检查视角，可引用已有记录并按任务裁剪。
- [证据登记](principles/07_evidence.md)：来源、适用模型、验证日期与复核触发器。

把本包供开发助手按需读取，不要原样注入目标业务Agent系统提示。简单任务不必建设持久化/事务平台；有受限数据和高后果动作时也不能省略必要边界。

规则是有条件工程指导，尚未通过跨业务开发实验验证普遍收益。出处集中在维护附录，运行时不必加载；原文与研究过程不随包发布。
