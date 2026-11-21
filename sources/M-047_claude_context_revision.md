# M-047 Claude上下文指导自我修订

## 元信息

- 来源链接：[原文](https://claude.dev/blog/the-new-rules-of-context-engineering-for-claude-5-generation-models/)
- 原文快照：[_snapshots_local/batch09/claude_context.html](_snapshots_local/batch09/claude_context.html)，哈希/检索时间见同名.html.json；txt仅定位辅助。
- 发布日期：2026-07-24；主张实质更新日期：未知。
- 检索/审查日期：2026-10-13；验证日期：未验证效果。
- 作者/机构：Thariq Shihipar / Anthropic
- 适用模型：Claude Opus 5、Claude Fable 5；Claude Code环境
- 来源类型与利益关系：厂商一手工程自述；一手不等于独立验证。
- 数据/事件观测窗口：内部实验运行日期未提供。
- 工件检查范围：全文正文；未检查历史提示diff或运行内部评测。
- 证据等级：经验断言/作者报告；当前状态：候选，原则升级为零。
- 复核触发器：下一代模型发布、原文修订、反例或新工件出现；超六个月补新据，不刷新旧数据日期。
- 框架落点：prompt / 上下文 / harness及评测安全；关联[总纲](../graph/overview.md)。

## 主张提取

### C1 来源记载

作者报告大幅删减Claude Code系统提示后，其内部编码评测未测得损失。

范围与位置：Unhobbling Claude / 引言；内部编码评测，非业务通用结果。原文短锚点：no measurable loss

### C2 来源记载

具体调整包括把工具使用说明放回工具描述、把验证与代码审查移入按需技能，并保留产品特有上下文。

范围与位置：Then and now / Applying；删减与信息搬移同时发生。原文短锚点：moved verification and code review

## 局限与解释边界

[我方审查] 未公开样本、评测方差、原始提示或消融。不能将全部变化归因于模型能力增长，也不能照抄删减比例；例子无用、HTML必优于截图均是模型与任务相关作者建议。文章经claude.com跳转claude.dev，本轮记录最终地址。

## 与已有知识的比较

补M-002/M-008与Q-001的厂商自我修订记录；限制把旧提示技巧固化成永久要求。不是独立复现。

## 下一步

追历史提示diff及任务失败例；比较保留、删除、搬移三种操作。

## 2026-10-14 Opus 5.5 代际复核（M-090）

方向延续+范围收窄：Opus 5.5 官方指南继续删"模型特定行为补丁"（推理复述/think-carefully行按条件删除，禁思考缓解组合需重测），与本篇"删减无测得损失"同向。但同一指南列有至少六类本批计数的提示/harness脚手架（本代新增归属未核）（早停防护、进度更新、探索指令、时间信号、粘贴标记、样式禁令；计数口径见M-090），且 thinking 禁用接口已移除——"删减"不适用于权限类检查，不构成脚手架整体消失。本篇保持候选级，适用范围按 M-090 存废表 #1 执行：仅"模型特定行为补丁"。详见[M-090](M-090_opus55_generation_review.md)。

## 2026-10-18 反方线索登记（未读全文）

A 类筛选取到反方文章 [Anthropic Deleted 80% of Its System Prompt. You Shouldn't.](https://addozhang.medium.com/anthropic-deleted-80-of-its-system-prompt-you-shouldnt-a35357bd4731)（addozhang/Medium）：主张多数团队不应照搬删减。搜索索引另显示 Pawel Huryn（X 2079700261581271487）质疑 80% 口径——称该数字是 memory 关闭时的字数（Opus 提示 2,686 词→514 词），记忆规则是搬移/重组而非删除。**本批 Medium 直连超时，全文未取得；以上为搜索摘要级线索，不作为证据采用**。若成立，与本文 C2"删减与信息搬移同时发生"的既有边界一致（搬移部分本就不该计入"删除"），口径待全文核。已核部分：X 原帖（Thariq）与本篇 M-047 同源，不另计来源。

