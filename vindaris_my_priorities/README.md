# Vindaris: My Priorities (Odoo module)

Adds a **My Priorities** screen to Odoo that shows the Vindaris goals you own and
the tasks assigned to you, by iframing the hosted Vindaris embed page
(`https://app.vindaris.com/embed/odoo`). It mirrors the Jira Forge panel and the
Microsoft Teams tab.

The module is **views + static assets only, with no server Python**, so it
installs on **Odoo Online** (via Apps -> Import Module) as well as Odoo.sh and
self-hosted. No API keys are pasted and no passwords are handled in Odoo.

## How it works

1. Open **My Priorities**. The screen iframes the Vindaris embed page.
2. The first time, it shows **Connect Vindaris**. Click it, sign in to Vindaris
   in the window that opens, and the screen fills with your goals and tasks.
3. The embed page keeps a short-lived token in its own (Vindaris-origin) storage,
   so later opens go straight to your priorities until it expires, then it asks
   to reconnect.

All sign-in happens in a first-party Vindaris window, so it does not rely on
third-party cookies (which are blocked inside the Odoo iframe). The screen is
read-only.

## Installing

- **Odoo Online:** turn on developer mode, then Apps -> **Import Module**, and
  upload this module (zip of the `vindaris_my_priorities` folder, or install it
  from the Apps store listing). Online accepts it because it has no server code.
- **Odoo.sh:** add the module to the instance repo, or use "Deploy on Odoo.sh"
  from the Apps store listing.
- **Self-hosted:** drop the folder into an addons path and install from Apps.

## Where it works

The screen renders by iframing `app.vindaris.com/embed/odoo`, and a browser only
loads that iframe if the Vindaris CSP lists the Odoo host as an allowed frame
ancestor. The current allowlist is `https://*.odoo.com`.

| Odoo deployment | Host | My Priorities screen |
| --- | --- | --- |
| **Odoo Online** (SaaS) | `yourco.odoo.com` | Works |
| **Odoo.sh** on the default domain | `yourco.odoo.com` | Works |
| **Odoo.sh / self-hosted on a custom domain** | `odoo.yourco.com` | Blocked by CSP |
| **Self-hosted** on any non-`*.odoo.com` host | e.g. `erp.acme.de` | Blocked by CSP |

Supporting a custom domain later means adding a per-instance dynamic
`frame-ancestors` header on Vindaris, or a native (fetch-JSON-and-render)
fallback like the Jira Forge panel.

## Vindaris side

- `/embed/odoo` (the iframe target) + `/embed/odoo/authorize` (the sign-in popup)
  + `GET /api/embed/odoo/token` (session -> short-lived embed token). Rendering
  reuses `/embed/priorities` and `getMemberPriorities`.
- Env: `EMBED_TOKEN_SECRET` (already set in prod; signs the embed token).
- CSP: `src/proxy.ts` allows `https://*.odoo.com` to frame `/embed/*`.

## Notes / TODO

- **Odoo version.** Written for Odoo 19 (the `@odoo/owl` + `@web/core/registry`
  client-action API). Confirm against the target build when testing.
- **Not yet run against a live Odoo.** First install is the validation; watch the
  server log on install and the panel on first open.
