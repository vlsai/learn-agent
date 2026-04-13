"""教学版 Reflection Agent。

这个脚本演示的重点不是“写出世界上最强的代码”，
而是让听众看清 Reflection 的基本节奏：

1. 先生成第一版
2. 再生成批评意见
3. 再根据批评意见重写

运行方式：

```bash
python paradigms/reflection_demo.py
```
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


CODE_ROOT = Path(__file__).resolve().parents[1]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from common.llm_client import build_default_client


DEFAULT_TASK = (
    "编写一个 Python 函数，返回 1 到 n 之间所有素数组成的列表。"
    "代码要适合培训讲解：结构清晰、边界条件明确、注释详细。"
)


class Memory:
    """教学版记忆模块。

    Reflection 中的记忆很重要，因为第二轮、第三轮都必须看见前面的轨迹。
    这里使用最简单的列表保存历史记录，足够培训演示。
    """

    def __init__(self) -> None:
        self.records: list[dict[str, str]] = []

    def add(self, record_type: str, content: str) -> None:
        self.records.append({"type": record_type, "content": content})

    def last_execution(self) -> str:
        for record in reversed(self.records):
            if record["type"] == "execution":
                return record["content"]
        raise ValueError("记忆里还没有 execution 记录。")


class ReflectionAgent:
    """教学版 Reflection Agent。"""

    CODE_BLOCK_PATTERN = re.compile(r"```(?:python)?\n(.*?)```", re.DOTALL)

    def __init__(self, max_iterations: int = 2) -> None:
        self.llm = build_default_client()
        self.memory = Memory()
        self.max_iterations = max_iterations

    def _extract_code(self, text: str) -> str:
        """尽量从模型输出中提取代码块。

        如果模型没有老老实实给 Markdown 代码块，
        就退而求其次直接返回原文。
        """

        match = self.CODE_BLOCK_PATTERN.search(text)
        if match:
            return match.group(1).strip()
        return text.strip()

    def _initial_draft(self, task: str) -> str:
        prompt = f"""
你是一名适合做培训讲解的 Python 工程师。
请完成下面的任务，并且只输出代码：

任务：
{task}

要求：
- 包含函数签名
- 处理边界条件
- 注释足够详细，方便课堂讲解
""".strip()

        raw = self.llm.chat([{"role": "user", "content": prompt}], temperature=0.2)
        return self._extract_code(raw)

    def _reflect(self, task: str, code: str) -> str:
        prompt = f"""
你是一位非常严格的代码评审员。
请只从下面四个角度审查代码：

1. 讲解是否清晰
2. 边界条件是否完整
3. 算法是否足够适合教学
4. 注释是否真的帮助理解

如果你认为已经足够好，请明确输出：无需继续改进

原始任务：
{task}

待审查代码：
```python
{code}
```
""".strip()

        return self.llm.chat([{"role": "user", "content": prompt}], temperature=0.2)

    def _refine(self, task: str, code: str, feedback: str) -> str:
        prompt = f"""
你是一名 Python 工程师。
请根据下面的评审意见重写代码，并且只输出最终代码。

原始任务：
{task}

当前代码：
```python
{code}
```

评审意见：
{feedback}
""".strip()

        raw = self.llm.chat([{"role": "user", "content": prompt}], temperature=0.2)
        return self._extract_code(raw)

    def run(self, task: str) -> str:
        print("===== Initial Draft =====")
        draft = self._initial_draft(task)
        self.memory.add("execution", draft)
        print(draft)

        for iteration in range(1, self.max_iterations + 1):
            print(f"\n===== Reflection Round {iteration} =====")
            latest_code = self.memory.last_execution()
            feedback = self._reflect(task, latest_code)
            self.memory.add("reflection", feedback)
            print(feedback)

            if "无需继续改进" in feedback:
                print("\n===== Final Code =====")
                print(latest_code)
                return latest_code

            print("\n===== Refined Draft =====")
            refined = self._refine(task, latest_code, feedback)
            self.memory.add("execution", refined)
            print(refined)

        final_code = self.memory.last_execution()
        print("\n===== Final Code =====")
        print(final_code)
        return final_code


def main() -> None:
    parser = argparse.ArgumentParser(description="运行教学版 Reflection demo。")
    parser.add_argument("--task", default=DEFAULT_TASK)
    args = parser.parse_args()

    agent = ReflectionAgent()
    agent.run(args.task)


if __name__ == "__main__":
    main()
