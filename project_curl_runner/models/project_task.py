from odoo import fields, models


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
        domain=[("name", "ilike", "curl_task_%")]
    )


    # def action_view_task_curls(self):
    #     self.ensure_one()
    #     return {
    #         "type": "ir.actions.act_window",
    #         "name": "Curl Tasks",
    #         "res_model": "curl.task",
    #         "view_mode": "tree,form",
    #         # "domain": [("project_task_ids", "in", self.curl_ids.ids)],
    #         "context": {"default_project_task_ids": [(4, self.id)]},
    #     }


    def action_view_task_curls(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Curl Tasks",
            "res_model": "curl.task",
            "view_mode": "tree,form",
            # Opción A: filtrar por la relación ya existente
            "domain": [("id", "in", self.curl_ids.ids)],
            # Opción B (si definís el espejo abajo):
            # "domain": [("project_task_ids", "in", self.id)],
            "context": {
                # Setea por defecto la tarea actual en el M2M del otro modelo
                "default_project_task_ids": [(6, 0, [self.id])],
            },
            "target": "current",
        }