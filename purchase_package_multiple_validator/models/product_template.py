from odoo import models, fields, api, _
from odoo.exceptions import ValidationError



class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_sellable_in_multipacks = fields.Boolean(
        string='Embalaje de ventas',
        help='Solo permite avanzar con la cotización de venta del producto si es múltiplo de alguno de los embalajes cargados.',
        store=True
    )
    
    is_purchasable_in_multipacks = fields.Boolean(
        string='Embalaje de compras',
        help='Solo permite avanzar con la cotización de compra del producto si es múltiplo de alguno de los embalajes cargados.',
        store=True
    )
    
    
    @api.onchange('is_sellable_in_multipacks', 'is_purchasable_in_multipacks')
    def _onchange_validation_packaging(self):
        for rec in self:
            if rec.product_variant_id:
                rec.product_variant_id.is_sellable_in_multipacks = rec.is_sellable_in_multipacks
                rec.product_variant_id.is_purchasable_in_multipacks = rec.is_purchasable_in_multipacks
                