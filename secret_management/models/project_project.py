from odoo import models, fields, api, _
from odoo.exceptions import ValidationError



class ProjectProject(models.Model):
    _inherit = 'project.project'

    secret_count = fields.Integer(
        string="Cantidad de credenciales",
        compute="_compute_secret_count"
    )

    @api.depends("partner_id")
    def _compute_secret_count(self):
        Secret = self.env["secret.secret"]
        for rec in self:
            if rec.partner_id:
                rec.secret_count = Secret.search_count([("partner_id", "=", rec.partner_id.id)])
            else:
                rec.secret_count = 0

    def action_view_partner_secrets(self):
        self.ensure_one()
        action = self.env.ref("secret_management.action_secret_secret").read()[0]
        partner_id = self.partner_id.id if self.partner_id else False
        action["domain"] = [("partner_id", "=", partner_id)] if partner_id else [("id", "=", 0)]
        action["context"] = {
            "default_partner_id": partner_id
        }
        return action