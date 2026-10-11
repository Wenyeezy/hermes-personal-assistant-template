# Public browser walkthrough

This is a **static, fictional simulation**, separate from the Python runtime and the owner's private Hermes services. It never calls a model or runtime API, sends an application, connects a bank, or persists browser state. Reload or Reset returns the fixtures to their starting values.

```bash
python3 -m http.server 8088 --bind 127.0.0.1 --directory site
```

Open `http://127.0.0.1:8088`. No build dependencies are required. All text, styles, fonts, and fixtures are served locally; no analytics or third-party scripts are loaded. Ordinary hosting access logs may still exist.

Build a strictly allowlisted deployment bundle:

```bash
python3 scripts/build_preview.py --version 0.1.0-preview.1
```

`dist/` is ignored. The builder rejects symlinks and excludes all runtime code, private records, configuration, credentials, and knowledge folders. Deployment instructions are in [docs/preview-deployment.md](../docs/preview-deployment.md). Never deploy the repository root as a website.

The public walkthrough includes simulated confirmation/review transitions for storytelling. The current downloaded runtime supports manual record creation and summaries; it does **not** yet implement these exact in-place edit transitions. This difference is stated on the website and should also be stated in launch material.
