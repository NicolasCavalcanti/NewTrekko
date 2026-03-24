#!/usr/bin/env bash
# verify-cdn.sh — Smoke-test CloudFront delivery and WebP content negotiation.
#
# Usage:
#   ./infra/verify-cdn.sh https://cdn.trekko.com.br trails/example.jpg
#
# What it checks:
#   1. HTTP 200 on the first request (CDN miss — X-Cache: Miss from cloudfront)
#   2. X-Cache: Hit from cloudfront on a second request
#   3. WebP rewrite: with Accept: image/webp the response content-type is image/webp
#   4. Cache-Control header contains "max-age=2592000"

set -euo pipefail

CDN_ORIGIN="${1:-}"
IMAGE_KEY="${2:-}"

if [[ -z "$CDN_ORIGIN" || -z "$IMAGE_KEY" ]]; then
  echo "Usage: $0 <cdn-origin> <image-key>"
  echo "  e.g. $0 https://cdn.trekko.com.br trails/123/hero.jpg"
  exit 1
fi

URL="${CDN_ORIGIN%/}/${IMAGE_KEY#/}"

PASS=0
FAIL=0

check() {
  local label="$1"; shift
  if "$@"; then
    echo "  PASS  $label"
    ((PASS++)) || true
  else
    echo "  FAIL  $label"
    ((FAIL++)) || true
  fi
}

echo ""
echo "=== Verifying CDN delivery: $URL ==="
echo ""

# ── First request (expect cache miss) ───────────────────────────────────────
echo "--- Request 1 (cold cache) ---"
HEADERS1=$(curl -sI "$URL")
echo "$HEADERS1"

check "HTTP 200" bash -c "[[ \$(echo '$HEADERS1' | grep -i '^HTTP') == *'200'* ]]"
check "Cache-Control: max-age=2592000" bash -c \
  "echo '$HEADERS1' | grep -qi 'cache-control:.*max-age=2592000'"

# ── Second request (expect cache hit) ────────────────────────────────────────
echo ""
echo "--- Request 2 (warm cache) ---"
HEADERS2=$(curl -sI "$URL")
echo "$HEADERS2"

check "X-Cache: Hit from cloudfront" bash -c \
  "echo '$HEADERS2' | grep -qi 'x-cache:.*hit from cloudfront'"

# ── WebP content negotiation ─────────────────────────────────────────────────
echo ""
echo "--- WebP negotiation (Accept: image/webp) ---"
HEADERS_WEBP=$(curl -sI -H "Accept: image/webp,image/*,*/*;q=0.8" "$URL")
echo "$HEADERS_WEBP"

check "Content-Type: image/webp (or WebP rewrite served)" bash -c \
  "echo '$HEADERS_WEBP' | grep -qi 'content-type:.*webp'"

# ── Summary ───────────────────────────────────────────────────────────────────
echo ""
echo "Results: ${PASS} passed, ${FAIL} failed"
[[ $FAIL -eq 0 ]] && exit 0 || exit 1
