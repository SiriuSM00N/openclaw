# Smart Search Skill

智能搜索引擎选择器 — 自动在 Brave Search 和 Tavily 之间选择最佳工具。

## 📁 文件结构

```
smart-search/
├── SKILL.md              # 技能定义（OpenClaw 读取）
├── tavily-search.sh      # Tavily CLI 工具
└── README.md             # 本文档
```

## 🚀 快速开始

### 1. 确认配置

Tavily API Key 应该已经在 `~/.openclaw/.env` 中：

```bash
cat ~/.openclaw/.env | grep TAVILY
```

### 2. 测试 CLI 工具

```bash
cd /Users/sirius/.openclaw/workspace/skills/smart-search
./tavily-search.sh "AI development trends 2026"
```

### 3. 在 OpenClaw 中使用

现在和我对话时，我会自动根据任务类型选择搜索引擎：

**简单查询** → Brave Search（默认）
```
"今天有什么新闻"
"谁是特斯拉的 CEO"
```

**复杂研究** → Tavily
```
"帮我调研最适合独立游戏开发的项目管理工具"
"对比 Notion 和 Obsidian 的优缺点"
```

## 📊 引擎选择逻辑

| 场景 | 引擎 | 原因 |
|------|------|------|
| 事实查询 | Brave | 快速、无限免费 |
| 新闻/时事 | Brave | 实时性好 |
| 深度研究 | Tavily | AI 优化、内容完整 |
| 对比分析 | Tavily | 结构化数据 |
| 学术搜索 | Tavily | 精准度高 |
| 日常搜索 | Brave | 节省 Tavily 配额 |

## 🔧 CLI 用法

```bash
# 基本搜索
./tavily-search.sh "your query"

# 指定结果数量（1-10）
./tavily-search.sh "your query" 10

# 指定搜索深度（basic|advanced）
./tavily-search.sh "your query" 5 advanced
```

## 📈 配额管理

Tavily 免费计划：**1000 次/月**

查看用量：https://app.tavily.com/home

**节省配额的技巧：**
1. 简单查询用 Brave
2. 设置 `max_results: 3-5` 而不是默认值
3. 相关搜索合并为一次查询
4. 配额紧张时自动降级到 Brave

## 🛠️ 故障排除

**问题：** `TAVILY_API_KEY not set`

**解决：**
```bash
export TAVILY_API_KEY=tvly-dev-xxxxx
# 或添加到 ~/.openclaw/.env
```

**问题：** CLI 工具无法执行

**解决：**
```bash
chmod +x tavily-search.sh
```

**问题：** jq 未安装

**解决：**
```bash
brew install jq
```

---

**创建日期：** 2026-03-10  
**版本：** 1.0  
**维护者：** 小虾米 🦐
