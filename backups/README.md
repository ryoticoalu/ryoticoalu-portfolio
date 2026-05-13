# Backups

Snapshots of `index.html` (and any other live-page file) before changes.

## Convention

Filename: `<file>.<YYYY-MM-DD-HHmm>.bak.<ext>`

Example: `index.html.2026-05-14-1830.bak.html`

The `.bak.<ext>` keeps the extension so editors/browsers still preview the file correctly while making clear it's a backup.

## When backups are taken

**Before any modification to a live-page file** (`index.html` primarily — also any future image, CSS file, JS file the site uses). No exception. This is a non-negotiable project rule — see `workflow-rules.md` in the Portfolio project memory at `C:\Users\ryoti\.claude\projects\C--Claude\memory\projects\portfolio\`.

## How to restore

Say to Claude: **"Restore the last backup"** or **"Restore the backup from `<filename>`"**

Manually:
```powershell
Copy-Item "backups\index.html.<timestamp>.bak.html" -Destination "index.html"
.\deploy.cmd "Restored from backup <timestamp>"
```

## Retention

Keep all backups indefinitely — they're small (~35 KB each) and disk is cheap. Prune only if the folder gets unwieldy (100+ backups), and then only the oldest "auto" snapshots (not "milestone" or pre-release ones).

## Also in Git

Every commit in the repo IS a backup too — the `backups/` folder is a UI convenience for easy filesystem browsing and "restore this specific snapshot" workflows without git knowledge. The two coexist intentionally.
