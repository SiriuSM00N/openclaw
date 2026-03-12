# 技能详细清单

_最后更新：2026-03-12_

---

## 📦 已安装技能

| 技能名 | 版本 | 安装日期 | 位置 | 用途 | 依赖/配置 | 状态 |
|--------|------|----------|------|------|-----------|------|
| smart-search | - | 2026-03-10 | `skills/smart-search/` | 智能搜索（Tavily） | TAVILY_API_KEY | ✅ 活跃 |
| model-router | - | 2026-03-10 | `skills/model-router/` | 模型自动路由 | - | ✅ 活跃 |
| exa-search | - | 2026-03-12 | `skills/exa-search/` | Exa AI 搜索 | EXA_API_KEY | ✅ 活跃 |
| agent-reach | 1.1.0 | 2026-03-12 | `~/.openclaw/skills/skills/skills/panniantong/agent-reach/` | 全网搜索（14 平台） | 部分渠道需额外配置 | ✅ 8/14 渠道可用 |
| clawfeed | - | 2026-03-12 | `skills/clawfeed/` | AI 新闻摘要 | 运行中 :8767 | ✅ 活跃 |
| ai-skills/deep-research | - | 2026-03-12 | `skills/ai-skills/skills/deep-research/` | Multi Search Engine | - | ✅ 已克隆 |
| x-reader | - | 2026-03-12 | `skills/x-reader/` | X/Twitter 阅读 | - | ✅ 已克隆 |
| browserwing | - | 2026-03-12 | `skills/browserwing/` | 浏览器自动化 | - | ✅ 已克隆 |
| modsearch | - | 2026-03-12 | `skills/modsearch/` | 模块化搜索 | - | ✅ 已克隆 |
| tabbit-flow | 1.0.0 | 2026-03-12 | `skills/tabbit-flow/` | Tabbit 工作流自动化 | 钉钉连接器 + Cron | ✅ 已安装 |

## 🛠️ 自研工具（2026-03-12 新增）

| 工具名 | 位置 | 用途 | 依赖 | 状态 |
|--------|------|------|------|------|
| memory-dedup | `scripts/memory-dedup.py` | 记忆去重索引 | Python 3 | ✅ 已测试 |
| memory-watcher | `scripts/memory-watcher.py` | 文件监听自动索引 | watchdog | ✅ 已安装 |

### 工具使用说明

**memory-dedup（去重索引）：**
```bash
# 手动索引
python3 scripts/memory-dedup.py ./memory/

# 输出：
# - 新增/修改的文件 → 自动索引
# - 无变化的文件 → 跳过（去重）
# - 已删除的文件 → 清理 chunk
```

**memory-watcher（文件监听）：**
```bash
# 后台监听
python3 scripts/memory-watcher.py ./memory/ &

# 功能：
# - 文件修改 → 1.5 秒后自动索引
# - 文件删除 → 自动清理 chunk
# - 防抖处理 → 避免频繁写入
```

**索引文件：** `memory/.index.json`
- 存储 chunk 哈希和元数据
- 自动创建，无需手动编辑
- 定期清理（季度归档时）

---

## 🔍 功能对比表

### 搜索类技能

| 功能 | smart-search | exa-search | agent-reach | 推荐场景 |
|------|--------------|------------|-------------|----------|
| 通用搜索 | ✅ Tavily | ✅ Exa | ✅ Exa | smart-search（免费） |
| 技术/学术 | ⚠️ 一般 | ✅ 强 | ✅ 强 | exa-search |
| 社交媒体 | ❌ | ❌ | ✅ 14 平台 | agent-reach |
| 新闻摘要 | ❌ | ❌ | ⚠️ 需配置 | clawfeed |
| 深度研究 | ✅ Tavily | ⚠️ 一般 | ❌ | smart-search |

### 模型路由

| 模型 | 角色 | 使用场景 |
|------|------|----------|
| Qwen3.5-Plus | default | 日常对话、通用任务（60%） |
| Qwen3-Coder-Plus | coder | 写代码、重构（15%） |
| GLM-5 | designer | 系统设计、数值规划（10%） |
| Kimi-K2.5 | reviewer | 代码审查、文档阅读（8%） |
| MiniMax-M2.5 | critic | 创意评估、批判分析（5%） |
| GLM-4.7 | light | 简单查询、快速任务（2%） |

---

## 🗑️ 弃用/替换记录

（暂无）

---

## 📝 安装流程规范

### 安装前检查清单

1. **检查是否已安装**
   ```bash
   ls ~/.openclaw/workspace/skills/ | grep <skill-name>
   ```
2. **检查功能重叠**
   - 查阅本文件"功能对比表"
   - 评估是否需要新功能
3. **评估依赖复杂度**
   - 是否需要 API Key？
   - 是否需要额外服务（Docker、数据库等）？
   - Python/Node 版本要求？

### 安装后强制步骤

1. **立即更新本文件**
   - 添加到"已安装技能"表格
   - 填写完整信息（版本、日期、位置、依赖、状态）
2. **更新 MEMORY.md（精简版）**
   - 添加技能名 + 状态
3. **测试功能**
   - 运行技能的基本功能测试
   - 记录测试结果

### 卸载/替换流程

1. **记录弃用原因**
2. **标注替代技能**
3. **清理配置文件**
4. **更新本文件"弃用记录"**

---

## 📊 统计信息

- **已安装技能：** 10 个
- **待安装技能：** 2 个
- **弃用技能：** 0 个
- **安装完成率：** 83%（10/12）

---

_维护规则：每次安装/卸载技能后，必须立即更新此文件_ 🦐
