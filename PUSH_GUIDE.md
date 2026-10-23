# 🚀 双仓库同步推送指南

本项目同时维护两个远端，**每次发布必须两个都更新**：

| remote | 地址 | 用途 |
|---|---|---|
| `origin` | https://github.com/Hongqiong12/ai-security-daily | 公网主站（GitHub） |
| `gongfeng` | https://git.woa.com/aegisliu/ai-security-daily | 内网镜像（腾讯工蜂） |

> ⚠️ 历史坑：README 曾指向 `github.com/ageisliu/ai-security-daily`，该仓库 **404 不存在**，导致"看起来一直没更新"。
> 已于 2026-10-23 统一改为 `Hongqiong12`。**不要再写回 `ageisliu` 的 GitHub 地址。**

---

## 日常同步（已自动化）

每日调研任务结束后会自动执行：

```bash
cd /Users/ageisliu/WorkBuddy/Claw/ai-security-daily
bash scripts/sync_remotes.sh main
```

脚本会依次 push `origin` 和 `gongfeng`，**任一失败不阻断另一个**。

手动补推（例如工蜂凭据失效后恢复）：

```bash
git push gongfeng main
```

---

## 凭据配置

### GitHub (origin)

推荐用 GitHub CLI 走 keychain，避免明文 token：

```bash
brew install gh
gh auth login
```

或确认 credential helper 已启用：

```bash
git config --global credential.helper osxkeychain
```

### 工蜂 (gongfeng)

工蜂 HTTPS 推送需要 **Personal Access Token**：

1. 打开 https://git.woa.com/-/profile/personal_access_tokens
2. 新建令牌，勾选 `api` / `read_repository` / `write_repository`
3. 推送时用令牌作为密码：

```bash
git push gongfeng main
# Username: aegisliu
# Password: <粘贴 Personal Access Token>
```

配合 macOS keychain 缓存后，后续无需重复输入：

```bash
git config --global credential.helper osxkeychain
```

**SSH 备选**（当前机器 `~/.ssh` 无可用公钥，需先生成）：

```bash
ssh-keygen -t ed25519 -C "aegisliu@git.woa.com"
cat ~/.ssh/id_ed25519.pub   # 粘贴到工蜂 SSH Keys
git remote set-url gongfeng git@git.woa.com:aegisliu/ai-security-daily.git
```

---

## 首次建仓（历史记录，已完成，无需再执行）

```bash
git remote add origin    https://github.com/Hongqiong12/ai-security-daily.git
git remote add gongfeng  https://git.woa.com/aegisliu/ai-security-daily.git
git branch -M main
git push -u origin main
git push -u gongfeng main
```

---

## 项目链接

- **GitHub（公网）**: https://github.com/Hongqiong12/ai-security-daily
- **工蜂（内网）**: https://git.woa.com/aegisliu/ai-security-daily

---

*最后更新: 2026-10-23*
