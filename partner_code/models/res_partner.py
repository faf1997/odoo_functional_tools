from odoo import api, fields, models, _

class ResPartner(models.Model):
    _inherit = 'res.partner'

    customer_code = fields.Char(
        string='Código de Referencia', copy=False, index=True
    )

    _sql_constraints = [
        ('customer_code_unique', 'unique(customer_code)', 'The customer code must be unique.'),
    ]

