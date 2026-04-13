"""三种范式 demo 共享的本地教学数据。

为什么要做这个文件？

因为培训演示时，我们不希望 ReAct 还依赖额外的搜索 API。
只要本地放一份小型知识库，就已经足够演示：

- Agent 如何决定调用工具
- 工具如何返回结果
- Observation 如何进入下一轮推理
"""

TRAINING_NOTES: list[dict[str, str]] = [
    {
        "id": "paradigm_react",
        "title": "ReAct 范式",
        "content": (
            "ReAct 是 Reasoning 和 Acting 的结合。"
            "它通过 Thought -> Action -> Observation 循环，把模型推理和工具调用连接起来。"
            "它适合实时问答、检索增强、API 编排等需要边走边修正的任务。"
        ),
    },
    {
        "id": "paradigm_plan",
        "title": "Plan-and-Solve 范式",
        "content": (
            "Plan-and-Solve 强调先规划再执行。"
            "常见实现是先由 Planner 生成结构化步骤，再由 Executor 严格按步骤完成。"
            "它适合多步推理、流程型任务和结构化内容生成。"
        ),
    },
    {
        "id": "paradigm_reflection",
        "title": "Reflection 范式",
        "content": (
            "Reflection 强调先生成初稿，再反思，再优化。"
            "它适合代码优化、报告打磨和高价值决策建议。"
            "本质上是用额外的模型调用换更高质量的结果。"
        ),
    },
    {
        "id": "s01",
        "title": "learn-claude-code s01: The Agent Loop",
        "content": (
            "这一章的核心是建立主循环。"
            "没有 loop，就没有真正的 agent。"
            "工具结果必须重新进入消息历史，成为下一轮推理输入。"
        ),
    },
    {
        "id": "s02",
        "title": "learn-claude-code s02: Tool Use",
        "content": (
            "这一章强调加工具不需要改主循环。"
            "关键是通过 dispatch map 把工具名映射到 handler。"
            "同时要在工具层处理路径安全和执行边界。"
        ),
    },
    {
        "id": "s03",
        "title": "learn-claude-code s03: TodoWrite",
        "content": (
            "这一章强调会话内规划。"
            "计划不是替模型思考，而是把当前要做什么显式写出来。"
            "同一时间最多一个 in_progress，有助于模型保持焦点。"
        ),
    },
    {
        "id": "s04",
        "title": "learn-claude-code s04: Subagents",
        "content": (
            "这一章首次引入子智能体。"
            "它的重点不是并发，而是上下文隔离。"
            "父智能体只拿回必要结果，不把全部中间噪声堆进主上下文。"
        ),
    },
    {
        "id": "s05",
        "title": "learn-claude-code s05: Skills",
        "content": (
            "这一章强调按需知识加载。"
            "不要把所有长期知识永远塞进 system prompt。"
            "先暴露可用 skill 的轻量目录，需要时再加载正文。"
        ),
    },
    {
        "id": "s06",
        "title": "learn-claude-code s06: Context Compact",
        "content": (
            "这一章解决上下文膨胀问题。"
            "核心做法包括：大输出写磁盘、旧结果微压缩、长历史做摘要。"
            "上下文不是越多越好，而是要保留继续推进任务真正有用的信息。"
        ),
    },
]
