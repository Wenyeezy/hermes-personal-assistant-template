# Hermes Life preview launch kit

Status: draft material, not a published X post. Advertising is deferred.

## Images

- `site/media/hermes-preview-wide.png`: 1200 × 675, homepage / pinned post.
- `site/media/hermes-preview-square.png`: 1080 × 1080, alternate feed image.
- `site/media/hermes-preview-30s.mp4`: verified 30-second, 1280 × 720 silent walkthrough; the current Descript export has a visible Descript watermark.

These are native browser captures of the code-rendered fictional preview, not pictures of the owner's data. They are rebuildable exports excluded from Git. Downloadable copies belong in the release assets.

To reproduce, run the static server from `site/README.md`, open `/?media=wide` at a 1200 × 675 viewport or `/?media=square` at 1080 × 1080, and capture the viewport. No photographic editing or invented interface elements are required.

## 30-second video storyboard

An explicitly scripted, silent walkthrough assembled from fictional UI frames:

| Time | Scene | Message |
| --- | --- | --- |
| 0–6 s | Wide homepage | A local-first public preview, using a fictional day. |
| 6–12 s | Career / saved sample | One opportunity and a visible next step. No application sent. |
| 12–17 s | Nutrition / pending | 420 kcal confirmed; fictional lunch stays separate. |
| 17–24 s | Nutrition / confirmed | A simulated review changes the total to 1,030 kcal. |
| 24–30 s | Local installation | Python 3.10+, one command, no API key required. |

Scene frames use 1280 × 720 and `/?media=career`, `/?media=nutrition`, and `/?media=install`. The nutrition before/after transition is a **browser simulation**, not a claim that the Python runtime already has in-place editing. The Adobe render was accepted but its completion-query tool was unavailable. The final video was assembled/exported through Descript and verified in-browser for duration, dimensions and scene content; it is not an AI-generated product screen recording.

## X launch post (draft)

> Hermes Life public preview: a local-first workspace for career, nutrition, activity & expense records.
>
> Try a fictional day—no signup or model calls. Or run the Python starter locally.
>
> Early, small, useful. Feedback welcome.
>
> [Replace with the verified permanent demo URL]

Attach the wide image or the verified 30-second MP4. Do not post both versions of the same cover in one tweet. The temporary AWS quick-tunnel hostname is for review, not the permanent launch link.

## Follow-up thread (draft)

1. Why: everyday context gets scattered. This preview starts with a few simple records and a clear next step.
2. What runs locally: manual records, summaries, a dashboard, SQLite, and Markdown. No third-party Python dependencies.
3. Boundary: offline Echo is a test adapter. Real model integrations are optional and use your own accounts. Private owner memory and services are not in the download.
4. Try it: download the preview, then run `python3 scripts/hermes.py start --demo --open`. Tell me where you got stuck.

## Before publishing

- Use a permanent HTTPS hostname, not a transient Quick Tunnel link.
- The current MP4 is a watermarked preview export. For a clean launch video,
  obtain an authorized watermark-free export; no paid plan was purchased here.
- Confirm the release download and one-command setup on a fresh ZIP copy.
- Verify images show only fictional samples; label the scripted walkthrough.
- Avoid “open source” until an explicit license is selected; the repository is public, license pending.
- Keep CertiK consulting messaging separate from Hermes product claims. Don't imply endorsement, data sharing, or a bundled commercial relationship.
- No post, paid membership, campaign registration, or advertising purchase is authorized by preparing this kit.
