# GitHub 认证配置指南

_创建日期：2026-03-12_

---

## 🎯 为什么需要 GitHub 认证

**解决的问题：**
- 克隆私有仓库
- 绕过 ClawHub 限流
- 安装 GitHub 托管的技能
- 避免"could not read Username"错误

---

## 📋 步骤 1：生成 GitHub Token

### 1.1 访问 Token 页面

**网址：** https://github.com/settings/tokens

### 1.2 创建新 Token（经典）

1. 点击 **"Generate new token"**
2. 选择 **"Generate new token (classic)"**
3. 填写信息：
   - **Note:** `OpenClaw Skills Installation`
   - **Expiration:** `No expiration`（或选择 90 天）

### 1.3 勾选权限

**必需权限：**
- ✅ `repo`（Full control of private repositories）
- ✅ `read:org`（Read org membership）

**可选权限（如需要）：**
- ⚪ `workflow`（Update GitHub Action workflows）
- ⚪ `write:packages`（Upload packages）

### 1.4 生成并保存

1. 点击 **"Generate token"**
2. **立即复制 Token**（格式：`ghp_xxxxxxxxxxxx`）
3. **⚠️ 重要：** Token 只显示一次，关闭页面后无法再查看
4. 保存到安全地方（密码管理器或 .env 文件）

---

## 📋 步骤 2：配置 Git 凭证

### 2.1 配置凭证助手

```bash
# 使用 store 方式（保存到 ~/.git-credentials）
git config --global credential.helper store

# 或使用 cache 方式（内存缓存 15 分钟）
git config --global credential.helper 'cache --timeout=3600'
```

### 2.2 配置用户信息

```bash
git config --global user.name "sirius997"
git config --global user.email "your-email@example.com"
```

### 2.3 保存 GitHub Token

**方式 A：使用凭证存储（推荐）**

```bash
# 创建凭证文件
echo "https://sirius997:ghp_xxxxxxxxxxxx@github.com" >> ~/.git-credentials

# 设置权限（仅自己可读）
chmod 600 ~/.git-credentials
```

**方式 B：首次克隆时输入**

```bash
git clone https://github.com/openclaw/find-skills.git
# 提示输入用户名时：sirius997
# 提示输入密码时：粘贴 Token（不是 GitHub 密码）
```

---

## 📋 步骤 3：测试配置

### 3.1 测试克隆

```bash
cd ~/.openclaw/workspace/skills
git clone --depth=1 https://github.com/openclaw/find-skills.git
```

**成功输出：**
```
Cloning into 'find-skills'...
remote: Enumerating objects: 3, done.
remote: Counting objects: 100% (3/3), done.
Receiving objects: 100% (3/3), done.
```

### 3.2 验证配置

```bash
# 查看 Git 配置
git config --global --list

# 应该看到：
# user.name=sirius997
# user.email=your-email@example.com
# credential.helper=store
```

---

## 📋 步骤 4：安装技能

### 4.1 安装 find-skills

```bash
# 方式 A：使用 git clone（推荐）
cd ~/.openclaw/workspace/skills
git clone --depth=1 https://github.com/openclaw/find-skills.git

# 方式 B：使用 ClawHub（限流解除后）
clawhub install find-skills
```

### 4.2 安装 Free Ride

```bash
# 使用水产市场 CLI
export OPENCLAWMP_TOKEN=sk-229050cc19b5d740167237622236487a
openclawmp install channel/@u-c01e65f81796623e/free-ride
```

---

## 🔒 安全注意事项

### Token 安全

- ✅ 保存在 `~/.git-credentials`（权限 600）
- ✅ 或保存在 `~/.openclaw/.env`
- ❌ 不要提交到 Git
- ❌ 不要在聊天中显示
- ❌ 不要分享给他人

### 权限最小化

- ✅ 只勾选必需权限（repo + read:org）
- ❌ 不要勾选 admin 权限
- ❌ 不要勾选不必要的写权限

### 定期轮换

- 建议每 90 天更换一次 Token
- 如怀疑泄露，立即撤销并重新生成
- 撤销网址：https://github.com/settings/tokens

---

## ⚠️ 故障排查

### 问题 1：认证失败

**错误：**
```
remote: Invalid username or password.
fatal: Authentication failed
```

**解决：**
1. 检查 Token 是否正确复制（无空格）
2. 检查 Token 是否过期
3. 重新生成 Token
4. 清除旧凭证：`rm ~/.git-credentials`

### 问题 2：权限不足

**错误：**
```
remote: Repository not found.
fatal: repository not found
```

**解决：**
1. 检查 Token 是否有 `repo` 权限
2. 确认仓库是否存在
3. 确认用户名正确

### 问题 3：凭证未保存

**错误：**
```
每次克隆都要求输入密码
```

**解决：**
```bash
# 检查凭证助手配置
git config --global credential.helper

# 如果是空的，重新配置
git config --global credential.helper store
```

---

## 📝 配置记录

| 配置项 | 值 | 日期 |
|--------|-----|------|
| GitHub 用户名 | sirius997 | 2026-03-12 |
| Token 权限 | repo, read:org | 2026-03-12 |
| 凭证助手 | store | 2026-03-12 |
| Token 过期 | 无 / 90 天 | 待填写 |

---

## 🎯 完成检查清单

- [ ] 生成 GitHub Token
- [ ] 复制并保存 Token
- [ ] 配置 credential.helper
- [ ] 配置 user.name 和 user.email
- [ ] 保存 Token 到 ~/.git-credentials
- [ ] 测试克隆 find-skills
- [ ] 安装 find-skills 成功
- [ ] 安装 Free Ride 成功

---

_配置完成后，一劳永逸！_ 🦐
