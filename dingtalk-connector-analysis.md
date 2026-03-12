# 钉钉连接器无限重启问题分析报告

**日期：** 2026-03-12  
**作者：** 小虾米 🦐  
**来源：** 官方文档 + 本次事故调查

---

## 📋 问题描述

**症状：**
- 钉钉连接器不断重启（`auto-restart attempt 1/10 ~ 7/10`）
- 重启间隔指数增长（5s→11s→21s→43s→84s→163s→300s）
- 用户断连，消息发送失败
- Cron 任务频繁超时

---

## 🔍 官方文档故障排除方法

### 第一步：60 秒快速诊断

```bash
openclaw status
openclaw status --all
openclaw gateway probe
openclaw gateway status
openclaw doctor
openclaw channels status --probe
openclaw logs --follow
```

**正常输出：**
- `Runtime: running`
- `RPC probe: ok`
- Channel 显示 `connected` 或 `ready`
- 日志无重复致命错误

### 第二步：决策树

```
OpenClaw 不工作
├── 无回复 → 检查 pairing list 和 allowlist
├── Dashboard 连不上 → 检查 gateway status
├── Gateway 不启动 → 检查 doctor
├── Channel 连接但消息不流动 → 检查 logs
├── Cron 不触发 → 检查 cron list 和 logs
└── Node 配对失败 → 检查 pairing list
```

---

## 🐛 本次事故根本原因

### 问题定位

**两个独立的重启系统互相干扰：**

| 系统 | 位置 | 限制 | 问题 |
|------|------|------|------|
| Channel 自动重启 | `gateway-cli-C2ZZYgwu.js:2523` | 10 次 | 计数器被重置 |
| Health-Monitor | `gateway-cli-C2ZZYgwu.js:1706` | 10 次/小时 | 重置 Channel 计数器 |

### 代码级 Bug

**位置：** `gateway-cli-C2ZZYgwu.js:1709`

```javascript
// health-monitor 重启逻辑（错误）
if (status.running) await channelManager.stopChannel(channelId, accountId);
channelManager.resetRestartAttempts(channelId, accountId);  // ❌ 这里重置了计数器！
await channelManager.startChannel(channelId, accountId);
```

**后果：**
- Channel 永远达不到 `MAX_RESTART_ATTEMPTS = 10`
- Health-Monitor 每 10 分钟重启一次
- 无限循环

---

## 🔧 解决方案对比

### 方案 A：禁用 Health-Monitor（本次采用）

**操作：**
```json
{
  "gateway": {
    "channelHealthCheckMinutes": 0
  }
}
```

**优点：**
- ✅ 立即生效
- ✅ 简单直接
- ✅ 不会误重启

**缺点：**
- ❌ 失去自动健康检查
- ❌ 需要手动监控

**适用场景：** 临时修复，等官方修复

---

### 方案 B：修改 Health-Monitor 代码（需要官方修复）

**操作：** 移除 `resetRestartAttempts()` 调用

```javascript
// 修改后（正确）
if (status.running) await channelManager.stopChannel(channelId, accountId);
// 不调用 resetRestartAttempts
await channelManager.startChannel(channelId, accountId);
```

**优点：**
- ✅ 根本修复
- ✅ 保留健康检查功能

**缺点：**
- ❌ 需要修改源码
- ❌ 需要官方发布新版本

**适用场景：** 官方修复后升级

---

### 方案 C：增加 Channel 重启上限（临时方案）

**操作：** 修改源码 `MAX_RESTART_ATTEMPTS = 20`

**优点：**
- ✅ 延长重启周期

**缺点：**
- ❌ 不解决根本问题
- ❌ 需要修改源码

**适用场景：** 不推荐

---

## 📊 类似 Channel 问题对比

### WhatsApp/Telegram/Discord 常见问题

| 问题 | 症状 | 解决方案 |
|------|------|---------|
| 配对失败 | 连接但无回复 | `openclaw pairing list <channel>` 检查并批准 |
| Allowlist 拦截 | DM 被阻止 | 添加 sender ID 到 allowFrom |
| 网络问题 | 随机断开重连 | 检查 DNS/代理路由 |
| 凭证过期 | 登录循环 | 重新登录，验证凭证目录 |

### 钉钉特有问题

| 问题 | 症状 | 解决方案 |
|------|------|---------|
| Stream 客户端断开 | `auto-restart attempt` | 禁用 health-monitor（临时） |
| 消息去重失败 | 重复处理同一消息 | 检查 `processedMessages` 缓存 |
| 会话隔离问题 | 多用户上下文泄露 | 设置 `session.dmScope` |

---

## 🎯 推荐的故障排除流程

### 钉钉连接器专用

```bash
# 1. 检查状态
openclaw status
openclaw channels status --probe

# 2. 检查日志（关键！）
tail -100 /tmp/openclaw/openclaw-*.log | grep -E "dingtalk|auto-restart|health-monitor"

# 3. 检查配对
openclaw pairing list dingtalk-connector

# 4. 检查配置
openclaw config get channels.dingtalk-connector

# 5. 实时监控
openclaw logs --follow | grep dingtalk
```

### 日志关键字

| 关键字 | 含义 | 处理 |
|--------|------|------|
| `auto-restart attempt` | 连接器重启 | 检查是否无限循环 |
| `health-monitor: restarting` | 健康检查触发重启 | 考虑禁用 |
| `DM 被拦截` | Allowlist 阻止 | 添加用户 ID |
| `connect success` | 连接成功 | 正常 |
| `GatewayDrainingError` | Gateway 重启中 | 等待完成 |

---

## 📝 本次事故处理总结

### 时间线

| 时间 | 事件 | 响应 |
|------|------|------|
| 2026-03-11 16:34 | Gateway 重启，钉钉连接器开始循环 | 未及时发现 |
| 2026-03-11 22:26 | 学习提醒任务超时 | 用户通知 |
| 2026-03-11 23:00 | 深入调查日志 | 找到根本原因 |
| 2026-03-11 23:30 | 执行三方案修复 | 禁用 health-monitor + 增加超时 + Bug 报告 |
| 2026-03-11 23:40 | 系统恢复稳定 | 持续监控 |

### 教训

1. **主动监控不足** — 应该有心跳检查 cron 状态
2. **第一次回复糊弄** — 应该直接查日志而不是说表面原因
3. **没及时写入记忆** — 用户说"记住"要立刻写进 MEMORY.md
4. **没全渠道验证** — 钉钉记住了，PC 端没同步

---

## 🔮 后续建议

### 短期（本周）

1. **保持 health-monitor 禁用** — 观察稳定性
2. **手动监控 cron 任务** — 每天检查 `cron list`
3. **提交 Bug 报告** — GitHub Issue 或 Discord

### 中期（本月）

1. **等待官方修复** — 关注 OpenClaw 更新
2. **设置告警** — cron 失败时主动通知
3. **增加日志保留** — 便于事后分析

### 长期（下季度）

1. **多通道冗余** — 钉钉 + 微信 + 邮件备份
2. **自动化监控** — 心跳 + 健康检查
3. **定期演练** — 模拟故障，测试恢复流程

---

## 📚 参考资源

- OpenClaw 官方文档：https://docs.openclaw.ai/
- 故障排除：https://docs.openclaw.ai/troubleshooting
- Channel 故障排除：https://docs.openclaw.ai/channels/troubleshooting
- GitHub Issues: https://github.com/openclaw/openclaw/issues
- Discord 社区：https://discord.com/invite/clawd

---

**报告完成时间：** 2026-03-12  
**下次更新：** 官方修复发布后

🦐
