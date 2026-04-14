# 教学版代码说明

这份代码只为一件事服务：

> 用最小、最清楚、最方便演示的方式，讲清三种经典智能体范式。

所有脚本都围绕同一个目标任务：

> 生成一个单文件 `HTML + CSS + JavaScript` 贪吃蛇小游戏。

## 设计原则

- 不绑定课程章节
- 不照抄现成工程源码
- 只保留讲解范式真正需要的结构
- 注释重点解释“为什么这样设计”
- 默认使用 OpenAI 兼容接口

## 目录结构

- `common/`
  - 配置读取
  - LLM 客户端
  - 输出文件保存与代码提取
- `paradigms/`
  - `react_demo.py`
  - `plan_and_solve_demo.py`
  - `reflection_demo.py`
  - `demo_data.py`
  - `tools.py`
- `standalone/`
  - `snake_reference.html`

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

## 推荐讲解顺序

1. 先打开 `standalone/snake_reference.html`，让听众看到目标长什么样
2. 再跑 `react_demo.py`，讲“边查边做”
3. 再跑 `plan_and_solve_demo.py`，讲“先拆再做”
4. 最后跑 `reflection_demo.py`，讲“先做再改”

## 运行命令

```bash
python paradigms/react_demo.py
python paradigms/plan_and_solve_demo.py
python paradigms/reflection_demo.py
```

生成的文件会写到：

```bash
code/.task_outputs/
```
