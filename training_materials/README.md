# 培训材料

这份目录是为组内培训单独整理的教学材料，目标不是完整复刻原仓库，而是把核心概念重新组织成更适合讲解、演示和二次修改的版本。

## 目录结构

- `markdown/`
  - 培训讲义、学习地图、现场演示脚本
- `code/`
  - 可直接运行的教学版示例代码
  - 包含三种经典智能体构建方式
  - 包含 `learn-claude-code` 前 6 章的最小示例代码

## 建议讲解顺序

1. 先讲 `markdown/01_overview.md`
2. 再讲 `markdown/02_agent_paradigms.md`
3. 然后讲 `markdown/03_learn_claude_code_s01_s06.md`
4. 最后按 `markdown/04_demo_walkthrough.md` 现场跑代码

## 代码特点

- 不是照抄原仓库源码
- 结构刻意简化，方便现场讲解
- 注释非常详细，适合边看边讲
- 只需要配置 `API Base URL`、`API Key` 和 `Model` 即可启动需要大模型的 demo

## 快速开始

进入代码目录：

```bash
cd /Users/sailv/IdeaProjects/agentStudy/training_materials/code
```

复制环境变量模板：

```bash
cp .env.example .env
```

安装依赖：

```bash
pip install -r requirements.txt
```

运行三种范式 demo：

```bash
python paradigms/react_demo.py
python paradigms/plan_and_solve_demo.py
python paradigms/reflection_demo.py
```

运行 `learn-claude-code` 前 6 章最小示例：

```bash
python claude_code_s01_s06/s01_agent_loop_minimal.py
python claude_code_s01_s06/s02_tool_dispatch_minimal.py
python claude_code_s01_s06/s03_todo_manager_minimal.py
python claude_code_s01_s06/s04_subagent_minimal.py
python claude_code_s01_s06/s05_skill_loader_minimal.py
python claude_code_s01_s06/s06_context_compact_minimal.py
```
