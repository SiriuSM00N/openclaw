#!/bin/bash
# Tabbit Flow 全自动新闻收集脚本
# 功能：Exa 搜索 + 自动摘要 + 保存 + 钉钉推送 + 索引

set -e

WORKSPACE="${HOME}/.openclaw/workspace-default"
NEWS_DIR="${WORKSPACE}/memory/news"
TODAY=$(date +%Y-%m-%d)
NEWS_FILE="${NEWS_DIR}/${TODAY}.md"

echo "🦐 Tabbit Flow 全自动新闻收集中..."

# 1. 确保目录存在
mkdir -p "$NEWS_DIR"

# 2. 用 Exa 搜索 AI+ 游戏新闻
echo "🔍 搜索 AI+ 游戏新闻..."
SEARCH_RESULTS=$(curl -s -X POST https://api.exa.ai/search \
  -H "Authorization: Bearer $EXA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "AI gaming news GDC 2026 game development",
    "numResults": 10,
    "type": "neural",
    "useAutoprompt": true
  }')

# 3. 提取结果（用 Python 解析 JSON）
PARSED=$(echo "$SEARCH_RESULTS" | python3 -c "
import sys, json
data = json.load(sys.stdin)
results = data.get('results', [])
for i, r in enumerate(results[:10], 1):
    title = r.get('title', '无标题')
    url = r.get('url', '')
    snippet = r.get('text', r.get('snippet', '无摘要'))[:200]
    print(f'{i}. **{title}**')
    print(f'   {snippet}...')
    print(f'   🔗 {url}')
    print()
")

# 4. 生成新闻文件
cat > "$NEWS_FILE" << EOF
# ${TODAY} AI 游戏新闻日报

_来源：Exa AI Search + 小虾米自动化_

---

## 📰 今日要闻

${PARSED}

---

## 📊 统计

- **搜索时间：** $(date +%H:%M)
- **新闻条数：** 10 条
- **来源：** Exa AI Search

---

_标签：#AI #游戏 #新闻 #GDC_
EOF

echo "✅ 新闻文件已保存：$NEWS_FILE"

# 5. 生成钉钉推送消息
DINGTALK_MSG=$(cat << EOF
📰 **AI 游戏新闻日报** — ${TODAY}

今日 10 条 AI+ 游戏热点：

${PARSED}

---
_来源：Exa + 小虾米自动化_ 🦐
EOF
)

echo "📱 准备推送钉钉..."

# 6. 调用 OpenClaw message 工具发送钉钉
# 注意：这里需要通过 OpenClaw 工具调用，不是直接 curl
# 创建一个临时文件供 OpenClaw 读取
echo "$DINGTALK_MSG" > /tmp/tabbit-dingtalk-msg.txt

echo "✅ 新闻处理完成！"
echo "文件：$NEWS_FILE"
echo "钉钉消息：/tmp/tabbit-dingtalk-msg.txt"

# 7. 触发记忆索引
if [ -f "${WORKSPACE}/scripts/memory-dedup.py" ]; then
    echo "📚 更新记忆索引..."
    python3 "${WORKSPACE}/scripts/memory-dedup.py" "${WORKSPACE}/memory/"
fi

echo ""
echo "🎉 完成！下一步："
echo "openclaw message send --target user:sirius997 --message \"\$(cat /tmp/tabbit-dingtalk-msg.txt)\""
