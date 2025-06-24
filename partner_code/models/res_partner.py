from odoo import api, fields, models, _
from odoo.exceptions import UserError

class ResPartner(models.Model):
_inherit = 'res.partner'

    customer_code = fields.Char(
        string='Customer Code', copy=False, readonly=True, index=True
    )

    _sql_constraints = [
        ('customer_code_unique', 'unique(customer_code)', 'The customer code must be unique.'),
    ]

    @api.model
    def create(self, vals):
        if not vals.get('customer_code'):
            vals['customer_code'] = self.env['ir.sequence'].next_by_code('res.partner.customer.code')
        return super().create(vals)

    def write(self, vals):
        if 'customer_code' in vals:
            for partner in self.filtered(lambda p: p.customer_code and vals.get('customer_code') and p.customer_code != vals.get('customer_code')):
                raise UserError(_('You cannot modify an existing customer code.'))
            # remove any accidental change
            vals.pop('customer_code', None)
        return super().write(vals)

