# Deploy Workflow

How to update [ryoticoalu.pages.dev](https://ryoticoalu.pages.dev).

## TL;DR — one command

From inside `C:\Claude\ryoticoalu-portfolio\`:

```powershell
.\deploy.cmd "what you changed"
```

That commits, pushes to GitHub, and deploys to Cloudflare Pages in one go.

To redeploy without committing (e.g., after a previous deploy failed):

```powershell
.\deploy.cmd
```

## What's actually happening

Cloudflare Pages is **not** wired to auto-deploy from GitHub — every deploy goes through Wrangler from your machine. Two things to keep in sync:

1. **GitHub repo** — source of truth, history, backup
2. **Cloudflare Pages** — what visitors actually see

`deploy.cmd` keeps both in sync. If you only `git push`, the GitHub repo updates but the live site doesn't change.

## Manual workflow (what `deploy.cmd` runs for you)

```powershell
# 1. Edit your site
notepad index.html        # or VS Code, or whatever editor

# 2. Commit + push to GitHub
git add .
git commit -m "Update hero copy"
git push

# 3. Deploy to Cloudflare Pages
wrangler.cmd pages deploy . --project-name=ryoticoalu --commit-dirty=true
```

After step 3, Wrangler prints a deploy URL like `https://<hash>.ryoticoalu.pages.dev` — that's the preview for that specific build. The production URL (`https://ryoticoalu.pages.dev`) updates within a few seconds.

## Why `wrangler.cmd` not `wrangler`

PowerShell's default execution policy blocks the `.ps1` shim that npm installs. The `.cmd` shim is unaffected — it does the same thing. You can ignore this detail; `deploy.cmd` handles it.

If you want to fix it once: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` (then `wrangler` works directly).

## Switching to GitHub auto-deploy (optional, later)

If you'd rather have pushes to `main` auto-deploy, connect the repo in the Cloudflare dashboard:

1. https://dash.cloudflare.com → Workers & Pages → `ryoticoalu` → Settings → Builds & deployments
2. Connect to Git → pick `ryoticoalu/ryoticoalu-portfolio` → main branch
3. Build settings: leave build command empty, output dir `.` (root)

After that, `git push` alone is enough — no Wrangler step. The `deploy.cmd` script still works (it just does an extra Wrangler deploy you don't need).

## Rollback

```powershell
# List recent deploys
wrangler.cmd pages deployment list --project-name=ryoticoalu

# Promote a previous deploy back to production (use the deploy ID)
wrangler.cmd pages deployment tail --project-name=ryoticoalu
```

Or use the Cloudflare dashboard → Pages → `ryoticoalu` → Deployments → "Rollback to this deployment" on a previous build.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `wrangler not recognized` | Open a new PowerShell window — PATH wasn't refreshed |
| `Authentication required` from wrangler | `wrangler.cmd login` again |
| `Permission denied` from git push | `gh auth login` again |
| Site updated on Cloudflare but old version showing | Hard refresh (Ctrl+Shift+R) — browser cache |
