"""教学版工具模块。

真实 Agent 系统的工具层通常会更复杂：

- 有 schema
- 有权限控制
- 有日志与监控
- 有重试和错误分类

但在培训版里，我们只保留两个最容易讲清楚的工具：

1. `search_notes`：搜索本地教学知识库
2. `calculator`：做简单数学计算

这样做的好处是：

- 不依赖第三方搜索 API
- 可以稳定复现 demo
- 更容易把注意力放在“工作流”而不是“外部服务接入”
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
from typing import Callable

from paradigms.demo_data import TRAINING_NOTES


@dataclass
class ToolSpec:
    """用于描述一个教学工具的最小结构。"""

    name: str
    description: str
    handler: Callable[[str], str]


def search_notes(query: str) -> str:
    """在本地教学知识库中做一个非常简单的关键词搜索。

    这里故意不用复杂检索算法，因为培训演示的核心不是“搜得最强”，
    而是让听众看清楚：

    - Agent 决定调用工具
    - 工具返回结果
    - 返回结果被下一轮推理再次使用
    """

    keywords = [word.strip().lower() for word in query.split() if word.strip()]
    if not keywords:
        keywords = [query.lower()]

    scored_results: list[tuple[int, dict[str, str]]] = []
    for note in TRAINING_NOTES:
        haystack = f"{note['title']} {note['content']}".lower()
        score = sum(1 for keyword in keywords if keyword in haystack)
        if score > 0:
            scored_results.append((score, note))

    scored_results.sort(key=lambda item: item[0], reverse=True)
    top_notes = [note for _, note in scored_results[:3]]

    if not top_notes:
        return "没有在本地培训知识库里找到相关内容。"

    lines: list[str] = []
    for index, note in enumerate(top_notes, start=1):
        lines.append(f"[{index}] {note['title']}")
        lines.append(note["content"])
        lines.append("")
    return "\n".join(lines).strip()


def calculator(expression: str) -> str:
    """安全地计算一个非常简单的算术表达式。

    这里使用 `ast` 做白名单求值，而不是直接 `eval()`。
    培训时可以顺便强调一个工程习惯：

    > 即使是 demo，也尽量不要直接把任意字符串交给 `eval()`。
    """

    allowed_nodes = (
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Constant,
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.Mod,
        ast.Pow,
        ast.USub,
        ast.UAdd,
        ast.FloorDiv,
    )

    def _eval(node: ast.AST) -> float:
        if not isinstance(node, allowed_nodes):
            raise ValueError(f"不支持的表达式节点: {type(node).__name__}")

        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.Constant):
            if not isinstance(node.value, (int, float)):
                raise ValueError("只允许数字常量。")
            return float(node.value)
        if isinstance(node, ast.UnaryOp):
            value = _eval(node.operand)
            if isinstance(node.op, ast.USub):
                return -value
            if isinstance(node.op, ast.UAdd):
                return value
            raise ValueError("不支持的单目运算符。")
        if isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)
            if isinstance(node.op, ast.Add):
                return left + right
            if isinstance(node.op, ast.Sub):
                return left - right
            if isinstance(node.op, ast.Mult):
                return left * right
            if isinstance(node.op, ast.Div):
                return left / right
            if isinstance(node.op, ast.Mod):
                return left % right
            if isinstance(node.op, ast.Pow):
                return left**right
            if isinstance(node.op, ast.FloorDiv):
                return left // right
            raise ValueError("不支持的双目运算符。")

        raise ValueError("未处理的表达式类型。")

    parsed = ast.parse(expression, mode="eval")
    result = _eval(parsed)
    return f"{expression} = {result}"


TOOLS: dict[str, ToolSpec] = {
    "search_notes": ToolSpec(
        name="search_notes",
        description=(
            "搜索本地培训知识库。"
            "适合查找三种智能体范式和 learn-claude-code 前 6 章的讲义信息。"
        ),
        handler=search_notes,
    ),
    "calculator": ToolSpec(
        name="calculator",
        description="计算简单算术表达式，比如 12 * (8 + 3) / 2。",
        handler=calculator,
    ),
}


def render_tool_descriptions() -> str:
    """把工具说明渲染成一段文本，方便直接塞进提示词。"""

    lines = []
    for tool in TOOLS.values():
        lines.append(f"- {tool.name}: {tool.description}")
    return "\n".join(lines)


def run_tool(tool_name: str, tool_input: str) -> str:
    """按名称执行工具。

    这就是教学版的 dispatch map。
    它刚好和 `learn-claude-code` s02 的思想相呼应：

    > 加工具，尽量不要改主循环；
    > 只要把工具注册进映射表即可。
    """

    tool = TOOLS.get(tool_name)
    if tool is None:
        return f"未知工具: {tool_name}"
    return tool.handler(tool_input)
