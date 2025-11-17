from odoo import models, fields, api
from odoo.exceptions import ValidationError


class WindowDeployProject(models.TransientModel):
    _name = "window.deploy.project"
    _description = "Window Deploy Project"

    project_id = fields.Many2one(
        "project.project",
        string="Project",
        readonly=True
    )

    config_parameter_ids = fields.Many2many(
        "ir.config_parameter",
        "project_config_parameter_wizard_rel",
        "wizard_id",
        "config_parameter_id",
        string="Parámetros",
        domain=[("key", "ilike", "project_param_%")]
    )

    initial_param_ids = fields.Char()


    @api.model
    def create(self, vals):
        record = super().create(vals)
        record.initial_param_ids = ",".join(str(x) for x in record.config_parameter_ids.ids)
        return record


    def _save_in_project(self):
        # self.ensure_one()
        prefix = 'project_param_'
        for rec in self:
            # for param in rec.config_parameter_ids:
            #     if param.key and not param.key.startswith(prefix):
            #         param.sudo().write({'key': f'{param.key}{prefix}'})

            rec.project_id.sudo().write({
                'config_parameter_ids': [(6, 0, rec.config_parameter_ids.ids)]
            })
        return True

    def action_launch(self):
        self.ensure_one()
        self._save_in_project()
        if self.project_id and self.project_id.task_ids:
            curl_ids = self.project_id.mapped('task_ids').mapped('curl_ids')
            for rec in curl_ids:
                rec.prepare_ir_actions_server_record()

            curl_ids.mapped('action_server_id').run()
        return {"type": "ir.actions.act_window_close"}







    def action_cancel(self):
        for wizard in self:
            initial_ids = set()
            if wizard.initial_param_ids:
                initial_ids = {int(x) for x in wizard.initial_param_ids.split(",") if x}
            current_ids = set(wizard.config_parameter_ids.ids)
            new_ids = current_ids - initial_ids
            if new_ids:
                self.env["ir.config_parameter"].sudo().browse(list(new_ids)).unlink()
        return {"type": "ir.actions.act_window_close"}
