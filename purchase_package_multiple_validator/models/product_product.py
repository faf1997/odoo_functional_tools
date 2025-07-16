from odoo import models, fields, api, _
from odoo.exceptions import ValidationError



class ProductProduct(models.Model):
    _inherit = 'product.product'
    
    is_sellable_in_multipacks = fields.Boolean(
        string='Embalaje de ventas',
        help='Solo permite avanzar con la cotización de venta del producto si es múltiplo de alguno de los embalajes cargados.'
    )
    
    is_purchasable_in_multipacks = fields.Boolean(
        string='Embalaje de compras',
        help='Solo permite avanzar con la cotización de compra del producto si es múltiplo de alguno de los embalajes cargados.'
    )
