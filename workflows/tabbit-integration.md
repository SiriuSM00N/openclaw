# Tabbit + OpenClaw 配合工作流

_白嫖 Tabbit 公测免费模型 + OpenClaw 自动化辅助_

---

## 📊 分工原则

| 任务 | Tabbit | OpenClaw |
|------|--------|----------|
| 模型调用 | ✅ 14 个免费模型 | ❌ 不调用 |
| 内容生成 | ✅ 对话/写作/代码 | ❌ 不生成 |
| 文件存储 | ❌ 不存储 | ✅ 保存到 workspace |
| 定时任务 | ❌ 无 Cron | ✅ 定时提醒/执行 |
| 通知推送 | ❌ 无钉钉 | ✅ 钉钉推送 |
| Git 操作 | ❌ 无 | ✅ 自动提交推送 |
| 记忆索引 | ❌ 无 | ✅ 索引到 memory/ |

---

## 📋 6 个工作流配置

### 工作流 1：代码生成（15 分钟）

**Tabbit 侧：**
1. 打开 Tabbit → 选 GPT-5.2
2. 输入需求（自然语言）
3. 等待生成（15 秒）
4. 复制代码 → 保存为 `.py`/`.js` 文件

**OpenClaw 侧：**
```bash
# 保存后告诉小虾米
"代码已保存到 ~/projects/xxx.py，帮我运行测试并提交"
```
- 读取代码文件
- 运行测试
- Git 提交 → 推送
- 发送钉钉通知

---

### 工作流 2：创意写作（20 分钟）

**Tabbit 侧：**
1. 打开 Tabbit → 选 MiniMax-M2.5
2. 输入 Prompt（小红书笔记模板）
3. 等待生成（15 秒）
4. 人工修改润色
5. 复制终稿 → 保存为 `.md` 文件

**OpenClaw 侧：**
```bash
# 保存后告诉小虾米
"笔记已保存到 drafts/xxx.md，帮我发布到各平台"
```
- 读取草稿文件
- 发布到各平台（需配置）
- 发送钉钉提醒

---

### 工作流 3：每日新闻收集（10 分钟）

**Tabbit 侧：**
1. 打开 Tabbit → 选 Gemini-Pro
2. 打开 3-5 个新闻网站标签页
3. 输入：`@所有标签页 总结今日 AI 新闻`
4. 等待生成（15 秒）
5. 导出摘要 → 保存为 `memory/news/YYYY-MM-DD.md`

**OpenClaw 侧：**
- Cron 每天 8:00 提醒：`该收集今日新闻了`
- 读取新闻文件
- 格式化 → 发送钉钉摘要
- 索引到记忆系统

---

### 工作流 4：网页抓取（10 分钟）

**Tabbit 侧：**
1. 打开 Tabbit → 选 Gemini-Pro
2. 打开目标文章
3. 输入：`@当前标签页 提取文章信息`
4. 等待生成（15 秒）
5. 复制 → 保存为 `memory/articles/xxx.md`

**OpenClaw 侧：**
- 读取文章摘要
- 索引到记忆系统
- 更新相关文档

---

### 工作流 5：竞品调研（25 分钟）

**Tabbit 侧：**
1. 打开 Tabbit → 选 Claude-Sonnet
2. 搜索竞品关键词，打开 5-10 个页面
3. 输入：`@所有标签页 对比分析`
4. 等待生成（30 秒）
5. 导出对比表格 + 报告 → 保存为 `research/xxx.md`

**OpenClaw 侧：**
- 读取报告
- 索引到记忆系统
- 更新 MEMORY.md 竞品章节
- 发送钉钉通知

---

### 工作流 6：翻译（5 分钟）

**Tabbit 侧：**
1. 打开 Tabbit → 选 DeepSeek-V3.2
2. 粘贴待翻译内容
3. 输入：`翻译为{语言}`
4. 等待生成（12 秒）
5. 复制译文 → 保存为 `translations/xxx.md`

**OpenClaw 侧：**
- 存储到翻译库
- 索引到记忆系统

---

## 📁 文件结构

```
~/.openclaw/workspace-default/
├── drafts/              # 创意写作草稿
├── research/            # 竞品调研报告
├── translations/        # 翻译内容
├── memory/
│   ├── news/           # 每日新闻
│   └── articles/       # 文章摘要
└── workflows/
    └── tabbit-integration.md  # 本文件
```

---

## ⏰ Cron 配置（可选）

### 每日新闻收集提醒

```json
{
  "name": "Tabbit 新闻收集提醒",
  "schedule": {
    "kind": "cron",
    "expr": "0 8 * * *",
    "tz": "Asia/Shanghai"
  },
  "payload": {
    "kind": "systemEvent",
    "text": "【💡 提醒】该收集今日 AI 新闻了！\n\n1. 打开 Tabbit\n2. 选 Gemini-Pro\n3. 打开 3-5 个新闻网站\n4. 输入：@所有标签页 总结今日 AI 新闻\n5. 保存到 memory/news/YYYY-MM-DD.md"
  },
  "sessionTarget": "main",
  "delivery": {
    "mode": "announce",
    "to": "user:sirius997"
  }
}
```

---

## 🚀 快速开始

**今天就可以用：**

1. **每日新闻收集**（10 分钟）
   - 打开 Tabbit → Gemini-Pro
   - @所有标签页 总结今日 AI 新闻
   - 保存到 `memory/news/2026-03-12.md`
   - 告诉我，我帮你格式化 + 推送钉钉

2. **代码生成**（15 分钟）
   - 打开 Tabbit → GPT-5.2
   - 描述需求，生成代码
   - 保存到 `projects/xxx.py`
   - 告诉我，我帮你测试 + 提交

---

_最后更新：2026-03-12_ 🦐
