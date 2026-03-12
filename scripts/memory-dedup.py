#!/usr/bin/env python3
"""
记忆去重工具 - 基于 SHA-256 内容哈希

功能：
1. 计算记忆内容的哈希值
2. 检查是否已索引（避免重复）
3. 只索引新增/修改的内容

使用：
python3 memory-dedup.py ./memory/
"""

import hashlib
import json
import os
import sys
from pathlib import Path
from datetime import datetime

INDEX_FILE = Path.home() / ".openclaw" / "workspace" / "memory" / ".index.json"

def compute_hash(content: str) -> str:
    """计算内容的 SHA-256 哈希"""
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

def load_index() -> dict:
    """加载索引文件"""
    if INDEX_FILE.exists():
        with open(INDEX_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"chunks": {}, "files": {}, "last_updated": None}

def save_index(index: dict):
    """保存索引文件"""
    INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

def chunk_memory(content: str, max_chunk_size: int = 500) -> list:
    """
    将记忆内容分块（按段落）
    
    规则：
    - 按空行分割段落
    - 每个 chunk 不超过 max_chunk_size 字符
    - 保留标题层级
    """
    chunks = []
    paragraphs = content.split('\n\n')
    
    current_chunk = []
    current_size = 0
    
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        
        para_size = len(para)
        
        # 如果单个段落就超过限制，强制分割
        if para_size > max_chunk_size:
            # 先保存当前 chunk
            if current_chunk:
                chunks.append('\n\n'.join(current_chunk))
                current_chunk = []
                current_size = 0
            
            # 按行分割长段落
            lines = para.split('\n')
            temp_chunk = []
            temp_size = 0
            
            for line in lines:
                line_size = len(line)
                if temp_size + line_size > max_chunk_size:
                    if temp_chunk:
                        chunks.append('\n'.join(temp_chunk))
                        temp_chunk = []
                        temp_size = 0
                    temp_chunk.append(line)
                    temp_size = line_size
                else:
                    temp_chunk.append(line)
                    temp_size += line_size
            
            if temp_chunk:
                chunks.append('\n'.join(temp_chunk))
        
        # 如果加上这个段落会超限，先保存当前 chunk
        elif current_size + para_size > max_chunk_size:
            chunks.append('\n\n'.join(current_chunk))
            current_chunk = [para]
            current_size = para_size
        else:
            current_chunk.append(para)
            current_size += para_size
    
    # 保存最后一个 chunk
    if current_chunk:
        chunks.append('\n\n'.join(current_chunk))
    
    return chunks

def scan_memory_dir(memory_dir: Path) -> dict:
    """扫描记忆目录，返回文件列表和哈希"""
    files = {}
    
    for md_file in memory_dir.glob("*.md"):
        # 跳过索引文件
        if md_file.name.startswith('.'):
            continue
        
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        files[str(md_file)] = {
            "path": str(md_file),
            "hash": compute_hash(content),
            "size": len(content),
            "modified": datetime.fromtimestamp(md_file.stat().st_mtime).isoformat()
        }
    
    return files

def find_new_or_changed(memory_dir: str) -> list:
    """
    找出新增或修改的文件
    
    返回：需要重新索引的文件列表
    """
    memory_path = Path(memory_dir)
    index = load_index()
    current_files = scan_memory_dir(memory_path)
    
    files_to_index = []
    
    for file_path, file_info in current_files.items():
        # 新文件
        if file_path not in index["files"]:
            files_to_index.append(file_path)
            print(f"🆕 新文件：{file_path}")
        # 文件有变化
        elif index["files"][file_path]["hash"] != file_info["hash"]:
            files_to_index.append(file_path)
            print(f"🔄 已修改：{file_path}")
        else:
            print(f"✅ 无变化：{file_path}")
    
    # 检查已删除的文件
    deleted_files = []
    for file_path in index["files"]:
        if file_path not in current_files:
            deleted_files.append(file_path)
            print(f"❌ 已删除：{file_path}")
    
    return files_to_index, deleted_files

def index_file(file_path: str, index: dict) -> dict:
    """索引单个文件，返回更新后的索引"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    file_hash = compute_hash(content)
    chunks = chunk_memory(content)
    
    new_chunks = 0
    for i, chunk in enumerate(chunks):
        chunk_hash = compute_hash(chunk)
        
        # 如果 chunk 已存在，跳过
        if chunk_hash in index["chunks"]:
            continue
        
        # 新增 chunk
        index["chunks"][chunk_hash] = {
            "content": chunk,
            "source": file_path,
            "chunk_index": i,
            "total_chunks": len(chunks),
            "indexed_at": datetime.now().isoformat()
        }
        new_chunks += 1
    
    # 更新文件记录
    index["files"][file_path] = {
        "hash": file_hash,
        "chunks": len(chunks),
        "indexed_at": datetime.now().isoformat()
    }
    
    index["last_updated"] = datetime.now().isoformat()
    
    return index, new_chunks

def remove_deleted_files(deleted_files: list, index: dict) -> dict:
    """从索引中移除已删除文件的 chunk"""
    removed_chunks = 0
    
    for file_path in deleted_files:
        # 找到这个文件的所有 chunk
        chunks_to_remove = []
        for chunk_hash, chunk_info in index["chunks"].items():
            if chunk_info["source"] == file_path:
                chunks_to_remove.append(chunk_hash)
        
        # 删除 chunk
        for chunk_hash in chunks_to_remove:
            del index["chunks"][chunk_hash]
            removed_chunks += 1
        
        # 删除文件记录
        if file_path in index["files"]:
            del index["files"][file_path]
    
    index["last_updated"] = datetime.now().isoformat()
    
    return index, removed_chunks

def main():
    if len(sys.argv) < 2:
        print("用法：python3 memory-dedup.py <memory_dir>")
        print("示例：python3 memory-dedup.py ./memory/")
        sys.exit(1)
    
    memory_dir = sys.argv[1]
    
    if not Path(memory_dir).exists():
        print(f"错误：目录不存在 {memory_dir}")
        sys.exit(1)
    
    print(f"🔍 扫描记忆目录：{memory_dir}")
    print("-" * 50)
    
    # 找出新增或修改的文件
    files_to_index, deleted_files = find_new_or_changed(memory_dir)
    
    if not files_to_index and not deleted_files:
        print("\n✅ 所有文件都是最新的，无需索引")
        return
    
    print("\n" + "=" * 50)
    print(f"📊 统计：{len(files_to_index)} 个文件需要索引，{len(deleted_files)} 个文件已删除")
    print("=" * 50)
    
    # 加载索引
    index = load_index()
    
    # 索引新文件
    total_new_chunks = 0
    for file_path in files_to_index:
        print(f"\n📝 索引：{file_path}")
        index, new_chunks = index_file(file_path, index)
        total_new_chunks += new_chunks
        print(f"   + 新增 {new_chunks} 个 chunk")
    
    # 移除已删除文件的 chunk
    if deleted_files:
        print(f"\n🗑️  清理已删除文件...")
        index, removed_chunks = remove_deleted_files(deleted_files, index)
        print(f"   - 移除 {removed_chunks} 个 chunk")
    
    # 保存索引
    save_index(index)
    
    print("\n" + "=" * 50)
    print(f"✅ 索引完成！")
    print(f"   - 新增 chunk: {total_new_chunks}")
    print(f"   - 总 chunk 数：{len(index['chunks'])}")
    print(f"   - 索引文件：{INDEX_FILE}")
    print("=" * 50)

if __name__ == "__main__":
    main()
