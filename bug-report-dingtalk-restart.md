# Bug 报告：钉钉连接器无限重启循环

**日期：** 2026-03-12  
**严重级别：** 🔴 高（导致断连 + cron 任务失败）

---

## 问题描述

钉钉连接器陷入无限重启循环，导致：
1. 消息发送不稳定
2. Cron 任务频繁超时
3. 用户断连

---

## 根本原因

**两个独立的重启系统互相干扰：**

### 系统 1：Channel 自动重启
- **位置：** `gateway-cli-C2ZZYgwu.js:2523`
- **限制：** `MAX_RESTART_ATTEMPTS = 10` 次
- **策略：** 指数退避 (5s→11s→21s→43s→84s→163s→300s)

### 系统 2：Health-Monitor 健康检查
- **位置：** `gateway-cli-C2ZZYgwu.js:1706`
- **限制：** `maxRestartsPerHour = 10` 次/小时
- **检查间隔：** 每 5 分钟 (300 秒)
- **致命 Bug：** 重启时会调用 `resetRestartAttempts()` 重置系统 1 的计数器！

---

## 时间线证据

```
16:34:27 - Gateway 重启，钉钉连接器启动
16:34:32-16:37:39 - 连接器不断重启 (1→6)
16:39:52 - health-monitor 检测到"stopped"，强制重启 → 重置计数器为 1
16:40:22-16:46:03 - 连接器继续重启 (1→7)
16:49:52 - health-monitor 再次强制重启 → 重置计数器为 1
16:51:03-16:53:45 - 连接器继续重启 (1→6)
... 无限循环
```

---

## 代码位置

**Bug 代码：** `gateway-cli-C2ZZYgwu.js:1709`

```javascript
// health-monitor 重启逻辑
if (status.running) await channelManager.stopChannel(channelId, accountId);
channelManager.resetRestartAttempts(channelId, accountId);  // ❌ 这里重置了计数器！
await channelManager.startChannel(channelId, accountId);
```

---

## 修复建议

### 方案 A：移除 resetRestartAttempts 调用

```javascript
// 修改前（错误）
channelManager.resetRestartAttempts(channelId, accountId);
await channelManager.startChannel(channelId, accountId);

// 修改后（正确）
// 不调用 resetRestartAttempts，让 channel 自己的重启计数器正常工作
await channelManager.startChannel(channelId, accountId);
```

### 方案 B：协调两个系统

让 health-monitor 知道 channel 已经重启了多少次，避免重复重启。

---

## 影响范围

- **断连事故：** 用户断连一整天
- **Cron 任务失败：** 学习提醒、竞品分析等任务超时
- **消息发送不稳定：** 钉钉消息可能发送失败

---

## 临时解决方案

1. 禁用 health-monitor
2. 增加 cron 任务超时时间
3. 手动重启 Gateway

---

## 参考 Issue

- 类似 bug：[如有，填写链接]
- 相关文档：`docs.openclaw.ai/troubleshooting`

---

**报告人：** 小虾米 🦐  
**联系方式：** [用户自行填写]
