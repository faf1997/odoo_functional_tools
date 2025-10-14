{
    "name": "Feriados Argentinos automáticos",
    "author": "Francisco Fiorentino",
    "category": "tools",
    "summary":
"""Feriados argentinos automáticos
""",
    "version": "17.0.2.1.0",
    "license": "AGPL-3",
    "depends": ['hr_holidays'],
    "data": [
        'data/cron.xml',
        'views/resource_calendar_leaves_views.xml',
    ],
    "post_init_hook": "post_init_hook",
    'installable': True,
    'application': False,
}