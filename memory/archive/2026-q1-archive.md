# 2026-Q1 归档内容

_创建日期：2026-03-12_

---

## 📦 技能安装优先级列表（2026-03-12）

**来源：** 卡尔的 AI 沃茨 (@aiwarts) X 推文
**推文链接：** https://x.com/aiwarts/status/2028841167186727154

**背景：** 2026-03-12 集中安装的技能优先级列表，用于指导当天的安装工作。

### 完整优先级列表

| 优先级 | 技能 | 安装命令/链接 | 最终状态 |
|--------|------|---------------|----------|
| 1 | ClawHub | `npm i -g clawhub` | ✅ 已安装 |
| 2 | Tavily | `clawhub install tavily-search` | ✅ API Key 已配置 |
| 3 | Agent-Reach | GitHub: Panniantong/Agent-Reach | ✅ 已安装（8/14 渠道可用） |
| 4 | ClawFeed | GitHub: kevinho/clawfeed | ✅ 已安装（运行中） |
| 5 | Multi Search Engine | GitHub: sanjay3290/ai-skills/deep-research | ✅ 已克隆 |
| 6 | x-reader | GitHub: runesleo/x-reader | ✅ 已克隆 |
| 7 | BrowserWing | GitHub: browserwing/browserwing | ✅ 已克隆 |
| 8 | ModSearch | GitHub: liustack/modsearch | ✅ 已克隆 |
| 9 | Free Ride | ClawHub: Shaivpidadi/free-ride | ⏳ 需认证 |
| 10 | find-skills | `clawhub install find-skills` | ⏳ 需认证 |

### 安装结果

**完成率：** 80%（8/10）

**已完成：**
- ClawHub、Tavily、Agent-Reach、ClawFeed
- Multi Search Engine、x-reader、BrowserWing、ModSearch

**待完成：**
- Free Ride（需 GitHub 认证）
- find-skills（需 ClawHub/GitHub 认证）

### 经验教训

1. **会话重启丢失记忆** — 安装后未立即记录，导致重复安装
2. **ClawHub 限流** — 需要错开安装或改用 git clone
3. **Python 版本限制** — Python 3.9 不支持 mcp 包（需要 3.10+）
4. **GitHub 认证** — 部分仓库需要认证才能 clone

### 后续改进

- 创建 `memory/skills.md` 详细技能清单
- 创建 `MEMORY.md` 精简版技能清单
- 建立安装流程规范（安装前检查 + 安装后强制记录）
- 设置季度归档维护 cron 任务

---

## 📝 归档说明

**归档日期：** 2026-03-12
**归档原因：** 临时性任务列表，完成后失去活跃价值
**保留价值：** 经验教训、安装流程改进参考

---

_此文件归档自 MEMORY.md，保留历史记录供未来参考_ 🦐
