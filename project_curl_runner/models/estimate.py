from odoo import models, fields, api

class Estimate(models.Model):
    _name = 'estimate'
    _description = 'Estimate'

    name = fields.Char(string='Name', required=True, copy=False, default='New')
    estimate_line_ids = fields.One2many('estimate.lines', 'estimate_id', string='Estimate Lines')
    logo = fields.Many2one('ir.attachment', string='Logo', help="Logo for the PDF report.")
    stage = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('finalized', 'Finalized'),
        ('cancelled', 'Cancelled'),
    ], string='Stage', default='draft', readonly=True, copy=False)
    total_hours = fields.Float(string='Total Hours', compute='_compute_total_hours', store=True)

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('estimate.sequence') or 'New'
        return super(Estimate, self).create(vals)

    @api.depends('estimate_line_ids.hours')
    def _compute_total_hours(self):
        for estimate in self:
            estimate.total_hours = sum(line.hours for line in estimate.estimate_line_ids)

    def action_confirm(self):
        self.write({'stage': 'confirmed'})

    def action_finalize(self):
        self.write({'stage': 'finalized'})

    def action_cancel(self):
        self.write({'stage': 'cancelled'})

    def action_reset_to_draft(self):
        self.write({'stage': 'draft'})

    def get_paged_lines(self):
        lines = self.estimate_line_ids
        lines_per_page = 50
        return [lines[i:i + lines_per_page] for i in range(0, len(lines), lines_per_page)]

class EstimateLines(models.Model):
    _name = 'estimate.lines'
    _description = 'Estimate Lines'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    tag_id = fields.Many2one('estimate.tags', string='Tag')
    estimate_id = fields.Many2one('estimate', string='Estimate')
    hours = fields.Float(string='Hours')

    @api.onchange('tag_id')
    def _onchange_tag_id(self):
        if self.tag_id:
            self.name = self.tag_id.name
            self.hours = self.tag_id.hours

class EstimateTags(models.Model):
    _name = 'estimate.tags'
    _description = 'Estimate Tags'

    name = fields.Char(string='Name', required=True)
    hours = fields.Float(string='Hours')
