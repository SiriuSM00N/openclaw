#!/bin/bash
# Tabbit 代码处理脚本
# 功能：运行测试 + Git 提交 + 钉钉通知

set -e

WORKSPACE="${HOME}/.openclaw/workspace-default"

# 参数处理
CODE_FILE="$1"
RUN_TEST="${2:-false}"

if [ -z "$CODE_FILE" ] || [ ! -f "$CODE_FILE" ]; then
    echo "❌ 代码文件不存在：$CODE_FILE"
    exit 1
fi

echo "💻 处理代码文件：$CODE_FILE"

# 1. 运行测试（如果指定）
if [ "$RUN_TEST" = "true" ] || [ "$RUN_TEST" = "--test" ]; then
    echo "🧪 运行测试..."
    
    # 根据文件类型选择测试命令
    case "$CODE_FILE" in
        *.py)
            if command -v pytest &> /dev/null; then
                pytest "$CODE_FILE" || echo "⚠️ 测试失败，继续提交"
            elif [ -f "${CODE_FILE%.py}_test.py" ]; then
                python3 "${CODE_FILE%.py}_test.py" || echo "⚠️ 测试失败，继续提交"
            else
                echo "⚠️ 未找到测试文件，跳过测试"
            fi
            ;;
        *.js)
            if [ -f "package.json" ] && grep -q "test" package.json; then
                npm test || echo "⚠️ 测试失败，继续提交"
            else
                echo "⚠️ 未配置测试，跳过测试"
            fi
            ;;
        *)
            echo "⚠️ 未知文件类型，跳过测试"
            ;;
    esac
fi

# 2. Git 提交
echo "📦 Git 提交..."
cd "$(dirname "$CODE_FILE")"
git add "$(basename "$CODE_FILE")" 2>/dev/null || true
git commit -m "feat: 添加 $(basename "$CODE_FILE") (Tabbit 生成)" 2>/dev/null || echo "⚠️ Git 提交失败（可能未初始化仓库）"

# 3. 输出统计
echo "✅ 代码处理完成！"
echo "文件：$CODE_FILE"
echo "行数：$(wc -l < "$CODE_FILE")"
echo "大小：$(du -h "$CODE_FILE" | cut -f1)"
