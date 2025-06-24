from odoo import api, fields, models, _
from odoo.exceptions import UserError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    customer_code = fields.Char(
        string='Código de cliente', copy=False, index=True
    )

    _sql_constraints = [
        ('customer_code_unique', 'unique(customer_code)', 'The customer code must be unique.'),
    ]

