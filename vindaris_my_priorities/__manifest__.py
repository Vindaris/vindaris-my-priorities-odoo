# Vindaris "My Priorities" — Odoo module.
# Shows a Vindaris member their goals and open tasks inside Odoo, by iframing the
# hosted https://app.vindaris.com/embed/odoo surface. The module is views +
# static assets only (no server Python), so it installs on Odoo Online via Apps
# -> Import Module, as well as on Odoo.sh and self-hosted. All auth happens in
# Vindaris: the embed page signs the user in (first-party popup) and holds a
# short-lived token. No API keys and no passwords are handled in Odoo.
{
    'name': 'Vindaris: My Priorities',
    'version': '19.0.2.0.0',
    'summary': 'See your Vindaris goals and tasks inside Odoo',
    'description': """
Vindaris: My Priorities
=======================

Adds a "My Priorities" screen to Odoo that shows the Vindaris goals you own and
the tasks assigned to you, rendered from your Vindaris workspace.

How it connects
---------------
Open My Priorities and sign in to Vindaris once in the window that opens. From
then on your goals and tasks show inside Odoo. No API keys, no passwords, and no
server code: the module is views and static assets only, so it imports on Odoo
Online as well as Odoo.sh and self-hosted.

The screen is read-only.
""",
    'category': 'Productivity',
    'author': 'Vindaris',
    'website': 'https://vindaris.com',
    'license': 'LGPL-3',
    # First image is the Apps store cover/thumbnail.
    'images': ['static/description/banner.png'],
    'depends': ['web'],
    'data': [
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
