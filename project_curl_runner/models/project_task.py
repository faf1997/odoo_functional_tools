from odoo import fields, models


# See _map_tasks_default_valeus




class ProjectTask(models.Model):
    _inherit = "project.task"

    curl_ids = fields.Many2many(
        "curl.task",
        "project_task_curl_rel",
        "task_id",
        "curl_id",
        string="Curls"
    )


    def action_view_task_curls(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Curl Tasks",
            "res_model": "curl.task",
            "view_mode": "tree,form",
            "domain": [("project_task_ids", "in", self.curl_ids.ids)],
            "context": {"default_project_task_ids": [(6, 0, [self.id])]},
        }
