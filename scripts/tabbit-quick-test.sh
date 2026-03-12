#!/bin/bash
# Tabbit 快速测试脚本
# 使用 AppleScript 直接控制

echo "=========================================="
echo "Tabbit 测试脚本"
echo "=========================================="

# 1. 激活 Tabbit
echo "1️⃣  激活 Tabbit..."
osascript -e 'tell application "Tabbit" to activate'
sleep 2

# 2. 模拟打开新标签页
echo "2️⃣  打开新标签页..."
osascript -e 'tell application "System Events" to tell process "Tabbit"' \
  -e 'keystroke "t" using command down' \
  -e 'end tell'
sleep 2

# 3. 打开 Tabbit 官网
echo "3️⃣  打开官网..."
osascript -e 'tell application "System Events" to tell process "Tabbit"' \
  -e 'keystroke "l" using command down' \
  -e 'keystroke "https://www.tabbitbrowser.com"' \
  -e 'keystroke return' \
  -e 'end tell'
sleep 3

# 4. 提示用户操作
echo ""
echo "=========================================="
echo "4️⃣  手动测试环节"
echo "=========================================="
echo ""
echo "请按以下步骤操作："
echo ""
echo "步骤 1: 点击右上角 Chat 图标（或按 Cmd+Shift+A）"
echo "步骤 2: 点击模型下拉菜单"
echo "步骤 3: 截图模型列表（Cmd+Shift+4）"
echo "步骤 4: 按回车继续..."
read

echo ""
echo "步骤 5: 选择 GPT-5.2-Chat 模型"
echo "步骤 6: 输入问题：1+1=?"
echo "步骤 7: 记录响应时间：___秒"
echo "步骤 8: 记录响应质量 (1-5): ___"
echo "按回车继续..."
read

echo ""
echo "步骤 9: 切换 Claude-Sonnet-4.6"
echo "步骤 10: 输入同样的问题"
echo "步骤 11: 记录响应时间：___秒"
echo "步骤 12: 记录响应质量 (1-5): ___"
echo "按回车继续..."
read

echo ""
echo "步骤 13: 切换 Gemini-3.1-Pro"
echo "步骤 14: 输入同样的问题"
echo "步骤 15: 记录响应时间：___秒"
echo "步骤 16: 记录响应质量 (1-5): ___"
echo "按回车继续..."
read

# 5. 测试@引用功能
echo ""
echo "=========================================="
echo "5️⃣  @引用功能测试"
echo "=========================================="
echo ""
echo "步骤 1: 打开 3 个不同的网页（建议：36 氪、机器之心、量子位）"
echo "步骤 2: 在 Chat 输入框输入 @"
echo "步骤 3: 看是否弹出标签页列表"
echo "步骤 4: 能否多选多个标签页？"
echo ""
echo "结果：@功能可用吗？(y/n)"
read at_result

# 6. 测试妙招功能
echo ""
echo "=========================================="
echo "6️⃣  妙招功能测试"
echo "=========================================="
echo ""
echo "步骤 1: 在 Chat 输入框输入 /"
echo "步骤 2: 看是否弹出妙招列表"
echo "步骤 3: 点击'创建妙招'"
echo "步骤 4: 创建一个测试妙招（名称：测试，内容：总结这篇文章）"
echo "步骤 5: 输入 / 看能否看到刚才创建的妙招"
echo ""
echo "结果：妙招功能可用吗？(y/n)"
read skill_result

# 7. 生成报告
echo ""
echo "=========================================="
echo "📊 测试报告"
echo "=========================================="
echo ""
echo "测试时间：$(date '+%Y-%m-%d %H:%M:%S')"
echo ""
echo "模型测试结果:"
echo "  GPT-5.2-Chat:     响应时间=___s, 质量=___/5"
echo "  Claude-Sonnet:    响应时间=___s, 质量=___/5"
echo "  Gemini-Pro:       响应时间=___s, 质量=___/5"
echo ""
echo "功能测试:"
echo "  @引用功能：$at_result"
echo "  妙招功能：$skill_result"
echo ""
echo "=========================================="
echo "✅ 测试完成！"
echo "=========================================="

# 8. 保存结果
cat > ~/.openclaw/workspace-default/memory/tabbit-quick-test-result.md << EOF
# Tabbit 快速测试结果

**测试时间：** $(date '+%Y-%m-%d %H:%M:%S')

## 模型测试

| 模型 | 响应时间 | 质量 (1-5) | 备注 |
|------|---------|-----------|------|
| GPT-5.2-Chat | ___s | ___ | |
| Claude-Sonnet-4.6 | ___s | ___ | |
| Gemini-3.1-Pro | ___s | ___ | |

## 功能测试

| 功能 | 状态 | 备注 |
|------|------|------|
| @引用功能 | $at_result | |
| 妙招功能 | $skill_result | |

## 结论

- [ ] 值得作为主力工具
- [ ] 仅作为辅助工具
- [ ] 不推荐

## 备注

(在此填写额外观察)
EOF

echo ""
echo "📄 结果已保存到：memory/tabbit-quick-test-result.md"
echo ""
