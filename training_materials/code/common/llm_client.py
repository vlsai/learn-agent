"""教学版 LLM 客户端。

这个版本刻意做得很小，原因不是它已经“最好”，而是它更适合培训演示：

- 只有一个类
- 只有一个最常用的 `chat()` 方法
- 输出和异常处理尽量直白

等听众理解完主干结构后，再扩展流式输出、重试、日志、监控、缓存都更自然。
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

        这里使用 `chat.completions` 而不是更复杂的工具调用协议，
        是为了让培训中可以把注意力放在“工作流设计”而不是 SDK 细节上。
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
    """构造一个使用默认环境变量的客户端。

    这样各个 demo 文件只要一行代码就能拿到可用客户端：

    ```python
    llm = build_default_client()
    ```
    """

    config = AppConfig.from_env()
    return TeachingLLMClient(config)
