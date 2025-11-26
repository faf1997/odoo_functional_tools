from odoo import models, fields, api, _
from odoo.exceptions import ValidationError




class Estimate(models.Model):
    _name = 'estimate'
    _description = _('Estimate')
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name',
        copy=False,
        default='New'
    )

    active = fields.Boolean(
        string='Active',
        default=True
    )

    date = fields.Date(
        string='Date',
        default=lambda self: fields.Date.context_today(self),
    )

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
    
    title_1 = fields.Char(
        string='Company name',
        copy=True,
        default=lambda self: self.env.company.name
    )

    title_2 = fields.Char(
        string='Pdf title',
        copy=True,
        default='Estimate'
    )

    note = fields.Html(
        string='Note',
        copy=True
    )

    logo = fields.Image(
        string="Logo",
        help="Logo for the PDF report.",
        copy=True,
        default=lambda self: self.env.company.logo
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
        string='Is template',
        copy=False,
    )

    partner_id = fields.Many2one(
        'res.partner',
        string='Customer',
        copy=False,
    )

    sale_order_ids = fields.One2many(
        comodel_name="sale.order",
        inverse_name="partner_id",
        string="Sale Orders",
        related="partner_id.sale_order_ids",
        readonly=True,
        domain="[('state' != 'cancel')]",
        copy=False,
    )

    sale_order_count = fields.Integer(
        string="Sale Orders",
        compute="_compute_sale_order_count",
        copy=False,
    )

    pdf_website_link = fields.Char(
        string="Pdf website link",
        default=lambda self: self.env['ir.config_parameter'].get_param('web.base.url', ''),
        copy=True,
    )


    tag_id = fields.Many2one('estimate.tags', string='Tag')

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        args = list(args or [])
        if name:
            args += [('title_2', 'ilike', name)]
        # return super(Estimate, self).name_search(name=name, args=args, operator=operator, limit=limit)
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)


    @api.depends("sale_order_ids")
    def _compute_sale_order_count(self):
        for rec in self:
            rec.sale_order_count = len(rec.sale_order_ids)


    def action_view_source_sale_orders(self):
        self.ensure_one()
        action = self.env.ref("sale.action_orders").read()[0]

        # Filtramos solo los pedidos relacionados a esta estimate
        action["domain"] = [("id", "in", self.sale_order_ids.ids)]

        # Creamos un contexto nuevo a partir del actual
        ctx = dict(self.env.context or {})
        ctx.update({
            "default_partner_id": self.partner_id.id if self.partner_id else False,
        })
        action["context"] = ctx  # <<-- acá reemplazamos en vez de hacer update sobre un string

        return action



    def _fix_encoding(self, text):
        if not text:
            return text
        try:
            return text.encode('latin-1').decode('utf-8')
        except (UnicodeDecodeError, UnicodeEncodeError):
            return text


    def action_open_estimate_sale_order_wizard(self):
        self.ensure_one()
        ctx = dict(self.env.context or {})
        ctx.update({
            "default_estimate_id": self.id,
            "default_partner_id": self.partner_id.id if self.partner_id else False,
        })

        return {
            "type": "ir.actions.act_window",
            "name": "Create Sale Order",
            "res_model": "wizard.estimate.sale.order",
            "view_mode": "form",
            "target": "new",
            "context": ctx,
        }


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

    percent = fields.Float(string='Percent', digits=(16, 2))

    @api.constrains('percent')
    def _check_percent(self):
        for line in self:
            if not 0 <= line.percent <= 100:
                raise models.ValidationError(_("Percentage must be between 0 and 100."))

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
    product_id = fields.Many2one('product.product', string='Product')

    @api.constrains('product_id')
    def _check_product_uom(self):
        for tag in self:
            if tag.product_id and tag.product_id.uom_id != self.env.ref('uom.product_uom_hour'):
                raise models.ValidationError(_("The product's unit of measure must be 'Hours'."))
            if tag.product_id and tag.product_id.detailed_type != 'service':
                raise models.ValidationError(_("The product must be a service."))


