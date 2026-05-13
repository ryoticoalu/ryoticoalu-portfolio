# TODO — Portfolio Improvements

Things to address in future Claude sessions. Loosely ordered by impact.

## Portfolio content

### High priority

- [ ] **Motion reel / showreel section** — embed Vimeo or YouTube. This is the single most important addition for a motion designer's portfolio. Visitors should see motion within 5 seconds of scrolling. Where to put it: probably right after the hero, before "Featured Projects." Or replace the largest placeholder card with the reel.
- [ ] **Replace gradient placeholder project cards with real work** — pull screenshots/thumbnails from Behance (https://www.behance.net/ryoticoalu). Five cards currently: POPL, BOLDe, OPPO, Matahari, FTL. Each `project-image` div needs a real image asset.
- [ ] **Real headshot for About section** — the current "RYO" text placeholder in `.about-image .placeholder-text` should become an `<img>` tag pointing to a real photo. Aspect ratio is 3:4, dark/moody lighting would match the vaporwave theme.

### Medium priority

- [ ] **Verify LinkedIn URL** — `https://www.linkedin.com/in/ryoticoalu` is currently linked. Confirm it resolves.
- [ ] **Fix Facebook link** — currently `href="#"` (broken placeholder) in footer social list. Either populate or remove the row.
- [ ] **Add web analytics** — Cloudflare Web Analytics is free and the simplest option (no GDPR cookie banner needed since it's privacy-friendly). Alternative: Google Analytics 4 if you want richer demographic data. Cloudflare path: dashboard → Web Analytics → add site → copy the JS snippet into `</head>`.

### Lower priority

- [ ] **Custom domain** — buy `ryoticoalu.com` via Cloudflare Registrar (~$10–12/year at-cost pricing; cheaper than GoDaddy/Namecheap because no markup). Then in CF Pages → Custom domains → Set up custom domain → done. Cloudflare handles SSL automatically.
- [ ] **OG image / social card** — currently no `og:image` meta tag. Add one (1200×630 PNG) so links shared on Twitter/LinkedIn/WhatsApp show a preview instead of just text. Could be a still of the hero with the gradient name.
- [ ] **Favicon** — site currently has the browser's default. Add `favicon.ico` or `<link rel="icon">`.
- [ ] **Loading state for fonts** — Google Fonts load asynchronously. Consider adding `font-display: swap` (already might be in Google Fonts URL — check) and a fallback font stack so first paint isn't blank.

## Workflow improvements

- [ ] **GitHub Actions** — beyond auto-deploy (which Cloudflare handles if you wire it up later), consider an Action that runs on every PR:
  - HTML validation via [html-validate](https://html-validate.org/)
  - Lighthouse CI check (performance/accessibility budgets)
  - Spell-check on copy via codespell
- [ ] **Switch to Cloudflare's GitHub auto-deploy** — see [DEPLOY.md](DEPLOY.md#switching-to-github-auto-deploy-optional-later). Removes the manual Wrangler step. Trade-off: every push deploys, including drafts/typos.
- [ ] **Local preview hot-reload** — for richer editing, swap `python -m http.server` for [live-server](https://www.npmjs.com/package/live-server) so saves auto-refresh the browser.

## Creative MCP exploration (post-Windows-MCP)

Things to try once Windows-MCP is stable and you're comfortable with it. These all benefit from a designer's automation but are experimental:

- [ ] **Photoshop layer batch operations** — try [mikechambers/adb-mcp](https://github.com/mikechambers/adb-mcp) for batch layer renaming, structured export of layer comps, or generating boilerplate PSD templates.
- [ ] **After Effects composition generation from briefs** — investigate [Dakkshin/after-effects-mcp](https://github.com/Dakkshin/after-effects-mcp) (ExtendScript-based). Workflow: paste a creative brief → MCP generates an AE composition skeleton with placeholders for footage, text, and animation presets.
- [ ] **Premiere project bootstrapping for podcast episodes** — for the IPGTM podcast workflow specifically. Bootstrap a Premiere project with sequence presets, color labels for guest/host tracks, and audio routing already configured. Saves the per-episode setup time.
- [ ] **Honest reality check first** — community Adobe MCPs require manual UXP plugin installs in each Adobe app. Worth doing a small experiment before committing. Start with Photoshop since it's the most stable target.

## Notes / ideas (not yet TODO)

- A dark/light mode toggle would be off-brand here — the vaporwave aesthetic is intentionally dark. Skip.
- A blog/posts section is a big addition (would need a build step or CMS). Probably not worth it unless you actually plan to write regularly.
- An interactive scene (Three.js / WebGL) in the hero would match the vibe but is a significant time investment. Hold for a v2 redesign.
