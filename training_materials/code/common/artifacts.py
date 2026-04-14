"""教学版输出工具。

这套 demo 的最终产物不是一句回答，而是一个真正的 HTML 文件。
所以这里额外抽了一个很小的输出模块，专门处理两件事：

1. 尽量从模型输出中提取代码块
2. 把最终结果写到 `.task_outputs/` 目录

把这些重复逻辑抽出来后，三种范式脚本就能把注意力集中在各自的工作流上。
"""

from __future__ import annotations

import re
from pathlib import Path


CODE_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = CODE_ROOT / ".task_outputs"


def extract_code_block(text: str, preferred_language: str | None = None) -> str:
    """尽量从模型输出里提取 fenced code block。

    为什么要做这层提取？

    因为模型往往会在代码前后带一点解释文字。
    如果我们直接把整段回答写进 `.html` 文件，浏览器就会把解释文字也当成页面内容，
    演示时结果会很难看。

    `preferred_language` 只是一个“优先选择”提示，不是强约束。
    如果没找到指定语言的代码块，就回退到第一个代码块；
    如果一个都没有，再回退到原始文本。
    """

    code_blocks = list(
        re.finditer(r"```(?P<lang>[a-zA-Z0-9_-]*)\n(?P<body>.*?)```", text, re.DOTALL)
    )

    if not code_blocks:
        return text.strip()

    if preferred_language:
        for match in code_blocks:
            if match.group("lang").strip().lower() == preferred_language.lower():
                return match.group("body").strip()

    return code_blocks[0].group("body").strip()


def write_text_output(filename: str, content: str) -> Path:
    """把文本内容写到统一输出目录，并返回文件路径。"""

    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    output_path = OUTPUT_ROOT / filename
    output_path.write_text(content, encoding="utf-8")
    return output_path
