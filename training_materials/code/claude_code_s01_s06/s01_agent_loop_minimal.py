"""s01 最小示例：Agent Loop。

这个脚本故意不用真实大模型，而是用一个非常简单的“假模型”来模拟：

1. 模型先收到用户问题
2. 模型决定要调用工具
3. 程序执行工具
4. 工具结果写回消息历史
5. 模型基于新历史继续，最后给出答案

这样做的好处是：

- 讲循环时不受外部 API 干扰
- 每一步都能稳定复现
- 听众更容易看懂数据流
"""

from __future__ import annotations


def search_kb(query: str) -> str:
    """一个极简搜索工具。

    真实系统里，这里可能是搜索引擎、数据库或知识库查询。
    教学版只需要一个字典就足够演示“工具调用 -> 结果回流”的机制。
    """

    kb = {
        "子智能体": "子智能体在 s04 首次引入，重点是上下文隔离。",
        "todo": "TodoWrite 在 s03 引入，重点是会话内规划。",
    }
    for key, value in kb.items():
        if key in query:
            return value
    return "知识库里没有找到对应内容。"


def fake_model(messages: list[dict]) -> dict:
    """一个极简“模型”。

    这个函数根据当前消息历史决定下一步输出什么。
    重点不是拟真，而是帮助培训时看清 Agent Loop 的结构。
    """

    last_message = messages[-1]

    # 第一轮：如果最后一条是用户问题，就先请求工具。
    if last_message["role"] == "user" and isinstance(last_message["content"], str):
        return {
            "type": "tool_use",
            "tool_name": "search_kb",
            "tool_input": last_message["content"],
        }

    # 第二轮：如果最后一条是工具结果，就基于结果生成最终答案。
    if last_message["role"] == "tool":
        return {
            "type": "final",
            "answer": f"根据工具结果，最终答案是：{last_message['content']}",
        }

    return {"type": "final", "answer": "无法继续。"}


def run_agent_loop(query: str) -> str:
    """运行最小 Agent Loop。"""

    # 这就是最小状态。
    # 培训里可以强调：`messages` 不是展示层聊天记录，
    # 而是下一轮推理真正会读取的工作上下文。
    messages: list[dict] = [{"role": "user", "content": query}]

    while True:
        model_output = fake_model(messages)
        print(f"\n模型输出: {model_output}")

        if model_output["type"] == "tool_use":
            result = search_kb(model_output["tool_input"])

            # 关键点：工具结果必须重新写回消息历史。
            # 如果少了这一步，下一轮“模型”就无法基于真实观察继续工作。
            messages.append(
                {
                    "role": "tool",
                    "tool_name": model_output["tool_name"],
                    "content": result,
                }
            )
            print(f"工具结果已写回 messages: {result}")
            continue

        if model_output["type"] == "final":
            return model_output["answer"]


if __name__ == "__main__":
    answer = run_agent_loop("请告诉我 learn-claude-code 里哪一章首次引入子智能体")
    print("\n最终答案:")
    print(answer)
