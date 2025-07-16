from odoo import models, fields, api, _
from odoo.exceptions import ValidationError



class ProductProduct(models.Model):
    _inherit = 'product.product'
    
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
            # raise ValidationError(f'{rec.product_tmpl_id.name}, {rec.product_tmpl_id.id}')
            
            product_tmpl = self.env['product.template'].search([
                    ('id', '=', rec.product_tmpl_id._origin.id)
                ], limit=1) if rec.product_tmpl_id else False
            
            if product_tmpl:
                product_tmpl.is_sellable_in_multipacks = rec.is_sellable_in_multipacks
                product_tmpl.is_purchasable_in_multipacks = rec.is_purchasable_in_multipacks