# 现场演示脚本

这份脚本用于培训现场边讲边跑。

## 演示顺序

### 第一段：三种范式

```bash
cd /Users/sailv/IdeaProjects/agentStudy/training_materials/code
python paradigms/react_demo.py
python paradigms/plan_and_solve_demo.py
python paradigms/reflection_demo.py
```

#### 讲解提示

- 跑 ReAct 时，重点讲循环、工具、Observation 回流
- 跑 Plan-and-Solve 时，重点讲 Planner 和 Executor 的分离
- 跑 Reflection 时，重点讲“初稿 -> 评审 -> 重写”的质量提升机制

### 第二段：learn-claude-code 前 6 章

```bash
python claude_code_s01_s06/s01_agent_loop_minimal.py
python claude_code_s01_s06/s02_tool_dispatch_minimal.py
python claude_code_s01_s06/s03_todo_manager_minimal.py
python claude_code_s01_s06/s04_subagent_minimal.py
python claude_code_s01_s06/s05_skill_loader_minimal.py
python claude_code_s01_s06/s06_context_compact_minimal.py
```

#### 讲解提示

- `s01` 看主循环如何推进
- `s02` 看工具如何注册而不是写死
- `s03` 看计划状态如何显式存在
- `s04` 看父子上下文如何隔离
- `s05` 看 skill 为什么要懒加载
- `s06` 看为什么输出要压缩和持久化

## 现场建议准备的问题

### 用于 ReAct

- “前 6 章里哪一章首次引入子智能体？”
- “前三章分别解决了什么问题？”

### 用于 Plan-and-Solve

- “请为一场 45 分钟培训设计议程，必须包含三种范式与前 6 章概览。”

### 用于 Reflection

- “写一个求 1 到 n 所有素数的函数，并把第一版优化到更适合演示和讲解。”

## 培训时最容易卡住的点

1. 听众把范式当成“模型能力”，而不是“任务组织方式”
2. 听众把 todo 当成完整任务平台
3. 听众把子智能体理解成“为了并发”，而忽略上下文隔离
4. 听众把上下文压缩理解成“删除历史”，而不是“保留连续性地缩写历史”

## 收尾时建议总结

最后可以统一收口成一句话：

> 这 6 章和三种范式合在一起，构成了一个教学版 Agent 系统最重要的骨架：  
> 主循环、工具、计划、子任务、知识加载、上下文管理。
