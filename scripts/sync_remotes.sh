#!/usr/bin/env bash
# 双仓库同步推送：GitHub (origin) + 工蜂 (gongfeng)
# 用法：
#   ./scripts/sync_remotes.sh              # 推送当前分支到两个远端
#   ./scripts/sync_remotes.sh main         # 指定分支
#
# 设计原则：任一远端失败不阻断另一个，退出码反映"是否至少一个成功"。

set -uo pipefail

REPO_DIR="/Users/ageisliu/WorkBuddy/Claw/ai-security-daily"
cd "$REPO_DIR" || { echo "[sync] FATAL: 无法进入 $REPO_DIR"; exit 1; }

BRANCH="${1:-$(git rev-parse --abbrev-ref HEAD)}"
TS=$(date '+%F %T')

echo "=============================================="
echo "[sync] $TS  branch=$BRANCH"
echo "=============================================="

SUCCESS=0
FAIL=0

for r in origin gongfeng; do
  URL=$(git remote get-url "$r" 2>/dev/null)
  if [ -z "$URL" ]; then
    echo "[sync] SKIP  $r (remote 未配置)"
    continue
  fi
  echo "[sync] PUSH  $r -> $URL"
  if git push "$r" "$BRANCH" 2>&1; then
    echo "[sync] OK    $r"
    SUCCESS=$((SUCCESS + 1))
  else
    echo "[sync] FAIL  $r  (凭据失效/网络/权限，另一个远端继续)"
    FAIL=$((FAIL + 1))
  fi
  echo "----------------------------------------------"
done

echo "[sync] 结果: 成功 $SUCCESS / 失败 $FAIL"

if [ "$SUCCESS" -eq 0 ]; then
  echo "[sync] 全部远端推送失败。若为凭据问题："
  echo "  GitHub : gh auth login  或  git credential 已缓存"
  echo "  工蜂   : 需 Personal Access Token，见 PUSH_GUIDE.md"
  exit 1
fi

exit 0
