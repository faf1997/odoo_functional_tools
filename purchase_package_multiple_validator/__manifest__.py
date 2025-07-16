{
    'name': 'validador de multipolos en embalados/paquetes para compras y ventas',
    'version': '18.0.1.1.1',
    'summary': 'Validación productos en embalados/paquetes para compras y ventas.',
    'description': 'Este módulo valida que los productos en un embalado/paquete para compras y ventas sean multiplos.',
    'category': 'Purchases',
    'author': 'Fiorentino Francisco',
    'license': 'LGPL-3',
    'depends': ['base', 'purchase', 'sale_management'],
    'data':[
      'views/view_product_template.xml',
      'views/view_product_product.xml'
    ],
    'installable': True,
    'application': False,
}