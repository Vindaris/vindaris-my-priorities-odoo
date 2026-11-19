# Vindaris "My Priorities" — Odoo module.
# Shows a Vindaris member their goals and open tasks inside Odoo, by iframing
# the hosted https://app.vindaris.com/embed/priorities surface. The module
# holds only its own per-instance credentials (registered once at connect);
# every viewer is authenticated by a one-time account link done from a
# logged-in Vindaris session, so no API keys are pasted and no password is
# handled here.
{
    'name': 'Vindaris: My Priorities',
    'version': '19.0.1.0.0',
    'summary': 'See your Vindaris goals and tasks inside Odoo',
    'description': """
Vindaris: My Priorities
=======================

Adds a "My Priorities" screen to Odoo that shows the Vindaris goals you own and
the tasks assigned to you, rendered from your Vindaris workspace.

How it connects
---------------
* An administrator connects Odoo to Vindaris once (Settings -> Vindaris ->
  Connect). The module registers with Vindaris and stores its own connection
  credentials; nothing is copied by hand.
* Each user links their Odoo account to their Vindaris account once, from a
  logged-in Vindaris page. No API keys, no shared passwords.

The screen is read-only.
""",
    'category': 'Productivity',
    'author': 'Vindaris',
    'website': 'https://vindaris.com',
    'license': 'LGPL-3',
    'depends': ['base_setup', 'web'],
    'data': [
        'views/res_config_settings_views.xml',
        'views/vindaris_menu.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'vindaris_my_priorities/static/src/js/priorities_action.js',
            'vindaris_my_priorities/static/src/xml/priorities_action.xml',
        ],
    },
    'installable': True,
    'application': True,
}
