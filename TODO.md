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

## Creative MCP exploration

### Next install: Dakkshin/after-effects-mcp (scheduled for a focused session)

**Why this one, decided 2026-05-14**: AE-MCP talks to AE's native ExtendScript API — fast, precise, robust to UI changes. Windows-MCP alone for AE is wrong (brittle pixel-clicking). 354 stars, MIT license, last push 2026-04-01. The friction is real but pays off for any structured AE work. See [Dakkshin/after-effects-mcp](https://github.com/Dakkshin/after-effects-mcp).

**Why I rejected `pypi:adobe-mcp`** (researched 2026-05-14): the linked GitHub repo `VoidChecksum/adobe-mcp` 404s — no public source for a tool that gets COM-automation access to Adobe apps. Skip until either restored or independently verified.

**Prerequisites before next session:**
- [ ] Set aside ~30 min of focused time (this is NOT a 5-min thing)
- [ ] Have After Effects 2022 or later open
- [ ] Have a clear test case in mind — recommended first prompt: *"Create a 1920×1080 30fps 10-second comp called 'TEST', add a text layer with the word 'HELLO', animate its position from (-200, 540) to (960, 540) over 1 second with ease-out keyframes."* If this works end-to-end, the install is solid.
- [ ] Node.js already installed (✓ done 2026-05-13)

**Install steps to run in next session:**
```powershell
cd C:\Claude
git clone https://github.com/Dakkshin/after-effects-mcp.git
cd after-effects-mcp
npm install
npm run build
npm run install-bridge      # writes mcp-bridge-auto.jsx into AE's Scripts folder
```

**Then in After Effects:**
1. Window menu → mcp-bridge-auto.jsx (panel appears)
2. Check "Auto-run commands" in the panel
3. Keep AE foreground for COM operations to work reliably

**Then add to Claude (next session):**
```powershell
claude mcp add ae-mcp --transport stdio -s user -- node C:\Claude\after-effects-mcp\build\index.js
```

**Risks logged:**
- Install modifies AE's Scripts folder (reversible — delete the `.jsx` to undo)
- Issue #7 from May 2025 had multiple "can't use any feature" reports. Year old, may be fixed, no resolution thread. If first test fails, check issues #7, #22, #23 before reinstalling.
- Project pace is slowing (6 weeks since last push). Not abandoned, but not hot either.

**Tools the MCP exposes (from README):**
`create-composition`, `run-script`, `get-results`, `get-help`, `setLayerKeyframe`, `setLayerExpression`, `setLayerProperties`, `batchSetLayerProperties`, `getLayerInfo`, `createCamera`, `createNullObject`, `duplicateLayer`, `deleteLayer`, `setLayerMask` (14 total).

### The end-goal use case: podcast episode scaffolding

For the IPGTM podcast workflow specifically — once AE-MCP is in: define a template brief format ("guest name, episode number, intro length, key talking points") → Claude scaffolds the AE comp with title cards, lower-thirds placeholders, and standard transitions → I review and tweak. Realistic time savings: hours per episode.

### Other Adobe MCPs (deferred, not next)

- [Dakkshin/after-effects-mcp](https://github.com/Dakkshin/after-effects-mcp) — already covered above
- [hetpatel-11/Adobe_Premiere_Pro_MCP](https://github.com/hetpatel-11/Adobe_Premiere_Pro_MCP) — 214 stars, pushed 2026-05-11. Premiere-specific. Try after AE-MCP if it pans out.
- [mikechambers/adb-mcp](https://github.com/mikechambers/adb-mcp) — PS + PR via UXP plugins. The OG. Lower priority since we're going AE-first.
- [Official Adobe for Creativity connector](https://developer.adobe.com/adobe-for-creativity/) — Claude.ai web app, zero install. Different use case (Adobe cloud APIs + Firefly, not local app automation). Worth enabling in Claude.ai for content generation tasks.

## Notes / ideas (not yet TODO)

- A dark/light mode toggle would be off-brand here — the vaporwave aesthetic is intentionally dark. Skip.
- A blog/posts section is a big addition (would need a build step or CMS). Probably not worth it unless you actually plan to write regularly.
- An interactive scene (Three.js / WebGL) in the hero would match the vibe but is a significant time investment. Hold for a v2 redesign.
