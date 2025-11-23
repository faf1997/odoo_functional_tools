from odoo import models, fields, api

class WizardEstimateLines(models.TransientModel):
    _name = 'wizard.estimate.lines'
    _description = 'Wizard Estimate Lines'

    total_hours = fields.Float(string='Total Hours', required=True)
    estimate_line_ids = fields.Many2many('estimate.lines', string='Estimate Lines')

    @api.model
    def default_get(self, fields):
        res = super(WizardEstimateLines, self).default_get(fields)
        active_id = self.env.context.get('active_id')
        if active_id:
            estimate = self.env['estimate'].browse(active_id)
            res['estimate_line_ids'] = [(6, 0, estimate.estimate_line_ids.ids)]
        return res

    def assign_hours(self):
        self.ensure_one()
        total_percent = sum(self.estimate_line_ids.mapped('percent'))
        if total_percent != 100:
            raise models.ValidationError("Error: to assign time percentages, the total must be 100% to assign the hours in the lines.")

        for line in self.estimate_line_ids:
            line.hours = (self.total_hours * line.percent) / 100

        return {'type': 'ir.actions.act_window_close'}
