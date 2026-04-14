"""教学版 LLM 客户端。

这里刻意只保留一个最常用的 `chat()` 接口，
让培训时的注意力尽量停留在“工作流怎么设计”，
而不是被 SDK 细节打散。
"""

from __future__ import annotations

from typing import Any

from openai import OpenAI

from common.config import AppConfig


class TeachingLLMClient:
    """面向培训场景的最小聊天客户端。"""

    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self.client = OpenAI(
            api_key=config.api_key,
            base_url=config.base_url,
            timeout=config.timeout,
        )

    def chat(
        self,
        messages: list[dict[str, Any]],
        temperature: float = 0.2,
        max_tokens: int = 1500,
    ) -> str:
        """向模型发送一轮对话，并返回纯文本结果。

        这里使用最直白的聊天接口。
        这样范式 demo 可以把“工具调用、规划、反思”的控制权留在 Python 代码里，
        更适合教学时逐步拆开讲。
        """

        response = self.client.chat.completions.create(
            model=self.config.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        message = response.choices[0].message
        return (message.content or "").strip()


def build_default_client() -> TeachingLLMClient:
    """构造一个读取默认环境变量的客户端。"""

    config = AppConfig.from_env()
    return TeachingLLMClient(config)
