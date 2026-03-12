# 记忆优化工具使用说明

_创建日期：2026-03-12_

---

## 🛠️ 工具列表

### 1. memory-dedup.py — 去重索引工具

**功能：**
- 扫描记忆目录，找出新增/修改的文件
- 使用 SHA-256 哈希去重（内容不变 = 永不重新索引）
- 自动清理已删除文件的索引
- 按段落分块（最大 500 字符/chunk）

**使用：**
```bash
# 手动索引
cd ~/.openclaw/workspace
python3 scripts/memory-dedup.py ./memory/

# 输出示例：
# 🆕 新文件：memory/2026-03-12.md
# 🔄 已修改：memory/skills.md
# ✅ 无变化：memory/2026-03-10.md
# 📊 统计：2 个文件需要索引，0 个文件已删除
```

**索引文件：** `memory/.index.json`
- 自动创建，无需手动编辑
- 包含 chunk 哈希、来源、时间戳

---

### 2. memory-watcher.py — 文件监听器

**功能：**
- 实时监听记忆目录的文件变化
- 文件修改/创建 → 1.5 秒后自动索引（防抖）
- 文件删除 → 自动清理对应 chunk
- 后台运行，无需手动触发

**使用：**
```bash
# 启动监听器（前台）
python3 scripts/memory-watcher.py ./memory/

# 启动监听器（后台）
python3 scripts/memory-watcher.py ./memory/ &

# 停止监听器
# Ctrl+C（前台）或 kill <pid>（后台）
```

**输出示例：**
```
👁️  开始监听：./memory/
⏱️  防抖时间：1500ms
📋 初始化索引现有文件...
   ✓ 2026-03-12.md (5 chunks)
   ✓ skills.md (9 chunks)
✅ 初始索引完成，共 81 个 chunk

📝 检测到修改：memory/2026-03-12.md
   + 新增 2 个 chunk
   💾 索引已保存
```

---

## 🔧 依赖安装

```bash
# memory-dedup.py — 无需额外依赖（Python 3 内置）
# memory-watcher.py — 需要 watchdog

pip3 install watchdog
```

---

## 📋 最佳实践

### 日常使用

**方案 1：手动索引（推荐）**
```bash
# 每天工作结束时运行一次
python3 scripts/memory-dedup.py ./memory/
```

**方案 2：后台监听（自动化）**
```bash
# 开机自启动（添加到 ~/.zshrc 或启动脚本）
python3 ~/.openclaw/workspace/scripts/memory-watcher.py ~/.openclaw/workspace/memory/ &
```

### 与 Heartbeat 集成

**在 HEARTBEAT.md 中添加：**
```markdown
### 🔍 记忆索引检查

- 执行：`python3 scripts/memory-dedup.py ./memory/`
- 如果有新增/修改 → 自动索引
- 如果无变化 → 跳过（去重机制）
```

### 季度维护

**与归档流程一起执行：**
1. 运行记忆归档 cron 任务
2. 归档旧记忆文件到 `memory/archive/`
3. 运行 `memory-dedup.py` 更新索引
4. 索引会自动清理已归档文件的 chunk

---

## 📊 性能指标

**测试数据（2026-03-12）：**
- 记忆文件：12 个 .md 文件
- 总 chunk 数：81 个
- 索引文件大小：~50KB
- 首次索引时间：~2 秒
- 增量索引时间：<0.5 秒（无变化时）

**优化效果：**
- ✅ 避免重复索引（SHA-256 去重）
- ✅ 自动更新（文件监听）
- ✅ 减少手动操作（自动化）

---

## ⚠️ 注意事项

1. **索引文件不要手动编辑**
   - `memory/.index.json` 是自动生成的
   - 手动修改可能导致不一致

2. **监听器不要重复启动**
   - 多个监听器会导致重复索引
   - 检查是否已在运行：`ps aux | grep memory-watcher`

3. **归档后记得更新索引**
   - 归档旧文件后，运行一次 `memory-dedup.py`
   - 会自动清理已归档文件的 chunk

4. **备份索引文件（可选）**
   - 索引可以重建（从 markdown 文件）
   - 但备份可以加快恢复速度

---

## 🚀 未来优化方向

**短期：**
- [ ] 添加搜索功能（基于索引的关键词搜索）
- [ ] 添加统计命令（`python3 scripts/memory-dedup.py --stats`）
- [ ] 添加清理命令（`python3 scripts/memory-dedup.py --clean`）

**中期：**
- [ ] 集成语义搜索（如果引入向量数据库）
- [ ] 添加记忆压缩功能（LLM 自动摘要）
- [ ] 添加记忆导出功能（按主题/时间导出）

**长期：**
- [ ] 参考 MemSearch 实现混合搜索（语义 + 关键词）
- [ ] 实现记忆关联图谱（自动发现相关记忆）
- [ ] 添加记忆质量评分（识别重要/过时记忆）

---

_维护：小虾米 | 最后更新：2026-03-12_ 🦐
