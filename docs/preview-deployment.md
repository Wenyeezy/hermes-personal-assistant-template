# Static preview deployment and rollback

The public demo contains only fictional data. Never publish a local runtime, a repository root, private databases, owner records, environment files, or credentials as the public site.

Live public preview: [https://hermes-preview.wenyeezy.com/](https://hermes-preview.wenyeezy.com/).
Its dedicated hostname route points only to `http://127.0.0.1:9082`; the
existing tunnel connector is reused without restarting it or changing its
other routes, tokens, or Access policies. No new AWS inbound port is required.

1. Run tests and `python3 scripts/privacy_check.py`.
2. Build with `python3 scripts/build_preview.py --version 0.1.0-preview.1`.
3. Deploy the archive to an owner-authorized Ubuntu/Nginx host:

   ```bash
   bash scripts/deploy_preview.sh user@your-server /absolute/path/to/key.pem dist/hermes-preview-0.1.0-preview.1.tar.gz
   ```

The script installs a **separate static-only** Nginx origin bound to `127.0.0.1:9082`, validates Nginx before reloading, and retains versioned assets plus a previous-release link. It does not restart or reconfigure private Hermes services. Build media are explicitly allowlisted. Don't use an untrusted archive with this script.

For a permanent public endpoint, add a **new** HTTPS tunnel route for the desired hostname pointing only to `http://127.0.0.1:9082`. Leave existing private tunnel routes and Access policies untouched. DNS/tunnel administration requires your own authorized Cloudflare session or suitably scoped API token; the server's running connector alone is not an administration credential.

A temporary Cloudflare Quick Tunnel can demonstrate the isolated static site without opening AWS inbound ports. Its random hostname is temporary; don't claim it is a stable launch URL. Never point it at any private service. The live preview now uses the fixed HTTPS hostname above; retain a temporary review endpoint only for compatibility with earlier downloads, not as a launch link.

After publishing, verify the HTTPS page, all three simulated actions, mobile layout, exported fictional JSON, CSP headers, `/api/status` returning 404, and unchanged private-service health. Normal host/proxy access logs may exist.

Rollback on the host:

```bash
preview_previous_release="$(readlink -f /var/www/hermes-preview/previous)"
test -f "$preview_previous_release/index.html"
sudo ln -sfn "$preview_previous_release" /var/www/hermes-preview/current
sudo nginx -t
sudo systemctl reload nginx
```

The previous link only exists after a second successful deployment. Resolve it before rolling back; never delete a broad web root or other services. To remove just the new public route, remove its DNS/tunnel mapping first, then disable only `/etc/nginx/sites-enabled/hermes-preview` and reload Nginx after validation. Keep the versioned assets for recovery.
