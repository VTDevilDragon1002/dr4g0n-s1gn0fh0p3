#!/usr/bin/env bash
cd "$(dirname "$0")"
echo "Starting Sign of Hope on http://localhost:5500"
python3 -m http.server 5500
