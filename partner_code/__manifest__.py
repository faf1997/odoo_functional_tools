{
    'name': 'Partner Customer Code',
    'version': '18.0.1.0.0',
    'summary': 'Automatic configurable sequence for customer codes',
    'description': 'Adds configurable sequence to assign unique customer codes to partners and applies it to existing records. Once set, codes cannot be modified.',
    'category': 'Contacts',
    'author': 'Your Company',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'data/partner_code_sequence_data.xml',
        'views/partner_views.xml',
    ],
    'post_init_hook': 'assign_existing_customer_codes',
    'installable': True,
    'application': False,
}