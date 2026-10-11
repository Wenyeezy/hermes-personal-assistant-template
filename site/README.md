# Public browser walkthrough

This is a **static, fictional simulation**, separate from the Python runtime and the owner's private Hermes services. It never calls a model or runtime API, sends an application, connects a bank, or persists browser state. Reload or Reset returns the fixtures to their starting values.

```bash
python3 -m http.server 8088 --bind 127.0.0.1 --directory site
```

Open `http://127.0.0.1:8088`. No build dependencies are required. All text, styles, fonts, and fixtures are served locally; no analytics or third-party scripts are loaded. Ordinary hosting access logs may still exist.

Build a strictly allowlisted deployment bundle:

```bash
python3 scripts/build_preview.py --version 0.1.0-preview.2
```

`dist/` is ignored. The builder rejects symlinks and excludes all runtime code, private records, configuration, credentials, and knowledge folders. Deployment instructions are in [docs/preview-deployment.md](../docs/preview-deployment.md). Never deploy the repository root as a website.

Nutrition is the default demo. Confirm a fictional meal, log a fictional walk,
and optionally enable Finance. Reset or reload returns Finance to off.
Exports omit the fictional ledger while Finance is off. All receipts are
simulated browser events, not private runtime writes.

The downloaded runtime now supports explicit in-place meal confirmation and
manual workouts, but this website remains an independent simulation.
`launch.html?format=wide` / `square` supplies native 1200×675 / 1080×1080
launch layouts. `launch.html?scene=cover|meal|workout|summary|install` supplies
1280×720 fictional storyboard frames. No photo editing is needed.
