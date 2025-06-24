from . import models 
from odoo import api, SUPERUSER_ID

def assign_existing_customer_codes(cr, registry):
env = api.Environment(cr, SUPERUSER_ID, {})
partners = env['res.partner'].search([('customer_code', '=', False)])
for partner in partners:
code = env['ir.sequence'].next_by_code('res.partner.customer.code')
partner.sudo().write({'customer_code': code})