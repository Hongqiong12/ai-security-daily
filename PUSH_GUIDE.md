# 🚀 GitHub 推送指南

## 首次推送（需要手动执行一次）

### 方法 1: 使用 GitHub CLI（推荐）

```bash
# 安装 gh (如果未安装)
brew install gh

# 登录 GitHub
gh auth login

# 推送代码
cd ai-security-daily
gh repo create ai-security-daily --public --push
```

### 方法 2: 使用 GitHub 网页

1. 打开 https://github.com/new
2. Repository name: `ai-security-daily`
3. 选择 Public
4. 不要勾选 "Initialize this repository with a README"
5. 点击 "Create repository"
6. 在终端执行：
```bash
cd ai-security-daily
git remote add origin https://github.com/Hongqiong12/ai-security-daily.git
git branch -M main
git push -u origin main
```

## 后续更新

仓库创建后，每日的自动化任务会自动更新 `daily-reports/` 目录中的报告。

你可以通过以下方式保持 GitHub 同步：

1. **手动同步**: 定期拉取最新报告后推送到 GitHub
2. **GitHub Actions**: 启用 `.github/workflows/sync.yml` 工作流

---

## 项目链接

创建仓库后，分享以下链接：

- **GitHub**: https://github.com/Hongqiong12/ai-security-daily
- **Issues**: https://github.com/Hongqiong12/ai-security-daily/issues

---

*本文件用于指导首次推送，后续不需要再次使用*
