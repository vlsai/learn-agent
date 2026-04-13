# 教学版代码说明

这份代码不是照搬原仓库，而是为了培训演示重新写的教学版实现。

## 设计原则

- 保留核心思想
- 刻意减少工程噪声
- 注释尽量写清楚“为什么这么做”
- 默认用 OpenAI 兼容接口，方便接任何兼容服务

## 目录结构

- `common/`
  - 通用配置和 LLM 客户端
- `paradigms/`
  - 三种经典范式的教学版实现
- `claude_code_s01_s06/`
  - `learn-claude-code` 前 6 章的最小示例

## 启动前配置

1. 复制环境变量模板：

```bash
cp .env.example .env
```

2. 填写以下配置：

```bash
LLM_API_KEY=你的密钥
LLM_BASE_URL=你的接口地址
LLM_MODEL=你的模型名
```

3. 安装依赖：

```bash
pip install -r requirements.txt
```

## 推荐先跑什么

如果你只想先确认环境可用，先跑：

```bash
python paradigms/react_demo.py
```

如果这个脚本能正常返回结果，说明 API 配置基本是通的。
