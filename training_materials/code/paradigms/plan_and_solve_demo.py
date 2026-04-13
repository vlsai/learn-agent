"""教学版 Plan-and-Solve Agent。

这个脚本重点演示两件事：

1. 先规划，再执行
2. 规划器和执行器是两个职责明确的组件

运行方式：

```bash
python paradigms/plan_and_solve_demo.py
```
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


CODE_ROOT = Path(__file__).resolve().parents[1]
if str(CODE_ROOT) not in sys.path:
    sys.path.insert(0, str(CODE_ROOT))

from common.llm_client import build_default_client


DEFAULT_QUESTION = (
    "请为一次 45 分钟的组内培训设计讲解议程，"
    "内容必须包含 ReAct、Plan-and-Solve、Reflection 三种构建方式，"
    "以及 learn-claude-code 前 6 章的讲解安排。"
)


class Planner:
    """专门负责“想清楚步骤”的组件。"""

    def __init__(self) -> None:
        self.llm = build_default_client()

    def plan(self, question: str) -> list[str]:
        """把用户问题拆成一个结构化步骤列表。"""

        prompt = f"""
你是一个教学版 Planner。
请把下面的问题拆成 4 到 6 个清晰步骤。

要求：
- 只输出 JSON 数组
- 每个元素都是一个字符串
- 不要输出 Markdown 代码块
- 不要输出任何额外解释

问题：
{question}
""".strip()

        raw = self.llm.chat(
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        print("\n===== Planner Output =====")
        print(raw)

        # 培训里可以顺便讲一个工程习惯：
        # 只要你要求模型输出结构化结果，就要立刻做解析与校验。
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
        question: str,
        full_plan: list[str],
        history: list[str],
        current_step: str,
    ) -> str:
        """执行计划中的单独一步。"""

        history_text = "\n".join(history) if history else "暂无已完成步骤。"

        prompt = f"""
你是一个教学版 Executor。
请严格围绕“当前步骤”输出结果。

原始问题：
{question}

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

    def run(self, question: str) -> str:
        plan = self.planner.plan(question)

        print("\n===== Structured Plan =====")
        for index, step in enumerate(plan, start=1):
            print(f"{index}. {step}")

        history: list[str] = []
        final_answer = ""

        for index, step in enumerate(plan, start=1):
            print(f"\n===== Execute Step {index} =====")
            print(f"Current Step: {step}")

            step_result = self.executor.run_step(
                question=question,
                full_plan=plan,
                history=history,
                current_step=step,
            )
            history.append(f"步骤 {index}: {step}\n结果: {step_result}")
            final_answer = step_result
            print(step_result)

        print("\n===== Final Output =====")
        print(final_answer)
        return final_answer


def main() -> None:
    parser = argparse.ArgumentParser(description="运行教学版 Plan-and-Solve demo。")
    parser.add_argument("--question", default=DEFAULT_QUESTION)
    args = parser.parse_args()

    agent = PlanAndSolveAgent()
    agent.run(args.question)


if __name__ == "__main__":
    main()
