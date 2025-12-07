{
    'name': 'Website WhatsApp Link Generator',
    'version': '17.0.1.0.0',
    'summary': 'Generate custom WhatsApp message links from your website',
    'category': 'Website',
    'author': 'FranDev',
    'website': 'https://frandev.com.ar',
    'depends': ['website'],
    'data': [
        'views/website_whatsapp_link_templates.xml',
    ],
    'assets': {
        'website.assets_frontend': [
            'website_whatsapp_link_generator/static/src/js/whatsapp_link.js',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}