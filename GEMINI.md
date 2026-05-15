# Gemini Project Context: SOGA & Skydog Sports

This project is a combined repository containing the **SOGA (Southwestern Ontario Gliding Association)** official website and a restored mirror of the **Skydog Sports** photography archive.

## Project Overview

### 1. SOGA Website (Root Directory)
The primary website for the Southwestern Ontario Gliding Association.
- **Entry Point:** `index.html` (redirects to `soga.htm`)
- **Main Pages:** `soga.htm`, `aerotow.htm`, `events.htm`, `gallery.htm`, `membership.htm`, `contact2.htm`
- **Technologies:** Static HTML, [Bulma CSS](https://bulma.io/) (via CDN), custom CSS in `styles.css`.
- **Purpose:** Provide information about the club, membership, events, and aerotowing operations.

### 2. Skydog Sports Mirror (`/skydog`)
A massive restoration of the original `skydogsports.com` website, preserving Bob Grant's extensive collection of extreme sports photography and stories.
- **Entry Point:** `skydog/index.html`
- **Structure:** Organized by sport-specific directories (e.g., `A-HG/`, `A-Windsurfing/`, `A-kayaks/`).
- **Content:** ~229 HTML files and thousands of image references.
- **Status:** Restoration is ongoing, with significant effort put into fixing broken image links and relative paths for subdirectory deployment.

## Technical Details

### Restoration Tooling (Python Scripts)
The `/skydog` directory contains several Python scripts used for site maintenance and restoration:
- `fix_image_links.py` / `fix_href_links.py`: Automated repair of broken image and hyperlink paths.
- `complete_final_recovery.py`: Script for systematic content recovery.
- `create_missing_dirs.py`: Reconstructs the original directory structure required by the HTML files.
- `download_missing_images.py`: Attempts to recover images from external sources.

### Development Conventions
- **Static HTML:** Both sites are static. Edits should be made directly to the `.htm` or `.html` files.
- **Link Management:** Ensure all links are relative to support hosting in subdirectories (e.g., `sogaclub.ca/skydog/`).
- **Backups:** Original HTML files in the `/skydog` directory often have `.backup` versions created before running restoration scripts.
- **CSS:** SOGA uses Bulma CSS; Skydog uses legacy inline styles and some shared CSS.

## Key Files
- `soga.htm`: Main entry point for the SOGA club site.
- `skydog/README.md`: Detailed documentation of the Skydog restoration project, including success rates and remaining challenges.
- `skydog/TRANSITION_PLAN.md`: Strategic plan for migrating Skydog content to the SOGA domain.
- `styles.css`: Custom styles for the SOGA website.

## Maintenance Procedures
1. **Adding SOGA Content:** Follow the Bulma-based layout in `soga.htm`.
2. **Fixing Skydog Links:** Use the Python scripts in `/skydog` rather than manual edits for large-scale link repairs.
3. **Image Assets:** Images for SOGA are mostly in the root or `images21/`; Skydog images are scattered within its sport-specific directories.
