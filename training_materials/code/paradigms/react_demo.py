"""教学版 ReAct Agent。

这个脚本只做一件事：

> 用 ReAct 工作流生成一个单文件贪吃蛇网页。

这里刻意保留最传统的文本协议：

- `Thought`
- `Action`
- `Observation`
- `Final Answer`

因为这种写法最适合培训现场逐行讲解。
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


# 为了让脚本可以直接从命令行运行，这里显式把 code 根目录加进 Python 路径。
# 这不是最优雅的工程写法，但它对培训演示很友好：
# 听众不需要先理解 package 安装和模块导入细节。
CODE_ROOT = Path(__file__).resolve().parents[1]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from common.artifacts import extract_code_block, write_text_output
from common.llm_client import build_default_client
from paradigms.demo_data import SNAKE_TASK
from paradigms.tools import render_tool_descriptions, run_tool


DEFAULT_TASK = SNAKE_TASK


class TeachingReActAgent:
    """一个非常小的 ReAct Agent。

    这个类故意保留了最经典的文本格式解析方式，
    因为它更适合教学：

    - 听众能直接看见模型输出长什么样
    - 听众能理解 Action 是如何被解析的
    - 听众也能顺便理解这种方案为什么比较脆弱
    """

    ACTION_PATTERN = re.compile(
        r"Action:\s*(?P<tool>[a-zA-Z_][a-zA-Z0-9_]*)\[(?P<input>.*)\]",
        re.DOTALL,
    )
    FINAL_PATTERN = re.compile(r"Final Answer:\s*(?P<answer>.*)", re.DOTALL)

    def __init__(self, max_steps: int = 5) -> None:
        self.llm = build_default_client()
        self.max_steps = max_steps

    def _build_system_prompt(self) -> str:
        """构造 system prompt。

        这份 prompt 最重要的部分不是“华丽措辞”，而是输出格式约束。
        因为没有格式约束，主循环就很难稳定解析模型结果。
        """

        return f"""
你是一个教学版 ReAct Agent。
你的任务是交付一个可直接保存为 `.html` 文件的单文件贪吃蛇网页。

可用工具如下：
{render_tool_descriptions()}

你每一轮只能做下面两种事情之一：

1. 如果还需要工具，就严格输出：
Thought: 你的思考
Action: 工具名[工具输入]

2. 如果你已经可以回答，就严格输出：
Thought: 你的思考
Final Answer: 你的最终回答

请注意：
- 不要同时输出 Action 和 Final Answer
- 工具输入不要再套引号
- 在给出 Final Answer 之前，至少调用一次工具
- 最终答案必须包含一个 ```html 代码块
- 代码必须是原生 HTML、CSS、JavaScript 的单文件实现
""".strip()

    def _build_user_prompt(self, task: str, scratchpad: str) -> str:
        """构造 user prompt。

        `scratchpad` 是 ReAct 教学版里最关键的状态之一。
        它记录了前面几轮已经产生的 Thought / Action / Observation。
        """

        return f"""
当前任务：
{task}

已有工作轨迹：
{scratchpad if scratchpad else "暂无。请开始第一步思考。"}
""".strip()

    def _parse_response(self, response: str) -> tuple[str | None, str | None]:
        """从模型返回文本里解析出 Action 或 Final Answer。

        返回值约定如下：

        - `(tool_name, tool_input)`：说明模型要调用工具
        - `(None, final_answer)`：说明模型已经给出最终答案

        这种解析方案很适合教学，因为直观；
        但培训时也应该顺带强调：它比结构化 JSON / 函数调用更脆弱。
        """

        final_match = self.FINAL_PATTERN.search(response)
        if final_match:
            return None, final_match.group("answer").strip()

        action_match = self.ACTION_PATTERN.search(response)
        if action_match:
            tool_name = action_match.group("tool").strip()
            tool_input = action_match.group("input").strip()
            return tool_name, tool_input

        raise ValueError(
            "模型输出既没有 Final Answer，也没有合法 Action，无法继续。"
        )

    def run(self, task: str) -> str:
        """运行完整的 ReAct 主循环。"""

        scratchpad = ""
        used_tool = False

        for step in range(1, self.max_steps + 1):
            print(f"\n===== ReAct Step {step} =====")

            response = self.llm.chat(
                messages=[
                    {"role": "system", "content": self._build_system_prompt()},
                    {
                        "role": "user",
                        "content": self._build_user_prompt(task, scratchpad),
                    },
                ],
                temperature=0.1,
            )
            print(response)

            tool_name, payload = self._parse_response(response)

            if tool_name is None:
                if not used_tool:
                    raise RuntimeError("模型没有先调用工具，ReAct demo 无法体现闭环。")

                html_code = extract_code_block(payload, preferred_language="html")
                output_path = write_text_output("react_snake.html", html_code)

                print("\n===== Final Answer =====")
                print(payload)
                print(f"\nSaved to: {output_path}")
                return html_code

            observation = run_tool(tool_name, payload)
            used_tool = True
            print("\n----- Observation -----")
            print(observation)

            scratchpad += (
                f"{response}\n"
                f"Observation: {observation}\n"
            )

        raise RuntimeError("超过最大步数仍未得到最终答案。")


def main() -> None:
    parser = argparse.ArgumentParser(description="运行教学版 ReAct demo。")
    parser.add_argument("--task", default=DEFAULT_TASK)
    args = parser.parse_args()

    agent = TeachingReActAgent()
    agent.run(args.task)


if __name__ == "__main__":
    main()
