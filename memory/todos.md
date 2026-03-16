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

## ✅ 已完成（2026-03-17）

### [x] Agent 自主进化方案（阶段 1）
- **完成：** 2026-03-17
- **内容：**
  - [x] 创建 `memory/skill-gaps.md`（能力缺口记录）
  - [x] 更新 HEARTBEAT.md 添加信号采集规则
  - [x] 配置自动化 cron（待添加）
- **观察期：** 2026-03-12 ~ 2026-03-19（1 周）

### [x] 完善记忆优化工具
- **完成：** 2026-03-17
- **内容：**
  - [x] 添加 `--stats` 参数（显示索引统计）
  - [x] 添加 `--search` 参数（关键词搜索）
  - [x] 添加 `--clean` 参数（清理过期 chunk）
- **测试：** 全部通过 ✅

### [x] 配置 Brave API Key（已移除）
- **决策：** 2026-03-17
- **原因：** 无 API Key，且 Tavily/Exa 已足够
- **替代方案：**
  - 日常搜索：smart-search（Tavily）
  - AI 搜索：exa-search（Exa）
  - 深度研究：deep-research（Tavily + Exa）

### [x] 推送 Session List PR（已删除）
- **决策：** 2026-03-17
- **原因：** 已采用直接提交代码方式同步
- **状态：** 本地 commit 完成，等待 git push 凭证配置

### [x] 配置 git 远程仓库
- **完成：** 2026-03-17
- **远程：** origin = https://github.com/SiriuSM00N/openclaw.git
- **状态：** ✅ 已配置，待推送（需 git 凭证）

---

## 🟡 中优先级（本月）

### [ ] 配置 git push 凭证
- **截止：** 2026-03-18
- **原因：** 本地 commit 已就绪，需推送到 GitHub
- **步骤：**
  - [ ] 运行 `git push origin main`
  - [ ] 输入 GitHub 用户名和密码（Personal Access Token）
  - [ ] 验证推送成功

### [ ] 添加能力缺口采集 cron
- **截止：** 2026-03-19
- **前提：** Agent 自主进化方案 阶段 1 完成 ✅
- **任务：**
  - [ ] 创建 cron 任务（每天 18:00）
  - [ ] 扫描会话历史
  - [ ] 自动记录到 skill-gaps.md

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

## 📊 统计（2026-03-17 更新）

- 🔴 高优先级：1 项
- 🟡 中优先级：2 项
- 🟢 低优先级：5 项
- ✅ 已完成：8 项（今日完成 5 项）

---

_维护规则：完成待办后移动到此文件，每月最后一天归档清理_ 🦐
