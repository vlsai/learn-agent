"""s03 最小示例：会话内规划。"""

from __future__ import annotations


class TodoManager:
    """一个最小但可运行的 todo 管理器。

    这个类的价值不是“功能完整”，而是帮助听众理解：
    todo 在这一章里是会话内规划状态，不是长期项目管理平台。
    """

    def __init__(self) -> None:
        self.items: list[dict[str, str]] = []

    def update(self, items: list[dict[str, str]]) -> None:
        """整体更新当前计划。

        培训版用“整份重写”而不是局部增删改，
        因为这样更容易讲清楚计划状态的全貌。
        """

        in_progress_count = sum(
            1 for item in items if item.get("status") == "in_progress"
        )
        if in_progress_count > 1:
            raise ValueError("同一时间最多只能有一个 in_progress。")
        self.items = items

    def render(self) -> str:
        marker_map = {
            "pending": "[ ]",
            "in_progress": "[>]",
            "completed": "[x]",
        }
        lines = []
        for item in self.items:
            marker = marker_map[item["status"]]
            lines.append(f"{marker} {item['content']}")
        return "\n".join(lines)


def demo() -> None:
    todos = TodoManager()

    todos.update(
        [
            {"content": "阅读 hello-agents 第四章", "status": "completed"},
            {"content": "准备三种范式讲义", "status": "in_progress"},
            {"content": "现场跑教学 demo", "status": "pending"},
        ]
    )
    print("第一次渲染：")
    print(todos.render())

    print("\n更新后：")
    todos.update(
        [
            {"content": "阅读 hello-agents 第四章", "status": "completed"},
            {"content": "准备三种范式讲义", "status": "completed"},
            {"content": "现场跑教学 demo", "status": "in_progress"},
        ]
    )
    print(todos.render())


if __name__ == "__main__":
    demo()
