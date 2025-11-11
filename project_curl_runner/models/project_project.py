from odoo import models, fields, api
from odoo.exceptions import UserError



#TODO: Falta completar
#1. replicar registros de variables y archivos
#2. el wizard dinámico para validar las variables al desplegar el proyecto
#3. leer los archivos .py y .json(de n8n) para asignar variables (las variables de n8n deben ser trabajadas sobre el nodo set)


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


    def action_deploy_proyect(self):
        pass