{
    "name": "Launcher queue job odoo.sh",
    "author": "Francisco Fiorentino",
    "category": "tools",
    "summary":
"""Agregar el siguiente repositorio en v17.0:
https://github.com/OCA/queue
""",
    "version": "17.0.0.0.0",
    "license": "AGPL-3",
    "depends": ['queue_job'],
    "data": [
        'data/cron.xml',
    ],
    'installable': True,
    'application': False,
}