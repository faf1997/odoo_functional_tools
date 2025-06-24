from . import models 


def assign_existing_customer_codes(env):
    """
    Assigns customer_code to existing partners without one.
    """
    partners = env['res.partner'].search([('customer_code', '=', False)])
    for partner in partners:
        code = env['ir.sequence'].next_by_code('res.partner.customer.code')
        partner.sudo().write({'customer_code': code})