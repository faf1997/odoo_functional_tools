from odoo import fields, models, api


# See _map_tasks_default_valeus




class ProjectTask(models.Model):
    _inherit = "project.task"

    curl_ids = fields.Many2many(
        "curl.task",
        "project_task_curl_rel",
        "task_id",
        "curl_id",
        string="Curls",
        store=True,
        domain=[("name", "ilike", "curl_task_%")],
    )


    def action_view_task_curls(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Tareas automatizadas",
            "res_model": "curl.task",
            "view_mode": "tree,form",
            # "domain": [("id", "in", self.curl_ids.ids)],
            "domain": [("project_task_ids", "in", self.ids)],
            "context": {
                "default_project_task_ids": [(6, 0, [self.id])],
                "task_param_prefix": "task_param_",
            },
            "target": "current",
        }
            # "context": {
            #     "default_project_task_ids": [(6, 0, self.ids)],
            #     "task_param_prefix": "task_param_",
            # },
            # "target": "current",        


    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {})

        # Campos que quiero copiar tal cual
        # copied_curl_ids = [rec.copy().id for rec in self.curl_ids]
        curl_ids = [rec.copy().id for rec in self.curl_ids]
        default.update({
            "name": self.name,
            "description": self.description,
            "curl_ids": [(6, 0, curl_ids)],
        })

        return super(ProjectTask, self).copy(default)