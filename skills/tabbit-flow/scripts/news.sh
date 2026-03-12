#!/bin/bash
# Tabbit 新闻处理脚本
# 功能：格式化新闻内容 + 推送钉钉 + 索引记忆

set -e

WORKSPACE="${HOME}/.openclaw/workspace-default"
NEWS_DIR="${WORKSPACE}/memory/news"
TODAY=$(date +%Y-%m-%d)

# 参数处理
NEWS_FILE="${1:-${NEWS_DIR}/${TODAY}.md}"

if [ ! -f "$NEWS_FILE" ]; then
    echo "❌ 新闻文件不存在：$NEWS_FILE"
    exit 1
fi

echo "📰 处理新闻文件：$NEWS_FILE"

# 1. 读取新闻内容
NEWS_CONTENT=$(cat "$NEWS_FILE")

# 2. 格式化钉钉消息
FORMATTED=$(cat <<EOF
📰 **AI 新闻日报** — ${TODAY}

${NEWS_CONTENT}

---
_来源：Tabbit + 小虾米自动化_ 🦐
EOF
)

# 3. 调用 OpenClaw message 工具发送钉钉
# 注意：实际执行需要通过 OpenClaw 工具调用
echo "✅ 新闻已格式化，准备推送钉钉..."
echo "文件：$NEWS_FILE"
echo "内容行数：$(wc -l < "$NEWS_FILE")"

# 4. 触发记忆索引
if [ -f "${WORKSPACE}/scripts/memory-dedup.py" ]; then
    echo "📚 更新记忆索引..."
    python3 "${WORKSPACE}/scripts/memory-dedup.py" "${WORKSPACE}/memory/"
fi

echo "✅ 新闻处理完成！"
