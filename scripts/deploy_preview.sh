#!/usr/bin/env bash
# Usage: bash scripts/deploy_preview.sh user@host /absolute/key.pem dist/bundle.tar.gz
# A public HTTPS route is a separate, explicit setup; this origin is loopback-only.
set -euo pipefail
if [[ $# != 3 ]]; then
  echo 'Usage: bash scripts/deploy_preview.sh user@host /absolute/key.pem dist/bundle.tar.gz' >&2
  exit 2
fi
preview_host="$1"
preview_key="$2"
preview_bundle="$3"
preview_repo="$(cd "$(dirname "$0")/.." && pwd)"
[[ -f "$preview_key" && -f "$preview_bundle" ]] || { echo 'Missing key or bundle.' >&2; exit 2; }
preview_digest="$(shasum -a 256 "$preview_bundle" | cut -c1-16)"
preview_release="preview-$preview_digest"
preview_remote="$(ssh -i "$preview_key" -o BatchMode=yes -o ConnectTimeout=10 "$preview_host" 'mktemp -d /tmp/hermes-preview-deploy.XXXXXX')"
[[ "$preview_remote" =~ ^/tmp/hermes-preview-deploy\.[A-Za-z0-9]+$ ]] || { echo 'Invalid remote staging path.' >&2; exit 2; }
scp -q -i "$preview_key" "$preview_bundle" "$preview_host:$preview_remote/bundle.tar.gz"
scp -q -i "$preview_key" "$preview_repo/site/nginx-preview.conf" "$preview_host:$preview_remote/nginx-preview.conf"
ssh -i "$preview_key" -o BatchMode=yes "$preview_host" bash -s -- "$preview_remote" "$preview_release" <<'REMOTE'
set -euo pipefail
preview_staging="$1"
preview_release="$2"
[[ "$preview_release" =~ ^preview-[a-f0-9]{16}$ ]] || exit 2
preview_root=/var/www/hermes-preview
preview_target="$preview_root/releases/$preview_release"
# The local builder produces only allowlisted files; independently reject traversal.
tar -tzf "$preview_staging/bundle.tar.gz" | while IFS= read -r entry; do
  case "$entry" in index.html|styles.css|media.css|app.js|fixtures.js|icon.svg|manifest.json|media/hermes-preview-wide.png|media/hermes-preview-square.png|media/hermes-preview-30s.mp4) ;; *) echo 'Unexpected public asset' >&2; exit 2 ;; esac
done
sudo install -d -m 755 "$preview_target"
sudo tar -xzf "$preview_staging/bundle.tar.gz" --no-same-owner -C "$preview_target"
test -f "$preview_target/index.html"
preview_previous="$(readlink "$preview_root/current" || true)"
if [[ -n "$preview_previous" ]]; then sudo ln -sfn "$preview_previous" "$preview_root/previous"; fi
sudo ln -sfn "$preview_target" "$preview_root/current"
preview_config=/etc/nginx/sites-available/hermes-preview
preview_config_backup="$preview_staging/previous-nginx.conf"
if [[ -f "$preview_config" ]]; then sudo cp "$preview_config" "$preview_config_backup"; fi
sudo install -m 644 "$preview_staging/nginx-preview.conf" "$preview_config"
sudo ln -sfn "$preview_config" /etc/nginx/sites-enabled/hermes-preview
if ! sudo nginx -t; then
  if [[ -f "$preview_config_backup" ]]; then sudo install -m 644 "$preview_config_backup" "$preview_config";
  else sudo unlink /etc/nginx/sites-enabled/hermes-preview; fi
  if [[ -n "$preview_previous" ]]; then sudo ln -sfn "$preview_previous" "$preview_root/current"; fi
  echo 'Nginx validation failed; previous configuration restored.' >&2
  exit 1
fi
sudo systemctl reload nginx
curl --fail --silent --retry 5 --retry-connrefused --retry-delay 1 http://127.0.0.1:9082/manifest.json
echo
echo 'Static origin ready on 127.0.0.1:9082. Existing private origins are unchanged.'
REMOTE
