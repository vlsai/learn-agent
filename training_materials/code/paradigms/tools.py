"""教学版工具模块。

这个版本只保留两个工具：

1. `search_snake_notes`
2. `calculator`

原因是培训里最重要的是让听众看清：

- 模型为什么要调用工具
- 工具结果怎么回到下一轮推理
- 工具层可以有多简单，但闭环不能省
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
from typing import Callable

from paradigms.demo_data import SNAKE_NOTES


@dataclass
class ToolSpec:
    """用于描述一个教学工具的最小结构。"""

    name: str
    description: str
    handler: Callable[[str], str]


def search_snake_notes(query: str) -> str:
    """在本地资料库里查找与贪吃蛇任务相关的说明。

    这是一个非常轻量的关键词搜索。
    它不是为了追求最强检索，而是为了让 ReAct demo 稳定地体现：

    - Agent 主动决定去查资料
    - 工具返回结构化观察结果
    - 下一轮推理会使用这些结果
    """

    keywords = [item.strip().lower() for item in query.split() if item.strip()]
    if not keywords:
        keywords = [query.strip().lower()]

    scored_notes: list[tuple[int, dict[str, str]]] = []
    for note in SNAKE_NOTES:
        haystack = f"{note['title']} {note['content']}".lower()
        score = sum(1 for keyword in keywords if keyword and keyword in haystack)
        if score > 0:
            scored_notes.append((score, note))

    scored_notes.sort(key=lambda item: item[0], reverse=True)
    matched_notes = [note for _, note in scored_notes[:3]]

    if not matched_notes:
        return "本地资料库里没有找到匹配内容。"

    lines: list[str] = []
    for index, note in enumerate(matched_notes, start=1):
        lines.append(f"[{index}] {note['title']}")
        lines.append(note["content"])
        lines.append("")
    return "\n".join(lines).strip()


def calculator(expression: str) -> str:
    """安全计算一个非常简单的算术表达式。

    这个工具不是主角，但很适合拿来说明：
    工具不一定非得是“联网搜索”或“文件系统操作”，
    一个小到只做运算的能力，也可以成为 Agent 的外部动作。
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
            operand_value = _eval(node.operand)
            if isinstance(node.op, ast.USub):
                return -operand_value
            if isinstance(node.op, ast.UAdd):
                return operand_value
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
    "search_snake_notes": ToolSpec(
        name="search_snake_notes",
        description="搜索本地贪吃蛇任务说明，适合补玩法、UI 和质量要求。",
        handler=search_snake_notes,
    ),
    "calculator": ToolSpec(
        name="calculator",
        description="计算简单算术表达式，适合估算网格、像素尺寸和速度参数。",
        handler=calculator,
    ),
}


def render_tool_descriptions() -> str:
    """把工具说明渲染成 prompt 可直接使用的文本。"""

    lines: list[str] = []
    for tool in TOOLS.values():
        lines.append(f"- {tool.name}: {tool.description}")
    return "\n".join(lines)


def run_tool(tool_name: str, tool_input: str) -> str:
    """按名称执行工具。

    这种 dispatch map 写法非常适合教学：
    增加工具时，不需要改 Agent 主循环，只要注册新 handler 即可。
    """

    tool = TOOLS.get(tool_name)
    if tool is None:
        return f"未知工具: {tool_name}"
    return tool.handler(tool_input)
