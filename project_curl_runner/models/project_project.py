from odoo import models, fields, api
from odoo.exceptions import UserError
import hashlib
import re



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


    def get_now_argentina(self):
        now_ar = fields.Datetime.context_timestamp(
            self,
            fields.Datetime.now()
        )
        # acá now_ar ya está en la tz del contexto (ej: America/Argentina/Buenos_Aires)
        return now_ar


    def make_hash(self, value: str) -> str:
        return hashlib.sha256(value.encode("utf-8")).hexdigest()


    def remove_from_hash(self, text: str) -> str:
        return re.sub(r'_hash:.*', '', text, flags=re.DOTALL)


    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {})

        # Campos que quiero copiar tal cual
        # copied_curl_ids = [rec.copy().id for rec in self.curl_ids]
        hash_ = self.make_hash(f'{self.name}{self.get_now_argentina()}')
        config_parameter_ids = [rec.copy({'key': f'{self.remove_from_hash(rec.key)}_hash:{hash_}'}).id for rec in self.config_parameter_ids]
        
        default.update({
            "description": self.description,
            "config_parameter_ids": [(6, 0, config_parameter_ids)],
        })
        
        return super(ProjectProject, self).copy(default)


    def action_deploy_project(self):
        self.ensure_one()
        ctx = dict(self.env.context or {})
        ctx.update({
            "default_project_id": self.id,
            "default_partner_id": self.partner_id.id,
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

