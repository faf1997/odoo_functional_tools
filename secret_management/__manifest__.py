# -*- coding: utf-8 -*-
{
    'name': 'Secret Management',
    'version': '17.0.0.0.1',
    'category': 'Project',
    'summary': 'Gestión de credenciales del cliente',
    'description': """
        Módulo para gestionar credenciales del cliente
        ===============================================
        
        Este módulo permite gestionar credenciales de clientes de tipo clave-valor,
        proporcionando un sistema seguro para almacenar información sensible
        asociada a cada partner.
        
        Características principales:
        - Almacenamiento de credenciales tipo clave-valor
        - Asociación de credenciales a partners específicos
        - Control de acceso mediante grupos de permisos
        - Posibilidad de archivar credenciales
        - Validación para evitar claves duplicadas por partner
    """,
    'author': 'Francisco Fiorentino',
    'website': '',
    'depends': ['base', 'project'],
    'data': [
        'security/secret_security.xml',
        'security/ir.model.access.csv',
        'views/secret_secret_views.xml',
        'views/menu_items.xml',
        'views/project_project_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
