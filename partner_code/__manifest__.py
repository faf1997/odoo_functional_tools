{
    'name': 'Partner Customer Code',
    'version': '18.0.1.0.1',
    'summary': 'Unique internal reference code for contacts',
    'description': 'Unique internal reference code for contacts.',
    'category': 'Contacts',
    'author': 'Your Company',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'views/partner_views.xml',
    ],
    'post_init_hook': 'assign_existing_customer_codes',
    'installable': True,
    'application': False,
}