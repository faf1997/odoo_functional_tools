from odoo import models, fields, api




class Estimate(models.Model):
    _name = 'estimate'
    _description = 'Estimate'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name',
        copy=False,
        default='New'
    )

    date = fields.Date(string='Date')

    user_id = fields.Many2one(
        'res.users',
        string='Responsible',
        default=lambda self: self.env.user  # opcional: usuario actual por defecto
    )

    estimate_line_ids = fields.One2many(
        'estimate.lines',
        'estimate_id',
        copy=True,
        string='Estimate Lines'
    )

    pdf_title = fields.Char(
        string='Pdf title',
        copy=True,
        default='Estimate'
    )

    company_name = fields.Char(
        string='Company name',
        copy=True,
        default=lambda self: self.env.company.name
    )

    note = fields.Html(
        string='Note',
        copy=True
    )

    logo = fields.Image(
        string="Logo",
        help="Logo for the PDF report."
    )

    stage = fields.Selection(
        [
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('finalized', 'Finalized'),
            ('cancelled', 'Cancelled'),
        ],
        string='Stage',
        default='draft',
        readonly=True,
        copy=False
    )

    total_hours = fields.Float(
        string='Total Hours',
        compute='_compute_total_hours',
        store=True
    )

    total_price = fields.Float(
        string='Total Price',
        compute='_compute_total_price',
        store=True
    )

    is_template = fields.Boolean(
        string='Is template'
    )

    partner_id = fields.Many2one(
        'res.partner',
        string='Customer'
    )

    def _fix_encoding(self, text):
        if not text:
            return text
        try:
            return text.encode('latin-1').decode('utf-8')
        except (UnicodeDecodeError, UnicodeEncodeError):
            return text


    def get_format_hours(self):
        '''
        Función para usar en el pdf. Retorna el float en formato hora.
        '''
        self.ensure_one()
        return self.format_hours(self.total_hours)


    def format_hours(self, hours_value):
        if not hours_value:
            return "00:00"
        total_minutes = int(round(hours_value * 60))
        hours, minutes = divmod(total_minutes, 60)
        return "%02d:%02d" % (hours, minutes)


    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('estimate.sequence') or 'New'
        return super(Estimate, self).create(vals)


    @api.depends('estimate_line_ids.hours')
    def _compute_total_hours(self):
        for estimate in self:
            estimate.total_hours = sum(line.hours for line in estimate.estimate_line_ids)

    def _compute_total_price(self):
        for estimate in self:
            estimate.total_price = sum(line.price for line in estimate.estimate_line_ids)

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


    def get_format_hours(self):
        '''
        Función para usar en el pdf. Retorna el float en formato hora.
        '''
        self.ensure_one()
        estimate = self.env['estimate']
        return estimate.format_hours(self.hours)


    def _fix_encoding(self, text):
        if not text:
            return text
        try:
            return text.encode('utf-8').decode('utf-8')
        except (UnicodeDecodeError, UnicodeEncodeError):
            return text


    @api.onchange('tag_id')
    def _onchange_tag_id(self):
        if self.tag_id:
            self.hours = self.tag_id.hours




class EstimateTags(models.Model):
    _name = 'estimate.tags'
    _description = 'Estimate Tags'

    name = fields.Char(string='Name', required=True)
    hours = fields.Float(string='Hours')

