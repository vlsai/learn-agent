"""s02 最小示例：Tool Dispatch。

这个脚本要演示的重点只有一个：

> 加工具，不需要改主循环；
> 只需要把工具注册进 dispatch map。
"""

from __future__ import annotations

from pathlib import Path


WORKSPACE = Path(__file__).resolve().parent / "_demo_workspace"
WORKSPACE.mkdir(exist_ok=True)


def safe_path(relative_path: str) -> Path:
    """把相对路径限制在教学工作区内。

    这就是 s02 特别值得讲的一个工程意识：
    工具层不是简单转发参数，而是要顺手处理安全边界。
    """

    path = (WORKSPACE / relative_path).resolve()
    if not path.is_relative_to(WORKSPACE):
        raise ValueError(f"路径逃逸工作区: {relative_path}")
    return path


def run_read(path: str) -> str:
    return safe_path(path).read_text(encoding="utf-8")


def run_write(path: str, content: str) -> str:
    safe_path(path).write_text(content, encoding="utf-8")
    return f"已写入 {path}"


def run_edit(path: str, old_text: str, new_text: str) -> str:
    file_path = safe_path(path)
    original = file_path.read_text(encoding="utf-8")
    if old_text not in original:
        return "没有找到待替换文本。"
    file_path.write_text(original.replace(old_text, new_text), encoding="utf-8")
    return f"已编辑 {path}"


# 这就是 dispatch map。
# 真实系统里可能还会接 schema、权限、上下文对象。
# 教学版先把“工具名 -> handler”的核心思想讲清楚就够了。
TOOL_HANDLERS = {
    "read_file": lambda **kw: run_read(kw["path"]),
    "write_file": lambda **kw: run_write(kw["path"], kw["content"]),
    "edit_file": lambda **kw: run_edit(
        kw["path"], kw["old_text"], kw["new_text"]
    ),
}


def demo() -> None:
    print(TOOL_HANDLERS["write_file"](path="note.txt", content="hello tool dispatch"))
    print(TOOL_HANDLERS["read_file"](path="note.txt"))
    print(
        TOOL_HANDLERS["edit_file"](
            path="note.txt",
            old_text="hello",
            new_text="hello, updated",
        )
    )
    print(TOOL_HANDLERS["read_file"](path="note.txt"))


if __name__ == "__main__":
    demo()
