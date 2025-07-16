from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_is_zero




class SaleOrder(models.Model):
    _inherit = 'sale.order'


    @api.constrains('order_line')
    def _validate_order_lines(self):
        self.ensure_one()
        is_packaging = self.env.user.has_group('product.group_stock_packaging')
        for rec in self.order_line:
            if is_packaging and rec.product_id.packaging_ids:
                self._validate_multiples(rec.product_id, rec.product_qty)


    def _validate_multiples(self, product_id, quantity):
        rounding = product_id.uom_id.rounding or 1.0    # seguridad

        ok = any(
            pkg.qty
            and float_is_zero(
                quantity % pkg.qty,
                precision_rounding=rounding           # ← clave correcta
            )
            for pkg in product_id.packaging_ids
        )

        if not ok:
            possibilities = "\n".join(
                f"{qty:g}" for qty in product_id.packaging_ids.mapped('qty')
            )
            raise ValidationError(_(
                "La cantidad %s para el producto %s no es múltiplo de ninguna "
                "de las cantidades de embalaje. \nElija un múltiplo de: \n%s")
                % (quantity, product_id.display_name, possibilities)
            )