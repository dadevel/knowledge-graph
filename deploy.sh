#!/usr/bin/env bash
set -eu
cd "$(dirname "$0")"
poetry run ./build.py
cd ./public
if [[ -n "$(find . -type f -ipath '*private*')" ]]; then
    echo 'abort: deployment contains private notes'
    exit 1
fi
exec wrangler pages deploy --project-name pentest-notes --commit-dirty true .
