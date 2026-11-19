# Vindaris Odoo apps

Odoo apps published by [Vindaris](https://vindaris.com), strategy-execution
software. Each app is a folder at the root of this repository, on the branch
that matches its Odoo series (for example `19.0`).

## Apps

### `vindaris_my_priorities` — My Priorities

Shows a user's Vindaris goals and assigned tasks inside Odoo, by embedding the
hosted Vindaris surface. An administrator connects Odoo to Vindaris once; each
user links their account once from a signed-in Vindaris page. No API keys are
pasted and no passwords are handled in Odoo. See
[`vindaris_my_priorities/README.md`](vindaris_my_priorities/README.md) for setup
and the supported Odoo deployments.

## Branches

Branches are named by Odoo series, matching the Odoo Apps requirement that the
branch name equals the series the modules target.

| Branch | Odoo series |
| --- | --- |
| `19.0` | Odoo 19 |

## License

LGPL-3. See [LICENSE](LICENSE).
