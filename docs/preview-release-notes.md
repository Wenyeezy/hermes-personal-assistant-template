# Hermes Life v0.1.0-preview.2 · Meals + Fitness

## New in this preview

- Nutrition and Fitness are the default first-run experience. No GPT required.
- Finance and Career are off by default, with explicit persisted opt-in and
  dashboard API gates. Existing data is preserved; older configs also default off.
- Review and confirm an existing meal without duplicating it.
- Daily workout totals and a fix for multiple independent manual workouts.
- Collapsed optional AI/photo settings and simpler workout-first forms.
- macOS/Windows convenience launchers, bilingual README and one-command start.
- MIT license, explicitly selected by the repository owner.
- Updated fictional AWS demo and meals/fitness launch media.

Download the latest source ZIP and run:

```sh
python3 scripts/hermes.py start --open
```

Python 3.10+; Windows can use `py -3`. Add `--demo` for isolated fictional data.
The demo website is not a hosted personal-data service. Chat adapters do not
auto-write records. The iOS companion, bank sync and production Hermes memory
or MCP gateway are not included. Local data is unencrypted.

## Verified for this update

29 Python tests and the privacy scan pass. Desktop and mobile browser checks
cover local meal confirmation, multiple workouts, persisted Finance opt-in and
disabled API access. Static-demo reset and fictional export were also checked.
The new video is 30 seconds at 1280 × 720; all five scenes were inspected.
It is an illustrative slideshow with a visible Descript watermark, not a live
screen recording. No paid plan, advertising or X post was purchased/published.

## Historical notes: v0.1.0-preview.1

The following describes the original archive and its original launch assets.
Its tag and downloadable source have not been replaced. The current repository
and v0.1.0-preview.2 use MIT licensing and the new meals/fitness-first workflow.

### Original release

An early public preview, not the maintainer's private assistant and not a stable production release.

## Try it

- [AWS fictional browser demo](https://hermes-preview.wenyeezy.com/).
- Download `hermes-life-v0.1.0-preview.1.zip`, extract it, and open a terminal in the extracted folder. With Python 3.10+ installed:

  ```sh
  python3 scripts/hermes.py start --demo --open
  ```

  Windows: use `py -3`. No Git, Codex, account, API key or extra Python packages are required. The default Echo is offline, not an AI model. Use `start --open` without `--demo` for your normal private workspace.

## Included

- Localhost dashboard with manual Nutrition, Health, Finance and Career records.
- Isolated fictional samples; safe repeated first run and preserved existing data.
- Bilingual README, installation troubleshooting, clear privacy/capability boundaries.
- Separate static browser simulation with review receipts, fictional JSON export, reset and keyboard controls.
- Strictly allowlisted AWS/Nginx build and rollback-aware deployment.
- Wide/square X images and a 30-second silent fictional walkthrough. These are prepared assets, not a posted campaign.

The current MP4 carries a visible Descript export watermark. It is suitable for
review; a clean promotional export remains a separate step. No paid plan was purchased.

## Verified

23 Python tests and privacy scan; CI on Python 3.10, 3.11 and 3.12; fresh ZIP setup and repeated start; desktop/mobile browser checks; fictional export and confirmed-only totals; local save receipt; public runtime API isolation; video duration/dimensions and scene inspection.

## Limits

The browser's in-place confirmation transitions are simulated; the downloaded runtime currently creates manual records and summaries. Owner-wide memory, production gateways, private accounts, automatic applications and bank sync are not included. Local SQLite/Markdown are not encrypted. Cloud providers and device adapters are optional and use your own setup/accounts.

The AWS site now has a fixed HTTPS hostname pointing only to the isolated static origin. The previous temporary Quick Tunnel address is not the launch link. Existing private tunnel routes and Access policies were not changed. The fixed domain was added after the initial release packaging; the original source archive and release tag remain unchanged, while the current README on main and these release notes point to the fixed address.

No open-source license has been granted; public visibility is not a license. Rights remain with the repository owner. No medical, financial or employment guarantee is offered. No X post, advertising registration, ad spend or paid membership purchase is part of this release.
