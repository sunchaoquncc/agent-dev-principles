# 业务 Agent 开发规则

v0.7 · 2026-10-13。面向开发业务 agent 的助手与工程团队，覆盖业务契约、事实、工具副作用、恢复、授权、接管、评测和发布。

## 使用

将本包放入开发项目：根 AGENTS.md 提供12条执行规则；按任务读取 principles/01—05。不要把整包原样注入业务 agent 系统提示。

- [核心规则](AGENTS.md)
- [提示与契约](principles/01_prompt.md) / [上下文与状态](principles/02_context.md) / [工具与恢复](principles/03_harness.md)
- [评测](principles/04_evaluation.md) / [安全](principles/05_security.md)
- [案例](principles/06_cases.md)
- [业务交付模板](principles/08_business_delivery_checklist.md)：填写实际业务要求和测试证据。
- [证据与适用性登记](principles/07_evidence.md)：维护时查阅，集中保留来源、适用模型、验证日期和触发器。

## 适用边界

这是一套有条件工程要求与方法建议，尚未在具体目标业务验证效果。业务政策由项目负责人确认；模型、工具、权限和客户端必须在真实目标栈验收。模拟或案例报告不代表生产收益。

本包自包含，不要求读者访问私有研究笔记；来源链接集中在维护附录。研究过程、原文、实验与历史争议不随包发布。
