"""s04 最小示例：子智能体。"""

from __future__ import annotations


FILES = {
    "pyproject.toml": """
[tool.pytest.ini_options]
testpaths = ["tests"]
""".strip(),
    "requirements.txt": """
pytest==8.3.2
python-dotenv==1.0.1
""".strip(),
}


def run_subagent(prompt: str) -> str:
    """运行一个极简子智能体。

    这里不模拟完整 LLM，只强调“独立上下文”这件事：

    - 父智能体有自己的 messages
    - 子智能体也有自己的 messages
    - 子智能体读文件后的中间过程不会自动写回父上下文
    """

    sub_messages = [{"role": "user", "content": prompt}]
    print(f"子智能体初始上下文: {sub_messages}")

    findings = []
    if "测试框架" in prompt:
        if "pytest" in FILES["requirements.txt"]:
            findings.append("requirements.txt 中声明了 pytest")
        if "pytest" in FILES["pyproject.toml"]:
            findings.append("pyproject.toml 中也出现了 pytest 配置")

    # 子智能体最后只返回总结，而不是把所有内部中间过程都带回去。
    return "；".join(findings) or "没有找到明确信息"


def demo() -> None:
    parent_messages = [
        {"role": "user", "content": "这个项目用什么测试框架？"}
    ]
    print(f"父智能体上下文: {parent_messages}")

    summary = run_subagent("请检查项目里使用了什么测试框架，并返回一句总结。")
    parent_messages.append({"role": "tool_result", "content": summary})

    print("\n父智能体只拿回总结：")
    print(parent_messages)


if __name__ == "__main__":
    demo()
