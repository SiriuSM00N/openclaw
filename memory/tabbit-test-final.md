# Tabbit 测试方案（最终版）

**日期：** 2026-03-12  
**状态：** ⚠️ GUI 自动化受限，采用半自动测试

---

## 🔍 技术限制分析

### 为什么不能全自动测试？

**Tabbit 是 Electron 应用**（基于 Chromium），存在以下限制：

| 方法 | 可行性 | 原因 |
|------|--------|------|
| AppleScript 直接控制 | ❌ 不可行 | Electron 不暴露标准 UI 元素 |
| pyautogui 图像识别 | ⚠️ 部分可行 | 需要安装依赖，且坐标不稳定 |
| CDP 协议控制 | ⚠️ 待验证 | Electron 可能禁用远程调试 |
| 辅助功能 API | ⚠️ 需要权限 | macOS 需要用户授权 |

### 已尝试的方法

```bash
# 1. AppleScript 获取窗口
osascript -e 'tell application "System Events" to tell process "Tabbit" to get name of every window'
# 结果：返回空（无标准窗口）

# 2. 检测 CDP 端口
lsof -i -n | grep tabbit
# 结果：command not found（需要安装）

# 3. 模拟按键
osascript -e 'tell application "System Events" to keystroke "t" using command down'
# 结果：可行（但无法确认 Tabbit 是否响应）
```

---

## ✅ 可行的测试方案

### 方案 A：半自动测试脚本（推荐）

**脚本：** `scripts/tabbit-quick-test.sh`

**流程：**
```
1. 脚本自动激活 Tabbit
2. 脚本打开官网
3. 脚本提示用户操作步骤
4. 用户按提示操作（点击/截图/输入）
5. 脚本记录结果
6. 自动生成测试报告
```

**运行方式：**
```bash
cd ~/.openclaw/workspace-default
./scripts/tabbit-quick-test.sh
```

**预计时间：** 10 分钟  
**用户操作：** 点击模型下拉菜单、截图、输入测试问题

---

### 方案 B：纯手动测试清单

**如果脚本运行有问题，直接按清单测试：**

#### Phase 1：模型可用性（5 分钟）

```
□ 1. 打开 Tabbit
□ 2. 点击右上角 Chat 图标（或按 Cmd+Shift+A）
□ 3. 点击模型下拉菜单
□ 4. 截图整个模型列表
□ 5. 对照以下清单，勾选存在的模型：

[ ] GPT-5.2-Chat
[ ] GPT-5.1-Chat
[ ] Claude-Sonnet-4.6
[ ] Claude-Haiku-4.5
[ ] Gemini-3.1-Pro
[ ] Gemini-3.1-Flash
[ ] Gemini-2.5-Flash
[ ] GLM-5
[ ] DeepSeek-V3.2
[ ] Doubao-Seed-1.8
[ ] Kimi-K2.5
[ ] Qwen3.5-Plus
[ ] MiniMax-M2.5
[ ] LongCat

□ 6. 每个模型问"1+1=?"，记录是否响应
```

#### Phase 2：调用限制（5 分钟）

```
□ 1. 选 GPT-5.2-Chat
□ 2. 连续问 10 次不同问题
□ 3. 记录第几次出现限制提示（如果有）
□ 4. 换 Claude-Sonnet 重复
□ 5. 换 Gemini-Pro 重复
```

#### Phase 3：功能测试（10 分钟）

```
@引用功能：
□ 1. 打开 3 个网页
□ 2. Chat 输入框输入 @
□ 3. 看是否弹出标签页列表
□ 4. 能否多选？

妙招功能：
□ 1. 输入 /
□ 2. 看是否弹出菜单
□ 3. 创建测试妙招
□ 4. 再次输入 / 看能否调用

收藏功能：
□ 1. 收藏当前网页
□ 2. 看是否生成 AI 摘要

导出功能：
□ 1. 找导出按钮
□ 2. 支持哪些格式？
```

---

### 方案 C：我负责的部分（可立即执行）

**不需要 Tabbit 界面操作，我现在就能做：**

#### 1. 网络信息收集

```bash
# 搜索更多实测报告
curl -s "https://api.exa.ai/search" \
  -H "Authorization: Bearer 1059e9e9-ec4f-4aa5-981b-c42e11ed1f7f" \
  -H "Content-Type: application/json" \
  -d '{"query":"Tabbit browser user review limitation 2026","numResults":10}'
```

#### 2. 替补方案验证

```bash
# 测试 OpenClaw + Tavily 的资讯总结
# 测试 OpenClaw + Exa 的竞品调研
# 测试 qwen3-coder-plus 的代码生成
# 测试 kimi-k2.5 的长文本处理
```

#### 3. 数据分析 + 报告生成

- 整理用户提供的测试结果
- 对比各模型能力
- 更新替补方案
- 生成最终决策建议

---

## 📋 推荐流程

### 最快路径（15 分钟）

```
1. 咔啦米运行 ./scripts/tabbit-quick-test.sh（10 分钟）
   - 按提示操作即可
   - 脚本自动记录结果

2. 我分析测试结果（5 分钟）
   - 更新能力评分表
   - 验证替补方案

3. 生成最终报告（自动）
   - memory/tabbit-final-report.md
```

### 备选路径（30 分钟）

```
1. 咔啦米手动测试清单（15 分钟）
   - 截图模型列表
   - 填写测试表格

2. 我同时验证替补方案（15 分钟）
   - 测试 OpenClaw 各模型
   - 对比 Tabbit vs OpenClaw

3. 合并结果生成报告
```

---

## 🎯 关键问题（必须确认）

**只需要确认这 5 个，就能决定整体方案：**

```
1. 14 个模型是否都在列表中？（截图）
2. GPT-5.2/Claude/Gemini 能否正常响应？
3. 连续调用 10 次有没有限制提示？
4. @引用功能是否可用？
5. 能否导出对话/收藏？
```

**如果以上都是✅，则 Tabbit 值得作为主力工具。**

**如果有任何❌，则启用替补方案。**

---

## 🔄 替补方案状态

**已就绪（可随时切换）：**

| 场景 | Tabbit | OpenClaw 替补 | 状态 |
|------|--------|------------|------|
| 资讯速读 | Gemini-Pro | Tavily+qwen3.5-plus | ✅ 可用 |
| 竞品调研 | Claude-Sonnet | Exa+glm-5 | ✅ 可用 |
| 代码生成 | GPT-5.2 | qwen3-coder-plus | ✅ 可用 |
| 代码审查 | Claude-Sonnet | qwen3-coder-plus | ✅ 可用 |
| 长文档 | Gemini-Pro(1M) | kimi-k2.5 | ✅ 可用 |
| 翻译 | DeepSeek-V3.2 | qwen3.5-plus | ✅ 可用 |
| 创意写作 | MiniMax-M2.5 | qwen3.5-plus | ⚠️ 略弱 |
| 逻辑推理 | Gemini-Pro | glm-5 | ✅ 可用 |

---

## 📝 下一步

**选项 A（推荐）：** 
```
现在运行 ./scripts/tabbit-quick-test.sh
10 分钟完成测试
我立即分析结果
```

**选项 B：**
```
你先忙别的
我验证 OpenClaw 替补方案
你抽空再测 Tabbit
```

**选项 C：**
```
你手动测试 5 个关键问题（见上方）
告诉我结果
我生成完整报告
```

选哪个？🦐
