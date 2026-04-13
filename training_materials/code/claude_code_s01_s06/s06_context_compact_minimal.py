"""s06 最小示例：上下文压缩。"""

from __future__ import annotations

from pathlib import Path


OUTPUT_DIR = Path(__file__).resolve().parent / ".task_outputs"
OUTPUT_DIR.mkdir(exist_ok=True)


def persist_large_output(tool_use_id: str, output: str, threshold: int = 120) -> str:
    """把过大的工具输出写入磁盘，只在上下文里保留预览。"""

    if len(output) <= threshold:
        return output

    file_path = OUTPUT_DIR / f"{tool_use_id}.txt"
    file_path.write_text(output, encoding="utf-8")
    preview = output[:120]
    return (
        "<persisted-output>\n"
        f"Full output saved to: {file_path}\n"
        f"Preview:\n{preview}\n"
        "</persisted-output>"
    )


def micro_compact(messages: list[dict]) -> list[dict]:
    """只保留最近 3 个工具结果的完整内容。"""

    tool_result_indices = [
        index for index, msg in enumerate(messages) if msg["role"] == "tool"
    ]
    for old_index in tool_result_indices[:-3]:
        messages[old_index]["content"] = "[Earlier tool result omitted for brevity]"
    return messages


def compact_history(messages: list[dict]) -> list[dict]:
    """把过长历史压缩成一份连续性摘要。"""

    summary = (
        "对话已经压缩。当前需要保留的信息有：\n"
        "- 目标：继续完成当前任务\n"
        "- 最近碰过的文件：demo.py, notes.md\n"
        "- 已完成：读取文件、执行命令、修复一个报错\n"
        "- 下一步：继续验证输出是否正确"
    )
    return [{"role": "user", "content": summary}]


def demo() -> None:
    oversized_output = "A" * 500
    persisted = persist_large_output("tool_001", oversized_output)
    print("大输出持久化后的上下文表示：")
    print(persisted)

    messages = [
        {"role": "tool", "content": "result 1"},
        {"role": "tool", "content": "result 2"},
        {"role": "tool", "content": "result 3"},
        {"role": "tool", "content": "result 4"},
        {"role": "tool", "content": "result 5"},
    ]
    print("\n微压缩前：")
    print(messages)
    print("\n微压缩后：")
    print(micro_compact(messages))

    long_history = [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]
    print("\n完整压缩后的历史：")
    print(compact_history(long_history))


if __name__ == "__main__":
    demo()
