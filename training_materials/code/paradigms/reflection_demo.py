"""教学版 Reflection Agent。

这个脚本把 Reflection 范式压缩成最容易看懂的三段：

1. 先生成第一版贪吃蛇网页
2. 再做严格评审
3. 再根据反馈重写

它非常适合讲“为什么多花一轮模型调用，结果可能会更稳”。
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


CODE_ROOT = Path(__file__).resolve().parents[1]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from common.artifacts import extract_code_block, write_text_output
from common.llm_client import build_default_client
from paradigms.demo_data import SNAKE_TASK


DEFAULT_TASK = SNAKE_TASK


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

    def __init__(self, max_iterations: int = 2) -> None:
        self.llm = build_default_client()
        self.memory = Memory()
        self.max_iterations = max_iterations

    def _initial_draft(self, task: str) -> str:
        prompt = f"""
你是一名适合做培训讲解的前端工程师。
请完成下面的任务，并且只输出最终代码：

任务：
{task}

要求：
- 输出一个单文件 HTML
- 内嵌 CSS 和 JavaScript
- 注释足够详细，方便课堂讲解
""".strip()

        raw = self.llm.chat([{"role": "user", "content": prompt}], temperature=0.2)
        return extract_code_block(raw, preferred_language="html")

    def _reflect(self, task: str, code: str) -> str:
        prompt = f"""
你是一位非常严格的前端代码评审员。
请只从下面五个角度审查代码：

1. 玩法是否完整
2. 碰撞和重开逻辑是否可靠
3. 页面是否适合培训展示
4. 代码结构是否容易讲解
5. 注释是否真的帮助理解

如果你认为已经足够好，请明确输出：无需继续改进

原始任务：
{task}

待审查代码：
```html
{code}
```
""".strip()

        return self.llm.chat([{"role": "user", "content": prompt}], temperature=0.2)

    def _refine(self, task: str, code: str, feedback: str) -> str:
        prompt = f"""
你是一名前端工程师。
请根据下面的评审意见重写代码，并且只输出最终代码。

原始任务：
{task}

当前代码：
```html
{code}
```

评审意见：
{feedback}
""".strip()

        raw = self.llm.chat([{"role": "user", "content": prompt}], temperature=0.2)
        return extract_code_block(raw, preferred_language="html")

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
                output_path = write_text_output("reflection_snake.html", latest_code)
                print("\n===== Final Code =====")
                print(latest_code)
                print(f"\nSaved to: {output_path}")
                return latest_code

            print("\n===== Refined Draft =====")
            refined = self._refine(task, latest_code, feedback)
            self.memory.add("execution", refined)
            print(refined)

        final_code = self.memory.last_execution()
        output_path = write_text_output("reflection_snake.html", final_code)
        print("\n===== Final Code =====")
        print(final_code)
        print(f"\nSaved to: {output_path}")
        return final_code


def main() -> None:
    parser = argparse.ArgumentParser(description="运行教学版 Reflection demo。")
    parser.add_argument("--task", default=DEFAULT_TASK)
    args = parser.parse_args()

    agent = ReflectionAgent()
    agent.run(args.task)


if __name__ == "__main__":
    main()
