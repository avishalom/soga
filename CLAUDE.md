# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Two static HTML sites in one repository, served by GitHub Pages at **sogaclub.ca** (see `CNAME`):

1. **SOGA website** (repo root) — the Southwestern Ontario Gliding Association club site.
2. **Skydog Sports mirror** (`skydog/`) — an ongoing restoration of the offline `skydogsports.com` photography archive (~229 HTML files, thousands of image references).

There is no build system, linter, or test suite. Edit `.htm`/`.html` files directly. To preview locally: `python3 -m http.server` from the repo root.

## Deployment (important)

The live site is served from the **gh-pages** branch. Always merge changes to **master first**, then deploy by merging master into gh-pages and pushing:

```
git checkout master && git merge <feature-branch> && git push
git checkout gh-pages && git merge master && git push
git checkout master
```

Never commit directly to gh-pages ahead of master.

## SOGA site (root)

- `index.html` is just a redirect to `soga.htm`, the real home page.
- The live pages are the ones linked from the `soga.htm` nav: `soga.htm`, `aerotow.htm`, `beginner.htm`, `experienced.htm`, `events.htm`, `gallery.htm`, `membership.htm`, `contact2.htm`. (`advanced.htm`, `joining.htm`, `blogs3.htm`, `associate.htm` are also current-generation pages reachable from those.)
- The root is littered with stale drafts and old versions — `*.old`, `*.htmold`, and numbered variants like `index2.htm`, `contact22.htm`, `membership2.htm`, `aerotow3.htm`. Do not edit these; they are not served as part of the live nav.
- Layout uses [Bulma CSS](https://bulma.io/) via CDN plus custom rules in `styles.css`. New pages should copy the Bulma-based structure of `soga.htm`.
- Images live in the repo root and `images21/`.
- `membership.htm` embeds the PayPal SDK for membership payments.

## Skydog mirror (`skydog/`)

- Entry point `skydog/index.html`; content organized in sport-specific directories (`A-HG/`, `A-Windsurfing/`, `A-kayaks/`, `A-TRIKE/`, etc.).
- Restoration status, statistics, and known problems are documented in `skydog/README.md`; migration strategy in `skydog/TRANSITION_PLAN.md`.
- For large-scale link/image repairs, use the Python scripts in `skydog/` (`fix_image_links.py`, `fix_href_links.py`, `complete_final_recovery.py`, `create_missing_dirs.py`, `download_missing_images.py`) rather than manual edits.
- Scripts create `.backup` copies of HTML files before modifying them — leave those in place.
- Keep all links **relative** so the site works when hosted under a subdirectory (`sogaclub.ca/skydog/`).
