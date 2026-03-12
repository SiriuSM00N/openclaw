# 待办事项

_最后更新：2026-03-12_

---

## 🔴 高优先级（本周）

### [ ] 准备水产市场发布材料
- **截止：** 2026-03-19
- **类型：** Experience
- **内容：** 记忆优化完整方案（去重 + 监听 + 归档）
- **任务清单：**
  - [ ] 写符合规范的 README.md（含标题 + 描述）
  - [ ] 准备打包脚本（zip/tar.gz）
  - [ ] 测试发布流程
  - [ ] 正式发布到 openclawmp.cc
- **差异化：** SHA-256 去重、实时监听、季度归档
- **参考：** 已有"跨会话记忆连续性"技能（184 次安装）

### [x] 配置 GitHub 认证
- **截止：** 2026-03-19
- **状态：** ✅ 已完成
- **任务清单：**
  - [x] 创建配置指南（`scripts/github-auth-guide.md`）
  - [x] 生成 GitHub Token（用户操作）
  - [x] 配置 Git 凭证（用户操作）
  - [x] 测试克隆 find-skills
  - [x] 安装 find-skills ✅
  - [x] 安装 Free Ride ⚠️ 已卸载（保守选择）
- **指南位置：** `scripts/github-auth-guide.md`
- **备注：** Free Ride 因需要 API Key 已卸载，find-skills 保留使用

---

## 🟡 中优先级（本月）

### [ ] 实施 Agent 自主进化方案（阶段 1）
- **截止：** 2026-03-19
- **状态：** 准备执行
- **任务清单：**
  - [ ] 创建 `memory/skill-gaps.md`（能力缺口记录）
  - [ ] 更新 HEARTBEAT.md 添加信号采集
  - [ ] 更新每周待办检查 cron（添加资产使用统计）
- **观察期：** 2026-03-12 ~ 2026-03-19（1 周）
- **下周讨论：** 是否增加自动化 cron（信号采集 + 每日复盘）

### [ ] 完善记忆优化工具
- **截止：** 2026-03-31
- **任务清单：**
  - [ ] 添加统计功能（`--stats` 参数）
  - [ ] 添加搜索功能（基于索引的关键词搜索）
  - [ ] 添加清理功能（`--clean` 参数）
  - [ ] 收集使用反馈，优化稳定性

### [ ] 配置 Brave API Key
- **截止：** 2026-03-31
- **原因：** web_search 工具需要
- **步骤：**
  - [ ] 申请 API Key（https://brave.com/search/api/）
  - [ ] 配置到 `.env` 文件
  - [ ] 测试搜索功能

---

## 🟢 低优先级（以后）

### [ ] 跟踪 Cron isolated bug 官方修复进度
- **截止：** 2026-04-12（1 个月后）
- **状态：** 等待官方修复
- **相关 Issues：**
  - #42632: `cron sessionTarget="isolated" + agentTurn can time out on a minimal prompt`
  - #26390: `[Bug] Isolated cron jobs timeout even when task is still running`
  - #41783: `bug(cron): job timeout includes cron-lane queue wait time`
  - #37505: `Cron job timeout aborts entire model fallback chain via shared AbortController`
- **当前状态：** 3 个任务已临时改用 `main` + `systemEvent`
- **修复后行动：**
  - [ ] 验证官方修复已发布（检查 OpenClaw 更新日志）
  - [ ] 将 3 个任务改回 `isolated` + `agentTurn`
  - [ ] 测试验证稳定性
  - [ ] 更新 CASES.md 记录

### [ ] 跟踪 Health-Monitor 无限重启 bug 官方修复
- **截止：** 2026-04-12（1 个月后）
- **状态：** 等待官方修复
- **Bug 描述：** health-monitor 重启 channel 时调用 `resetRestartAttempts()`，导致无限重启循环
- **代码位置：** `gateway-cli-*.js:1709`（`resetRestartAttempts` 调用）
- **当前状态：** `channelHealthCheckMinutes: 0`（已禁用）
- **修复后行动：**
  - [ ] 验证官方修复已发布（检查更新日志是否提到 health-monitor 或 resetRestartAttempts）
  - [ ] 恢复配置：`channelHealthCheckMinutes: 5`
  - [ ] 观察 24 小时确认无无限重启
  - [ ] 更新 CASES.md 记录
  - [ ] 更新 CASES.md 记录
- **检查频率：** 每周一次（周一早上）
- **提醒方式：** 钉钉 + webchat

### [ ] 实施 Agent 自主进化方案（阶段 2）
- **截止：** 2026-03-26
- **状态：** 等待观察期结束（2026-03-19）
- **前提：** 阶段 1 观察效果良好
- **任务清单：**
  - [ ] 评估信号采集效果（误报/漏报情况）
  - [ ] 评估资产使用统计效果
  - [ ] 决定是否增加自动化 cron
    - [ ] 信号采集 cron（每天 18:00）
    - [ ] 每日复盘 cron（每天 10:00）
  - [ ] 配置 auto_install 参数（永远 ask）
- **讨论日期：** 2026-03-19（观察期结束）

### [ ] 实施水产市场贡献家方案（阶段 3）
- **截止：** 2026-04-02
- **状态：** 等待阶段 2 完成
- **前提：** 阶段 1-2 运行稳定
- **任务清单：**
  - [ ] 测试手动提炼流程（不自动化）
  - [ ] 验证质量评分标准
  - [ ] 验证安全扫描流程
  - [ ] 决定是否创建每日扫描 cron（每天 22:00）
  - [ ] 配置 publish_mode（永远 ask）
- **讨论日期：** 2026-03-26（阶段 2 结束后）

### [ ] 完成 find-skills 安装
- **状态：** 需 GitHub 认证
- **优先级：** 低（有替代方案）

### [ ] 完成 Free Ride 安装
- **状态：** 需 GitHub 认证
- **优先级：** 低（需查询用途）

### [ ] 配置 Agent-Reach 剩余渠道
- **状态：** 需额外配置
- **渠道：**
  - [ ] 小红书（Docker）
  - [ ] 抖音（Python 3.10+）
  - [ ] LinkedIn（包不存在）
  - [ ] 小宇宙（Groq API Key）

---

## ✅ 已完成

### [x] 建立技能管理体系
- **完成：** 2026-03-12
- **内容：**
  - memory/skills.md（详细清单）
  - MEMORY.md（精简版）
  - AGENTS.md（安装流程规范）

### [x] 建立归档维护机制
- **完成：** 2026-03-12
- **内容：**
  - memory/archive/ 目录
  - 季度归档 cron 任务
  - MEMORY.md 精简 22%

### [x] 实施方案 A 优化（记忆去重 + 监听）
- **完成：** 2026-03-12
- **内容：**
  - memory-dedup.py（去重索引）
  - memory-watcher.py（文件监听）
  - 测试验证通过（81 个 chunk）

### [x] 配置水产市场账号
- **完成：** 2026-03-12
- **内容：**
  - CLI 安装
  - 账号注册（邀请码：SEAFOOD）
  - API Key 保存（⚠️ 不再显示）

### [x] 强化安全规范
- **完成：** 2026-03-12
- **内容：**
  - 敏感信息不显示原则
  - MEMORY.md + AGENTS.md 更新

---

## 📊 统计

- 🔴 高优先级：1 项
- 🟡 中优先级：2 项
- 🟢 低优先级：3 项
- ✅ 已完成：5 项

---

_维护规则：完成待办后移动到此文件，每月最后一天归档清理_ 🦐
