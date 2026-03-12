#!/bin/bash
# Tabbit Flow 初始化脚本
# 功能：创建目录结构 + 配置 Cron + 验证环境

set -e

WORKSPACE="${HOME}/.openclaw/workspace-default"

echo "🦐 Tabbit Flow 初始化..."

# 1. 创建目录结构
echo "📁 创建目录结构..."
mkdir -p "${WORKSPACE}/drafts"
mkdir -p "${WORKSPACE}/research"
mkdir -p "${WORKSPACE}/translations"
mkdir -p "${WORKSPACE}/memory/news"
mkdir -p "${WORKSPACE}/memory/articles"

echo "✅ 目录结构已创建"

# 2. 检查 Cron 配置
echo "⏰ 检查 Cron 配置..."
CRON_EXISTS=$(openclaw cron list 2>/dev/null | grep -c "Tabbit 新闻收集提醒" || echo "0")

if [ "$CRON_EXISTS" -eq 0 ]; then
    echo "⚠️ Cron 任务未配置，需要手动添加"
    echo "   运行：openclaw skill tabbit-flow cron --enable news"
else
    echo "✅ Cron 任务已配置"
fi

# 3. 验证钉钉连接器
echo "📱 检查钉钉连接器..."
if openclaw plugins list 2>/dev/null | grep -q "dingtalk-connector"; then
    echo "✅ 钉钉连接器已加载"
else
    echo "⚠️ 钉钉连接器未加载"
fi

# 4. 输出使用说明
echo ""
echo "✅ 初始化完成！"
echo ""
echo "📋 下一步："
echo "1. 打开 Tabbit 浏览器扩展"
echo "2. 选择 Gemini-Pro 模型"
echo "3. 打开 3-5 个新闻网站"
echo "4. 输入：@所有标签页 总结今日 AI 新闻"
echo "5. 保存到：${WORKSPACE}/memory/news/$(date +%Y-%m-%d).md"
echo "6. 告诉小虾米：'新闻已保存'"
echo ""
echo "📚 可用命令："
echo "   openclaw skill tabbit-flow news     — 处理新闻"
echo "   openclaw skill tabbit-flow code     — 处理代码"
echo "   openclaw skill tabbit-flow cron     — 管理 Cron"
echo "   openclaw skill tabbit-flow status   — 查看状态"
echo ""
