# Vindaris: My Priorities (Odoo module)

Adds a **My Priorities** screen to Odoo that iframes the hosted Vindaris embed
surface (`https://app.vindaris.com/embed/priorities`), mirroring the Jira Forge
panel and the Microsoft Teams tab. No API keys are pasted and no password is
handled inside Odoo.

## How it works

1. **Admin connects once.** Settings → Vindaris → Connect. The module POSTs to
   `POST /api/embed/odoo/register` and stores the returned `instanceId` +
   `secret` as system parameters (`vindaris.instance_id`,
   `vindaris.instance_secret`). The secret is never shown in the UI.
2. **Each user links once.** Opening My Priorities, the OWL client action calls
   the Odoo controller `/vindaris/priorities/url`, which calls
   `POST /api/embed/odoo/session` server-to-server (so the secret never reaches
   the browser), passing the authenticated Odoo user id. If that Odoo account
   is not yet linked, Vindaris returns a one-time link URL; the user opens it,
   signs into Vindaris, and confirms. From then on the same call returns a
   short-lived embed URL that the module iframes.

The Odoo user id comes from the authenticated session (`request.env.uid`), so a
user can only ever request their own priorities.

## Trust model

The module runs inside the customer's own Odoo, where its source is readable, so
there is **no single baked-in secret**. Each instance registers for its own
secret, stored on the Vindaris side only as a bcrypt hash. A link is keyed by
`<instanceId>:<odooUid>`, so one instance's credentials can never present a
token for an account linked from another instance. Access always requires the
one-time, member-confirmed account link.

## Vindaris-side requirements

- Env: `EMBED_TOKEN_SECRET` (already set in prod; used to sign embed/link
  tokens). No new env var is introduced by Odoo.
- Migration: `manual_add_odoo_embed_instances` (the `odoo_embed_instances`
  table). Applies automatically on deploy via `scripts/migrate.js`.
- CSP: `src/proxy.ts` allows `https://*.odoo.com` to frame `/embed/*`.

## Where it works

The screen renders by iframing `app.vindaris.com/embed/priorities`, and a
browser only loads that iframe if the Vindaris CSP lists the Odoo host as an
allowed frame ancestor. The current allowlist is `https://*.odoo.com`.

| Odoo deployment | Host | My Priorities screen |
| --- | --- | --- |
| **Odoo Online** (SaaS) | `yourco.odoo.com` | ✅ Works |
| **Odoo.sh** on the default domain | `yourco.odoo.com` | ✅ Works |
| **Odoo.sh / self-hosted on a custom domain** | `odoo.yourco.com` | ❌ Blocked by CSP |
| **Self-hosted** on any non-`*.odoo.com` host | e.g. `localhost`, `erp.acme.de` | ❌ Blocked by CSP |

The connect and account-link flows work on every deployment; only the embedded
screen is gated, because the iframe's parent origin must be on the allowlist.
Supporting a custom domain later means either adding a per-instance dynamic
`frame-ancestors` header on Vindaris, or a native (fetch-JSON-and-render)
fallback like the Jira Forge panel.

## Known limitations / TODO before publishing

- **Odoo version.** Written for Odoo 19 (`type="json"` controller, the
  `@web/core/network/rpc` import, the `<app>/<setting>` settings layout, and
  Odoo 17+ `invisible="..."` attribute syntax). Confirm against the target
  Odoo build when testing.
- **Not yet run against a live Odoo.** The module is scaffolded to match Odoo's
  conventions but has not been installed on a running Odoo. First install is the
  validation: watch the Odoo server log on install and on first open. Note a
  custom module cannot be installed on Odoo Online directly; test on a local
  Odoo or Odoo.sh (see `localtest/README.md`).

## Publishing

To install on Odoo Online it must be published on apps.odoo.com and pass Odoo's
review. On Odoo.sh and self-hosted it installs directly.
