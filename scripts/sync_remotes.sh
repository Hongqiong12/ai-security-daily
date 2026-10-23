#!/usr/bin/env bash
# 双仓库同步推送
#   origin    → GitHub  : https://github.com/Hongqiong12/ai-security-daily      分支 main
#   gongfeng  → 工蜂    : https://git.woa.com/aegisliu/ai-security-daily        分支 master
#
# 用法：
#   bash scripts/sync_remotes.sh          # 同步两个远端
#   bash scripts/sync_remotes.sh github   # 只推 GitHub
#   bash scripts/sync_remotes.sh gongfeng # 只推工蜂
#
# 为什么工蜂不能简单 git push：
#   工蜂开启了 committer-check，要求 committer 属于账号 aegisliu。
#   本仓库历史 commit 的身份是 sentinelliu(github noreply)，直接 push 会被拒：
#     "You can't push commit[xxx] with committer[sentinelliu] ... does not belong to the account[aegisliu]"
#   因此工蜂侧采用「快照同步」：在 gongfeng/master 之上追加一个 commit，
#   文件树内容直接取自本地 main，committer 强制为 aegisliu <aegisliu@tencent.com>。
#   代价：工蜂历史是快照式（每次同步 1 个 commit），与 GitHub 完整历史不同；
#   收益：不 force push、不改历史、内容始终一致。

set -uo pipefail

REPO_DIR="/Users/ageisliu/WorkBuddy/Claw/ai-security-daily"
SRC_BRANCH="main"
GF_BRANCH="master"
GF_NAME="aegisliu"
GF_EMAIL="aegisliu@tencent.com"

cd "$REPO_DIR" || { echo "[sync] FATAL: 无法进入 $REPO_DIR"; exit 1; }

TARGET="${1:-all}"
TS=$(date '+%F %T')
echo "=============================================="
echo "[sync] $TS  target=$TARGET  source=$SRC_BRANCH"
echo "=============================================="

SUCCESS=0
FAIL=0

# ---------- 1. GitHub ----------
push_github() {
  local url
  url=$(git remote get-url origin 2>/dev/null)
  if [ -z "$url" ]; then
    echo "[github] SKIP (remote origin 未配置)"; return
  fi
  echo "[github] PUSH origin/$SRC_BRANCH -> $url"
  if git push origin "$SRC_BRANCH" 2>&1 | sed 's/^/    /'; then
    echo "[github] OK"; SUCCESS=$((SUCCESS + 1))
  else
    echo "[github] FAIL"; FAIL=$((FAIL + 1))
  fi
}

# ---------- 2. 工蜂（快照同步） ----------
push_gongfeng() {
  local url
  url=$(git remote get-url gongfeng 2>/dev/null)
  if [ -z "$url" ]; then
    echo "[gongfeng] SKIP (remote gongfeng 未配置)"; return
  fi
  echo "[gongfeng] FETCH $url"
  git fetch gongfeng "$GF_BRANCH" 2>&1 | sed 's/^/    /'

  local base
  base=$(git rev-parse --verify "refs/remotes/gongfeng/$GF_BRANCH" 2>/dev/null)
  if [ -z "$base" ]; then
    echo "[gongfeng] FAIL: 远端分支 $GF_BRANCH 不存在，请先在工蜂创建仓库/分支"
    FAIL=$((FAIL + 1)); return
  fi

  local tmp
  tmp=$(mktemp -d)/gf-sync
  if ! git worktree add --detach "$tmp" "$base" >/dev/null 2>&1; then
    echo "[gongfeng] FAIL: 无法创建临时 worktree"; FAIL=$((FAIL + 1)); return
  fi

  (
    cd "$tmp" || exit 1
    git read-tree -u --reset "$SRC_BRANCH" || exit 1
    if git diff --cached --quiet; then
      echo "[gongfeng] SKIP: 内容已与 $SRC_BRANCH 一致，无需提交"
      exit 0
    fi
    local n
    n=$(git status --short | wc -l | tr -d ' ')
    echo "[gongfeng] COMMIT 快照同步（$n 个文件变更）"
    GIT_AUTHOR_NAME="$GF_NAME" GIT_AUTHOR_EMAIL="$GF_EMAIL" \
    GIT_COMMITTER_NAME="$GF_NAME" GIT_COMMITTER_EMAIL="$GF_EMAIL" \
      git commit -q -m "sync: 同步 $SRC_BRANCH 快照 $(date '+%F %T')" || exit 1
    echo "[gongfeng] PUSH -> $GF_BRANCH"
    git push gongfeng "HEAD:$GF_BRANCH" 2>&1 | sed 's/^/    /'
  )
  local rc=$?

  git worktree remove --force "$tmp" >/dev/null 2>&1
  rm -rf "$(dirname "$tmp")" 2>/dev/null

  if [ $rc -eq 0 ]; then
    echo "[gongfeng] OK"; SUCCESS=$((SUCCESS + 1))
  else
    echo "[gongfeng] FAIL (见上方 remote 输出)"; FAIL=$((FAIL + 1))
  fi
}

case "$TARGET" in
  github)   push_github ;;
  gongfeng) push_gongfeng ;;
  all)      push_github; echo "----------------------------------------------"; push_gongfeng ;;
  *)        echo "[sync] 未知参数: $TARGET (可选 github|gongfeng|all)"; exit 1 ;;
esac

echo "=============================================="
echo "[sync] 结果: 成功 $SUCCESS / 失败 $FAIL"

if [ "$SUCCESS" -eq 0 ]; then
  echo "[sync] 全部失败。排查见 PUSH_GUIDE.md"
  exit 1
fi
exit 0
