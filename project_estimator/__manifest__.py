{
    'name': 'Project estimator',
    'summary': 'Nos permite estimar horas y costos como una tabla excel y exportarlo a pdf',
    'version': '17.0.1.0.0',
    'author': 'Francisco Fiorentino',
    'category': 'Project',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'mail',
    ],

    'data': [
        'security/ir.model.access.csv',
        'data/estimate_data.xml',
        'views/estimate_views.xml',
        'report/estimate_report.xml',
    ],
    'installable': True,
    'application': True,
}
