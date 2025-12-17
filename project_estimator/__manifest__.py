{
    'name': 'Project estimator',
    'summary': 'Nos permite estimar horas y costos como una tabla excel y exportarlo a pdf',
    'version': '17.0.1.0.2',
    'author': 'Francisco Fiorentino',
    'category': 'Project',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mail',
        'product',
        'sale_management',
    ],

    'data': [
        'security/estimate_security.xml',
        'security/ir.model.access.csv',
        'data/estimate_data.xml',
        'wizards/wizard_estimate_lines_view.xml',
        'wizards/wizard_estimate_sale_order_view.xml',
        'views/estimate_views.xml',
        'report/estimate_report.xml',
    ],
    'installable': True,
    'application': True,
}
