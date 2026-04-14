# 培训材料

这份目录现在是一套纯 demo 版培训材料，不再绑定任何课程章节或原书结构。

目标很简单：

- 只讲三种经典智能体工作流
- 只围绕一个统一任务展开
- 只保留方便现场演示和二次修改的最小代码

统一任务是：

> 生成一个单文件 `HTML + CSS + JavaScript` 贪吃蛇小游戏。

这样做的好处是：

- 任务背景足够轻
- 范式差异更容易横向对比
- 结果是否可用可以立刻验证

## 目录结构

- `markdown/`
  - `01_overview.md`：培训总览
  - `02_agent_paradigms.md`：三种范式讲解
  - `03_demo_walkthrough.md`：现场演示脚本
- `code/`
  - `common/`：配置、LLM 客户端、输出工具
  - `paradigms/`：三种范式的教学版实现
  - `standalone/`：可直接打开运行的参考版贪吃蛇网页

## 建议讲解顺序

1. 先讲 `markdown/01_overview.md`
2. 再讲 `markdown/02_agent_paradigms.md`
3. 最后按 `markdown/03_demo_walkthrough.md` 现场跑代码

## 代码特点

- 不照抄任何课程源码
- 不依赖课程上下文
- 注释偏讲解型，强调“为什么这样设计”
- 只需要配置 `API Base URL`、`API Key`、`Model` 即可运行
- 同时提供一个不依赖 API 的参考版网页

## 快速开始

```bash
cd /Users/sailv/IdeaProjects/agentStudy/training_materials/code
cp .env.example .env
pip install -r requirements.txt
```

运行三种范式 demo：

```bash
python paradigms/react_demo.py
python paradigms/plan_and_solve_demo.py
python paradigms/reflection_demo.py
```

如果你想先看一个直接可运行的结果：

```bash
open standalone/snake_reference.html
```
