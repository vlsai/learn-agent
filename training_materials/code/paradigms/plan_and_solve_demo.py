"""教学版 Plan-and-Solve Agent。

这个脚本把“生成贪吃蛇网页”拆成三个职责清楚的组件：

1. `Planner` 负责拆步骤
2. `Executor` 负责逐步产出中间结果
3. `Composer` 负责合成为最终 HTML 文件

这样做的目的，是把“先拆再做”的范式特征显式展示出来。
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


CODE_ROOT = Path(__file__).resolve().parents[1]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from common.artifacts import extract_code_block, write_text_output
from common.llm_client import build_default_client
from paradigms.demo_data import SNAKE_TASK


DEFAULT_TASK = SNAKE_TASK


class Planner:
    """专门负责“先想清楚步骤”的组件。"""

    def __init__(self) -> None:
        self.llm = build_default_client()

    def plan(self, task: str) -> list[str]:
        """把任务拆成一个结构化步骤列表。"""

        prompt = f"""
你是一个教学版 Planner。
请把下面的开发任务拆成 4 到 6 个清晰步骤。

要求：
- 只输出 JSON 数组
- 每个元素都是一个字符串
- 不要输出 Markdown 代码块
- 不要输出任何额外解释
- 最后一步必须包含“合成最终 HTML 并检查可运行性”的意思

任务：
{task}
""".strip()

        raw = self.llm.chat(
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        print("\n===== Planner Output =====")
        print(raw)

        plan = json.loads(raw)
        if not isinstance(plan, list) or not all(
            isinstance(item, str) for item in plan
        ):
            raise ValueError("Planner 没有返回字符串列表。")
        return plan


class Executor:
    """专门负责“按计划一步一步执行”的组件。"""

    def __init__(self) -> None:
        self.llm = build_default_client()

    def run_step(
        self,
        task: str,
        full_plan: list[str],
        history: list[str],
        current_step: str,
    ) -> str:
        """执行计划中的单独一步。"""

        history_text = "\n".join(history) if history else "暂无已完成步骤。"

        prompt = f"""
你是一个教学版 Executor。
请严格围绕“当前步骤”输出结果。

原始任务：
{task}

完整计划：
{json.dumps(full_plan, ensure_ascii=False, indent=2)}

已完成的步骤结果：
{history_text}

当前步骤：
{current_step}

要求：
- 只输出当前步骤的结果
- 保持简洁明确
""".strip()

        return self.llm.chat(
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )


class PlanAndSolveAgent:
    """把 Planner 和 Executor 组合起来的教学版智能体。"""

    def __init__(self) -> None:
        self.planner = Planner()
        self.executor = Executor()
        self.composer = Composer()

    def run(self, task: str) -> str:
        plan = self.planner.plan(task)

        print("\n===== Structured Plan =====")
        for index, step in enumerate(plan, start=1):
            print(f"{index}. {step}")

        history: list[str] = []
        final_answer = ""

        for index, step in enumerate(plan, start=1):
            print(f"\n===== Execute Step {index} =====")
            print(f"Current Step: {step}")

            step_result = self.executor.run_step(
                task=task,
                full_plan=plan,
                history=history,
                current_step=step,
            )
            history.append(f"步骤 {index}: {step}\n结果: {step_result}")
            print(step_result)

        final_answer = self.composer.compose(task=task, plan=plan, history=history)
        html_code = extract_code_block(final_answer, preferred_language="html")
        output_path = write_text_output("plan_and_solve_snake.html", html_code)

        print("\n===== Final Output =====")
        print(final_answer)
        print(f"\nSaved to: {output_path}")
        return html_code


class Composer:
    """专门负责把中间结果合成为最终交付物的组件。"""

    def __init__(self) -> None:
        self.llm = build_default_client()

    def compose(self, task: str, plan: list[str], history: list[str]) -> str:
        """把执行阶段产生的中间结果合成为一个完整 HTML 文件。"""

        prompt = f"""
你是一个教学版 Composer。
请根据任务、计划和已完成步骤，输出最终的单文件贪吃蛇网页。

任务：
{task}

完整计划：
{json.dumps(plan, ensure_ascii=False, indent=2)}

已完成步骤结果：
{chr(10).join(history)}

要求：
- 只输出最终结果
- 最终结果必须包含 ```html 代码块
- 使用原生 HTML、CSS、JavaScript
- 代码注释清楚，适合培训讲解
""".strip()

        return self.llm.chat(
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            max_tokens=2200,
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="运行教学版 Plan-and-Solve demo。")
    parser.add_argument("--task", default=DEFAULT_TASK)
    args = parser.parse_args()

    agent = PlanAndSolveAgent()
    agent.run(args.task)


if __name__ == "__main__":
    main()
