@echo off
title Sign of Hope Local Server
cd /d "%~dp0"
echo Starting Sign of Hope on http://localhost:5500
echo Keep this window open while using camera/microphone features.
python -m http.server 5500
pause
