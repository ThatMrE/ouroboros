# docs-site — methods & analysis reference (deployable)

A single static page (`index.html`) indexing the study protocol, SAP, data-infra,
bench-test, OSF form, and analysis code. **Methods/code only — no fundraising or
recruitment content.** Safe to publish.

## Deploy it as its OWN Netlify site (separate from the main project)

This is the non-recruitment target. Stand it up as a **new** Netlify site so it's
independent of `ouroboros-dose`:

1. Netlify → **Add new site → Import an existing project → GitHub → `ThatMrE/ouroboros`**.
2. **Base directory:** `docs-site`
3. **Publish directory:** `docs-site`  (no build command — it's static)
4. Deploy. Every push to `master` that touches `docs-site/` auto-updates it.

Equivalent `netlify.toml` if you prefer config-as-code (place at repo root only if this
is the *only* site built from the repo):

```toml
[build]
  base    = "docs-site"
  publish = "docs-site"

[[headers]]
  for = "/*"
  [headers.values]
    X-Frame-Options = "DENY"
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"
    Permissions-Policy = "geolocation=(), microphone=(), camera=()"
```

The doc links point at the GitHub-rendered Markdown, so the page works regardless of
publish directory and needs no build step.
