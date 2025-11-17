from odoo import models, fields, api
from odoo.exceptions import UserError



#TODO: Falta completar
#1. replicar registros de variables y archivos
#2. el wizard dinámico para validar las variables al desplegar el proyecto
#3. leer los archivos .py y .json(de n8n) para asignar variables (las variables de n8n deben ser trabajadas sobre el nodo set)
#4. relacionar el log de odoo con las tareas de ir.actions.server

class ProjectProject(models.Model):
    _inherit = "project.project"

    config_parameter_ids = fields.Many2many(
        comodel_name="ir.config_parameter",
        relation="project_config_parameter_rel",
        column1="project_id",
        column2="parameter_id",
        string="Parámetros del proyecto",
        store=True,
        domain=[("key", "ilike", "project_param_%")],
    )


    def action_deploy_project(self):
        self.ensure_one()
        ctx = dict(self.env.context or {})
        ctx.update({
            "default_project_id": self.id,
            "partner_id": self.partner_id.id,
            "default_config_parameter_ids": [(6, 0, self.config_parameter_ids.ids)],
            "project_param_prefix": "project_param_",
        })

        return {
            "type": "ir.actions.act_window",
            "name": "Lanzar proyecto",
            "res_model": "window.deploy.project",
            "view_mode": "form",
            "view_id": self.env.ref(
                "project_curl_runner.view_window_deploy_project_form"
            ).id,
            "target": "new",
            "context": ctx,
        }

