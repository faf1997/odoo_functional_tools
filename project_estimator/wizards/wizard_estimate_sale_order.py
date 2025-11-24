from odoo import models, fields, api

class WizardEstimateSaleOrder(models.TransientModel):
    _name = 'wizard.estimate.sale.order'
    _description = 'Wizard Estimate Sale Order'

    pricelist_id = fields.Many2one('product.pricelist', string='Pricelist', required=True)

    partner_id = fields.Many2one(
        'res.partner',
        string='Customer'
    )

    def create_sale_order(self):
        self.ensure_one()
        active_id = self.env.context.get('active_id')
        estimate = self.env['estimate'].browse(active_id)

        for line in estimate.estimate_line_ids:
            if not line.tag_id.product_id:
                raise models.ValidationError("Todas las etiquetas en las líneas de la estimación deben tener un producto asociado.")

        order_lines = []
        for line in estimate.estimate_line_ids:
            product = line.tag_id.product_id
            order_lines.append((0, 0, {
                'product_id': product.id,
                'name': line.name,
                'product_uom_qty': line.hours,
            }))

        sale_order = self.env['sale.order'].create({
            'partner_id': self.partner_id.id,
            'pricelist_id': self.pricelist_id.id,
            'order_line': order_lines,
        })

        estimate.write({
            'partner_id': self.partner_id.id,
        })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'res_id': sale_order.id,
            'view_mode': 'form',
            'target': 'current',
        }
