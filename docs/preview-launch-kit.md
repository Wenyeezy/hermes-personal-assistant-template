# Hermes Preview launch kit · Meals + Fitness

Prepared material, not a published X post. Advertising and paid memberships are deferred.

## Downloads and demo

- Public fictional demo: https://hermes-preview.wenyeezy.com/
- Release: https://github.com/Wenyeezy/hermes-personal-assistant-template/releases/tag/v0.1.0-preview.2
- Exact post and reply text: [x-first-post.txt](x-first-post.txt).
- License: MIT. Fork, modify and reuse under the [LICENSE](../LICENSE) terms.

## Images

- `site/media/hermes-preview-wide.png`: 1200 × 675, first X post / pinned post.
- `site/media/hermes-preview-square.png`: 1080 × 1080, alternative cover.
- `site/media/hermes-preview-30s.mp4`: 30 seconds, 1280 × 720, silent illustrative launch video. The export has a visible Descript watermark.

These are browser captures of repo-native HTML/CSS launch sheets, using only fictional samples. They are illustrations of the product focus, not screenshots of owner data or an AI-generated interface. Rebuildable binary exports are excluded from Git and attached to the release.

Run the static server from [site/README.md](../site/README.md). Capture `launch.html?format=wide` at 1200 × 675, or `launch.html?format=square` at 1080 × 1080. Video stills use a 1280 × 720 viewport and the `scene` query below. No photographic editing is required.

## 30-second storyboard

| Time | Scene query | Message |
| --- | --- | --- |
| 0–6 s | `scene=cover` | Meals + fitness first; finance is off / opt-in. |
| 6–12 s | `scene=meal` | A fictional confirmed meal, reviewed by the user. |
| 12–18 s | `scene=workout` | A manually entered fictional walk. No device connected. |
| 18–24 s | `scene=summary` | Fictional confirmed meal totals and recorded movement. |
| 24–30 s | `scene=install` | Python 3.10+, one command, no GPT or API key required. |

This is a scripted slideshow of launch illustrations, not a live screen recording. The separate interactive browser demo simulates confirmation and record receipts. The Python runtime now also supports real local manual records and in-place meal confirmation; its storage is separate from the website.

Adobe accepted a render but did not expose its compatible completion-query tool in this session. The delivered video was assembled and exported through Descript. Its duration, dimensions and all five scenes were checked in-browser. No paid plan was purchased, and the watermark was not removed.

## X first post

> After months of building & polishing, Hermes Preview is live.
>
> A local-first workspace for meals, workouts & daily activity.
>
> Try the fictional demo, or run it locally. No GPT required.
> https://hermes-preview.wenyeezy.com/
>
> Feedback welcome.

Use the wide cover or MP4; do not attach both cover variants to one post. “Months” avoids asserting an unverified June start or exact three-month polish period.

## Follow-up reply

Link the repository and explain the essentials:

- MIT licensed; fork it or download the source ZIP.
- Start with `python3 scripts/hermes.py start --open` (Windows: `py -3`). Add `--demo` only to try isolated fictional data.
- Manual meals, workout records and local summaries work without an AI account.
- Finance requires explicit opt-in; disabling it keeps local records and blocks dashboard API access.
- Optional AI chat uses the user's own setup and does not automatically save meals or workouts. A compatible local chat gateway is optional; native production Hermes MCP/memory is not bundled.
- iOS companion is later. Bank sync and a hosted personal-data service are not included.

Keep CertiK consulting messaging separate. Do not imply endorsement, shared private data or a bundled commercial relationship.

## Publishing boundaries

Use the fixed HTTPS demo hostname, not the old Quick Tunnel URL. Inspect the latest release ZIP and fictional assets before posting. Local data is unencrypted. Do not promise medical, financial or employment outcomes.

The current video is usable as a watermarked preview; a clean promotional export would require a separately authorized export. Preparing this kit does not publish to X, connect an account, buy a membership, register a campaign or spend on advertising.
