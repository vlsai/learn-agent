"""教学版配置加载模块。

这份配置模块保持极小，原因不是功能已经完整，
而是培训代码更应该让听众先看懂依赖关系。

在这套 demo 里，所有需要调用模型的脚本都共享同一组配置：

- `LLM_API_KEY`
- `LLM_BASE_URL`
- `LLM_MODEL`

这样做的目的，是把“业务逻辑”和“环境配置”明确分开。
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


# 这里故意把 .env 放在 code 根目录下，避免听众在培训现场找不到配置文件。
CODE_ROOT = Path(__file__).resolve().parents[1]
ENV_FILE = CODE_ROOT / ".env"


# 如果 .env 存在，就自动加载；不存在也不报错，方便教学时先看代码再补配置。
load_dotenv(ENV_FILE)


@dataclass
class AppConfig:
    """教学版 demo 使用的最小配置集合。"""

    api_key: str
    base_url: str
    model: str
    timeout: int = 120

    @classmethod
    def from_env(cls) -> "AppConfig":
        """从环境变量中读取配置。

        这里不做太多花哨逻辑，原因很简单：
        培训代码最重要的是让听众能一眼看懂“启动依赖哪些配置”。
        """

        api_key = os.getenv("LLM_API_KEY", "").strip()
        base_url = os.getenv("LLM_BASE_URL", "").strip()
        model = os.getenv("LLM_MODEL", "").strip()
        timeout = int(os.getenv("LLM_TIMEOUT", "120"))

        if not api_key:
            raise ValueError(
                "缺少 LLM_API_KEY。请先在 code/.env 中填写你的 API Key。"
            )
        if not base_url:
            raise ValueError(
                "缺少 LLM_BASE_URL。请先在 code/.env 中填写你的 API 地址。"
            )
        if not model:
            raise ValueError(
                "缺少 LLM_MODEL。请先在 code/.env 中填写你的模型名称。"
            )

        return cls(
            api_key=api_key,
            base_url=base_url,
            model=model,
            timeout=timeout,
        )
