from odoo import models, fields, api
from odoo.exceptions import UserError





class ProjectProject(models.Model):
    _inherit = "project.project"

    # def copy(self, default=None):
    #     self.ensure_one()
    #     default = dict(default or {})
    #     new_project = super(ProjectProject, self).copy(default=default)
    #     mapping = {}
    #     for task in self.task_ids:
    #         vals = {'project_id': new_project.id}
    #         new_task = task.copy(vals)
    #         mapping[task.id] = new_task
    #     for old, new in mapping.items():
    #         parent = self.env['project.task'].browse(old).parent_id
    #         if parent and parent.id in mapping:
    #             new.parent_id = mapping[parent.id].id
    #     return new_project