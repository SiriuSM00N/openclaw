# tabbit-flow — Tabbit 工作流自动化技能

_白嫖 Tabbit 公测免费模型 + OpenClaw 自动化辅助_

---

## 📖 简介

**Tabbit** 是一个 AI 浏览器扩展，提供 14 个免费模型的上下文感知对话能力。

**tabbit-flow 技能** 将 Tabbit 内容生成与 OpenClaw 自动化能力结合，实现：
- Tabbit 负责：模型调用、内容生成
- OpenClaw 负责：文件存储、Cron 提醒、钉钉推送、Git 操作、记忆索引

---

## 🎯 适用场景

当你需要：
- ✅ 使用多个免费 LLM 模型（GPT-5.2/Claude/Gemini/MiniMax 等）
- ✅ 批量处理网页内容（总结/提取/对比）
- ✅ 自动化后续步骤（存储/推送/索引/Git）
- ✅ 定时提醒执行固定工作流

---

## 🚀 快速开始

### 安装后第一步

```bash
# 1. 确认 Tabbit 浏览器扩展已安装
# 2. 确认 OpenClaw 钉钉连接器已配置
# 3. 运行初始化命令
openclaw skill tabbit-flow init
```

---

## 📋 6 个工作流

### 1️⃣ 每日新闻收集（10 分钟）

**Tabbit 侧：**
1. 打开 Tabbit → 选 Gemini-Pro
2. 打开 3-5 个新闻网站标签页
3. 输入：`@所有标签页 总结今日 AI 新闻`
4. 保存到 `memory/news/YYYY-MM-DD.md`

**OpenClaw 侧：**
- Cron 每天 8:00 自动提醒
- 读取新闻文件 → 格式化 → 钉钉推送
- 索引到记忆系统

**触发命令：**
```bash
openclaw skill tabbit-flow news --date today
```

---

### 2️⃣ 代码生成（15 分钟）

**Tabbit 侧：**
1. 打开 Tabbit → 选 GPT-5.2
2. 输入需求（自然语言）
3. 复制代码 → 保存为 `.py`/`.js` 文件

**OpenClaw 侧：**
- 读取代码文件 → 运行测试
- Git 提交 + 推送
- 钉钉通知

**触发命令：**
```bash
openclaw skill tabbit-flow code --file ~/projects/xxx.py --test
```

---

### 3️⃣ 创意写作（20 分钟）

**Tabbit 侧：**
1. 打开 Tabbit → 选 MiniMax-M2.5
2. 输入 Prompt（小红书笔记模板）
3. 人工修改润色
4. 保存为 `drafts/xxx.md`

**OpenClaw 侧：**
- 读取草稿 → 发布到各平台（需配置）
- 钉钉提醒

**触发命令：**
```bash
openclaw skill tabbit-flow draft --file drafts/xxx.md --publish
```

---

### 4️⃣ 网页抓取（10 分钟）

**Tabbit 侧：**
1. 打开 Tabbit → 选 Gemini-Pro
2. 打开目标文章
3. 输入：`@当前标签页 提取文章信息`
4. 保存为 `memory/articles/xxx.md`

**OpenClaw 侧：**
- 索引到记忆系统
- 更新相关文档

**触发命令：**
```bash
openclaw skill tabbit-flow article --file memory/articles/xxx.md --index
```

---

### 5️⃣ 竞品调研（25 分钟）

**Tabbit 侧：**
1. 打开 Tabbit → 选 Claude-Sonnet
2. 打开 5-10 个竞品页面
3. 输入：`@所有标签页 对比分析`
4. 保存为 `research/xxx.md`

**OpenClaw 侧：**
- 索引到记忆系统
- 更新 MEMORY.md 竞品章节
- 钉钉通知

**触发命令：**
```bash
openclaw skill tabbit-flow research --file research/xxx.md --update-memory
```

---

### 6️⃣ 翻译（5 分钟）

**Tabbit 侧：**
1. 打开 Tabbit → 选 DeepSeek-V3.2
2. 粘贴待翻译内容
3. 输入：`翻译为{语言}`
4. 保存为 `translations/xxx.md`

**OpenClaw 侧：**
- 存储到翻译库
- 索引到记忆系统

**触发命令：**
```bash
openclaw skill tabbit-flow translate --file translations/xxx.md --lang zh
```

---

## ⚙️ 配置

### Cron 提醒配置

```bash
# 启用每日新闻收集提醒（8:00）
openclaw skill tabbit-flow cron --enable news

# 启用学习提醒（21:00）
openclaw skill tabbit-flow cron --enable study

# 列出所有 Cron 配置
openclaw skill tabbit-flow cron --list
```

### 钉钉推送配置

在 `TOOLS.md` 中确认：
```markdown
### 钉钉
- **用户 ID：** `sirius997`
- **推送目标：** 私聊 + 群聊（可选）
```

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
└── skills/tabbit-flow/
    ├── SKILL.md        # 本文件
    ├── scripts/
    │   ├── news.sh     # 新闻处理脚本
    │   ├── code.sh     # 代码测试脚本
    │   └── index.sh    # 记忆索引脚本
    └── templates/
        ├── news.md     # 新闻模板
        └── article.md  # 文章模板
```

---

## 🔧 命令参考

| 命令 | 功能 |
|------|------|
| `tabbit-flow init` | 初始化（创建目录 + 配置 Cron） |
| `tabbit-flow news` | 处理每日新闻 |
| `tabbit-flow code` | 处理代码生成 |
| `tabbit-flow draft` | 处理创意写作 |
| `tabbit-flow article` | 处理网页抓取 |
| `tabbit-flow research` | 处理竞品调研 |
| `tabbit-flow translate` | 处理翻译 |
| `tabbit-flow cron` | 管理 Cron 提醒 |
| `tabbit-flow status` | 查看工作状态 |

---

## 📊 工作流统计

**已配置：**
- ✅ Cron 任务：每天 8:00 新闻收集提醒
- ✅ 目录结构：6 个工作流目录
- ✅ 集成文档：workflows/tabbit-integration.md

**推荐优先使用：**
1. 每日新闻收集（10 分钟）→ Cron 已配置
2. 代码生成（15 分钟）→ 生成后自动测试 + 提交

---

## ⚠️ 注意事项

1. **Tabbit 是公测免费** — 政策可能变化，定期检查
2. **内容需人工审核** — Tabbit 生成的内容需确认后再发布
3. **文件保存路径** — 必须保存到指定目录才能触发自动化
4. **钉钉推送** — 需确认钉钉连接器正常运行

---

## 📝 更新记录

| 日期 | 版本 | 更新内容 |
|------|------|----------|
| 2026-03-12 | 1.0.0 | 初始版本，6 个工作流 + Cron 配置 |

---

_最后更新：2026-03-12_ 🦐
