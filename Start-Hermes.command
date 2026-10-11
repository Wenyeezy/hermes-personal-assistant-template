#!/bin/sh
# Local-only launcher. No installs, account connections, or background services.
hermes_folder=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd) || exit 1
cd "$hermes_folder" || exit 1
if ! command -v python3 >/dev/null 2>&1 || ! python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)'; then
  printf '%s\n' 'Install Python 3.10 or newer, then open this launcher again.' 'Download: https://www.python.org/downloads/'
  printf '%s' 'Press Enter to close: '
  read -r hermes_answer
  exit 1
fi
python3 scripts/hermes.py start --open
printf '%s' 'Hermes stopped. Press Enter to close: '
read -r hermes_answer
