#!/usr/bin/env bash
set -eu
if [[ -z "${CLOUDFLARE_API_TOKEN:-}" ]]; then
    echo 'error: $CLOUDFLARE_API_TOKEN not set'
    exit 1
fi
cd "$(dirname "$0")"
poetry run ./build.py
cd ./public
if [[ -n "$(find . -type f -ipath '*private*')" ]]; then
    echo 'abort: deployment contains private notes'
    exit 1
fi
if grep -qr '^draft: true'; then
    echo 'abort: deployment contains drafts'
    exit 1
fi
exec wrangler pages deploy --project-name pentest-notes --commit-dirty true .
