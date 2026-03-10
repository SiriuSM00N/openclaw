# Model Router Skill - 模型自动路由

_根据任务内容自动选择最优模型_

---

## 🎯 用途

根据用户任务的关键词和复杂度，自动选择最适合的 LLM 模型。

---

## 📋 触发条件

当用户请求使用特定模型，或需要为子任务分配合适模型时。

---

## 🔄 路由规则

### 优先级匹配（从上到下）

```javascript
function selectModel(task) {
  const keywords = {
    coder: ["写代码", "函数", "类", "脚本", "实现", "重构", "TypeScript", "JavaScript", "模块", "API", "接口"],
    reviewer: ["审查", "找 bug", "优化", "阅读文档", "审计", "安全检查", "代码审查", "性能优化"],
    designer: ["设计", "架构", "系统", "数值", "配置", "公式", "数据结构", "游戏系统", "数值平衡"],
    critic: ["评估", "评审", "创意", "建议", "头脑风暴", "可行性", "方案评审", "批判"],
    light: ["什么是", "解释", "定义", "翻译", "摘要", "总结", "格式化", "整理"]
  };

  // 检查关键词匹配
  if (keywords.coder.some(k => task.includes(k))) return "bailian/qwen3-coder-plus";
  if (keywords.reviewer.some(k => task.includes(k))) return "moonshot/kimi-k2.5";
  if (keywords.designer.some(k => task.includes(k))) return "bailian/glm-5";
  if (keywords.critic.some(k => task.includes(k))) return "minimax/minimax-m2.5";
  
  // 架构类任务：只用 GLM-5
  if (task.includes("架构")) return "bailian/glm-5";
  
  // 简单任务判断
  if (task.length < 100 || keywords.light.some(k => task.includes(k))) {
    return "bailian/glm-4.7";
  }
  
  // 默认模型
  return "bailian/qwen3.5-plus";
}
```

---

## 📊 模型映射表

| 角色 | 模型 ID | 使用场景 |
|------|---------|----------|
| default | `bailian/qwen3.5-plus` | 日常对话、通用任务 |
| coder | `bailian/qwen3-coder-plus` | 写代码、重构 |
| reviewer | `moonshot/kimi-k2.5` | 代码审查、文档阅读 |
| designer | `bailian/glm-5` | 系统设计、数值规划 |
| critic | `minimax/minimax-m2.5` | 创意评估、批判分析 |
| light | `bailian/glm-4.7` | 简单查询、快速任务 |

---

## 🛠️ 使用方法

### 方式 1：手动指定模型别名

```
/codex 用 coder 模型写一个排序函数
/codex 用 reviewer 模型审查这段代码
/codex 用 designer 模型设计一个战斗系统
```

### 方式 2：自动路由（默认）

不指定模型时，自动根据任务内容选择。

### 方式 3：子任务分发

```javascript
// 复杂任务多模型协作
sessions_spawn({
  runtime: "acp",
  model: "bailian/glm-5",  // 设计阶段
  task: "设计游戏战斗系统"
});

sessions_spawn({
  runtime: "acp", 
  model: "bailian/qwen3-coder-plus",  // 实现阶段
  task: "实现战斗系统代码"
});

sessions_spawn({
  runtime: "acp",
  model: "moonshot/kimi-k2.5",  // 审查阶段
  task: "审查战斗系统代码"
});
```

---

## 💡 使用示例

### 示例 1：写代码
```
用户：写一个快速排序函数
→ 自动路由 → bailian/qwen3-coder-plus
```

### 示例 2：系统设计
```
用户：设计一个 RPG 游戏的装备系统
→ 自动路由 → bailian/glm-5
```

### 示例 3：代码审查
```
用户：帮我审查这段代码有没有 bug
→ 自动路由 → moonshot/kimi-k2.5
```

### 示例 4：简单查询
```
用户：什么是闭包？
→ 自动路由 → bailian/glm-4.7
```

### 示例 5：日常对话
```
用户：今天天气怎么样？
→ 自动路由 → bailian/qwen3.5-plus (默认)
```

---

## 📝 注意事项

1. **手动优先**：用户明确指定模型时，覆盖自动路由
2. **复杂任务协作**：大任务可拆分为多个子任务，用不同模型处理
3. **成本意识**：简单任务用轻量模型，节省 Token
4. **质量优先**：关键任务（代码、设计）用专业模型

---

## 🔧 配置扩展

如需添加新模型或调整规则，修改 `MODEL_ROUTING.md` 并更新此技能。

---

_版本：1.0 | 最后更新：2026-03-10_ 🦐
