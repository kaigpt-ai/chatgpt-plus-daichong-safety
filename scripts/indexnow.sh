#!/usr/bin/env bash
# 向 IndexNow 提交本站页面，让 Bing 和 Yandex 更快抓取。
# 用法： ./scripts/indexnow.sh
#
# 密钥文件是仓库根目录的 3f750abfe6fb85c7b7bd0062482b0dae.txt，
# 内容必须与文件名一致，IndexNow 靠它验证域名归属。不要改名或删除。
#
# 注意：IndexNow 只对 Bing / Yandex 等参与方生效，Google 不使用该协议。

set -euo pipefail

KEY="3f750abfe6fb85c7b7bd0062482b0dae"
HOST="pbhhdf.github.io"
BASE="https://${HOST}/chatgpt-membership-safety-guide"

URLS=(
  "${BASE}/"
  "${BASE}/chatgpt-recharge-methods.html"
  "${BASE}/chatgpt-plus-recharge.html"
  "${BASE}/chatgpt-pro-recharge.html"
  "${BASE}/chatgpt-recharge-safety.html"
)

payload=$(python3 - "$KEY" "$HOST" "${URLS[@]}" <<'PY'
import json, sys
key, host, *urls = sys.argv[1:]
print(json.dumps({
    "host": host,
    "key": key,
    "keyLocation": f"https://{host}/chatgpt-membership-safety-guide/{key}.txt",
    "urlList": urls,
}))
PY
)

echo "提交 ${#URLS[@]} 个 URL 到 IndexNow..."
code=$(curl -s -o /tmp/indexnow.out -w '%{http_code}' \
  -X POST "https://api.indexnow.org/indexnow" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d "$payload")

echo "HTTP ${code}"
case "$code" in
  200|202) echo "已接收。IndexNow 返回 200 或 202 表示提交成功，不代表已收录。" ;;
  400) echo "请求格式有误，检查 payload。" ;;
  403) echo "密钥校验失败：确认密钥文件仍在线且内容与文件名一致。" ;;
  422) echo "URL 与 host 不匹配，或密钥位置无效。" ;;
  429) echo "提交过于频繁，稍后再试。" ;;
  *)   echo "未预期的状态码。响应："; cat /tmp/indexnow.out ;;
esac
