# CRON_CONFIG.md - 定时任务配置文档

_结构化配置规范 + 失败通知机制_

---

## 📋 配置原则（方案 B）

虽然 OpenClaw cron 不支持 `defaults` 继承，但我们保持**结构化一致性**：

### 统一字段规范

```json
{
  "agentId": "main",                    // 统一使用 main agent
  "sessionKey": "agent:main:main",      // 统一 session
  "sessionTarget": "isolated",          // 隔离执行
  "wakeMode": "now",                    // 立即唤醒
  "delivery": {
    "mode": "direct",                   // 直接发送
    "channel": "dingtalk-connector",    // 钉钉渠道
    "to": "user:333446632538210751"     // 目标用户
  }
}
```

### 差异化字段

每个任务只差异化以下内容：
- `id` - 唯一标识
- `name` - 任务名称
- `schedule` - 执行时间
- `payload.message` - 任务指令
- `payload.timeoutSeconds` - 超时时间

---

## 📊 当前任务列表

| ID | 名称 | 时间 | Timeout | 状态 |
|----|------|------|---------|------|
| `7f1c2e47...` | 早安资讯 - AI 游戏 | 每天 8:00 | 900s | ✅ |
| `1ad11520...` | 游戏策划学习提醒 | 每天 21:00 | 600s | ✅ |
| `98e80e0f...` | 每周记忆回顾 | 每周日 21:00 | 1200s | ✅ |
| `1d8e060e...` | 竞品分析监控 | 每周一 8:00 | 1800s | ✅ |
| `54b0508d...` | Cron 失败监控 | 每 30 分钟 | 300s | ✅ 新增 |

---

## 🚨 失败通知机制

### 监控任务配置

**任务 ID：** `54b0508d-dfa5-464e-9bbb-8d59cb3b7cb5`

**执行频率：** 每 30 分钟

**检查逻辑：**
1. 调用 `cron list` 获取所有任务
2. 检查 `state.consecutiveErrors > 0` 或 `state.lastRunStatus = 'error'`
3. 如果失败 → 发送钉钉通知
4. 如果正常 → 回复 `HEARTBEAT_OK`

### 失败通知格式

```
🚨 **Cron 任务失败通知**

| 任务 | 错误 | 时间 |
|------|------|------|
| {name} | {error} | {time} |

**建议操作：**
- 查看日志：`tail -50 /tmp/openclaw/openclaw-*.log`
- 手动重试：`openclaw cron run <jobId>`
- 检查配置：`openclaw cron list`
```

---

## ⏱️ Timeout 标准

| 任务类型 | Timeout | 理由 |
|----------|---------|------|
| 资讯收集（3-5 条） | 900s (15 分钟) | 搜索 + 整理 + 推送 |
| 学习提醒（互动） | 600s (10 分钟) | 等待用户回复 + 简单处理 |
| 竞品分析（周报） | 1800s (30 分钟) | 多站点搜索 + 分析 |
| 记忆回顾（周任务） | 1200s (20 分钟) | 读取多文件 + 整理 |
| 监控检查 | 300s (5 分钟) | 快速检查 + 通知 |

---

## 🔧 管理命令

### 查看任务
```bash
openclaw cron list
```

### 查看运行历史
```bash
openclaw cron runs --id <jobId>
```

### 手动触发
```bash
openclaw cron run <jobId>
```

### 禁用/启用
```bash
openclaw cron disable <jobId>
openclaw cron enable <jobId>
```

### 删除任务
```bash
openclaw cron rm <jobId>
```

---

## 📝 更新记录

| 日期 | 操作 | 说明 |
|------|------|------|
| 2026-03-11 23:25 | 修复 delivery 配置 | `recipient` → `to: "user:xxx"` |
| 2026-03-11 23:33 | 方案 B 重构 | 统一配置结构 |
| 2026-03-11 23:33 | 添加失败监控 | 每 30 分钟检查 |
| 2026-03-11 23:33 | 优化 timeout | 学习提醒 300s→600s，竞品分析 3600s→1800s |
| 2026-03-11 23:54 | **P0+P1 全部完成** | 7 项检查清单 + 验证清单 + 自动触发 |
| 2026-03-11 23:54 | 添加验证清单 | 4 个任务 payload 增加验证要求 |
| 2026-03-11 23:54 | 更新 MEMORY.md | 添加常见失败模式章节 |

---

## 🎯 P0+P1 完成清单

### P0（高价值、低成本）
- ✅ 7 项检查清单 → `HEARTBEAT.md`
- ✅ 失败复盘模板 → `CASES.md`
- ✅ 先做后问原则 → `AGENTS.md`
- ✅ 自动触发逻辑 → `prompts/pua.md` + `AGENTS.md`
- ✅ 失败监控优化 → Cron Job #54b0508d

### P1（中价值、中成本）
- ✅ 端到端验证标准 → 4 个 Cron 任务 payload
- ✅ 失败模式记录 → `MEMORY.md`
- ✅ 主动诊断清单 → `HEARTBEAT.md`（Cron 健康检查）

---

## 📊 预期收益（更新）

| 指标 | 基线 | 目标 | 当前状态 |
|------|------|------|----------|
| Cron 任务成功率 | ~75% | 95%+ | 🟡 待验证 |
| 失败复盘覆盖率 | 0% | 100% | ✅ 模板就绪 |
| 无效提问减少 | - | 50%+ | 🟡 待验证 |
| 问题发现时间 | 用户发现 | 自动监控 | ✅ 30 分钟检查 |

---

_最后更新：2026-03-11 23:54_ 🦐
