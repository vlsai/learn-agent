# 现场演示说明

这份文档可以在培训现场直接照着走。

统一演示目标：

> 用三种不同工作流，生成一个单文件贪吃蛇网页。

## 演示前准备

```bash
cd /Users/sailv/IdeaProjects/agentStudy/training_materials/code
cp .env.example .env
pip install -r requirements.txt
```

在 `.env` 中填写：

```bash
LLM_API_KEY=你的密钥
LLM_BASE_URL=你的接口地址
LLM_MODEL=你的模型名
```

## 预热演示

如果你想先给大家看最终效果长什么样，可以直接打开：

```bash
open standalone/snake_reference.html
```

这个文件是离线可运行的参考版，不代表某一种范式，只是方便先建立共同预期。

## 第一段：ReAct

```bash
python paradigms/react_demo.py
```

讲解重点：

- 模型先思考，再查本地说明，再继续推理
- `Action` 触发工具
- 工具结果会回流成 `Observation`
- 最终结果会写到 `.task_outputs/react_snake.html`

建议现场强调：

> ReAct 的关键不是工具调用本身，而是工具结果能否驱动下一轮推理。

## 第二段：Plan-and-Solve

```bash
python paradigms/plan_and_solve_demo.py
```

讲解重点：

- 先生成计划，再按步骤执行
- 规划阶段和执行阶段职责不同
- 每一步只解决当前子问题
- 最终结果会写到 `.task_outputs/plan_and_solve_snake.html`

建议现场强调：

> Plan-and-Solve 的核心价值是把复杂任务拆成更稳定的生产流程。

## 第三段：Reflection

```bash
python paradigms/reflection_demo.py
```

讲解重点：

- 先做第一版
- 再做严格评审
- 再按评审意见重写
- 最终结果会写到 `.task_outputs/reflection_snake.html`

建议现场强调：

> Reflection 的价值不是多调用一次模型，而是把“看起来能用”提升成“更可靠、更适合交付”。

## 横向对比时可以问的问题

1. 如果需求在做的过程中还会变化，哪种方式更自然
2. 如果任务天然有明显阶段，哪种方式更稳
3. 如果你最担心隐藏 bug，哪种方式更适合放在最后一层

## 收尾时建议总结

你可以直接用下面这段话收尾：

> ReAct 适合边查边做，Plan-and-Solve 适合先拆再做，Reflection 适合先做再改。  
> 它们不是互斥路线，而是三种可以组合的工作流积木。
