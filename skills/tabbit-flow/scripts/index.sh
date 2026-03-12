#!/bin/bash
# Tabbit 记忆索引脚本
# 功能：更新记忆索引 + 触发文件监听器

set -e

WORKSPACE="${HOME}/.openclaw/workspace-default"
MEMORY_DIR="${WORKSPACE}/memory"

# 参数处理
TARGET_FILE="$1"
INDEX_TYPE="${2:-auto}"

echo "📚 更新记忆索引..."

# 1. 运行去重索引
if [ -f "${WORKSPACE}/scripts/memory-dedup.py" ]; then
    echo "运行去重索引..."
    python3 "${WORKSPACE}/scripts/memory-dedup.py" "$MEMORY_DIR"
else
    echo "⚠️ 未找到 memory-dedup.py，跳过"
fi

# 2. 如果指定了文件，检查是否需要更新索引
if [ -n "$TARGET_FILE" ] && [ -f "$TARGET_FILE" ]; then
    echo "目标文件：$TARGET_FILE"
    
    # 根据文件类型分类
    case "$TARGET_FILE" in
        */news/*)
            echo "📰 类型：每日新闻"
            ;;
        */articles/*)
            echo "📄 类型：文章摘要"
            ;;
        */research/*)
            echo "🔍 类型：调研报告"
            ;;
        */translations/*)
            echo "🌐 类型：翻译内容"
            ;;
        *)
            echo "📁 类型：其他"
            ;;
    esac
fi

# 3. 触发文件监听器（如果运行中）
if pgrep -f "memory-watcher.py" > /dev/null; then
    echo "👀 文件监听器运行中，自动检测变更"
else
    echo "⚠️ 文件监听器未运行（可选）"
fi

echo "✅ 索引更新完成！"
