@echo off
setlocal
cd /d "%~dp0"
py -3 -c "import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)" >nul 2>&1
if not errorlevel 1 (
  py -3 scripts/hermes.py start --open
) else (
  python -c "import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)" >nul 2>&1
  if errorlevel 1 (
    echo Install Python 3.10 or newer from https://www.python.org/downloads/
  ) else (
    python scripts/hermes.py start --open
  )
)
pause
