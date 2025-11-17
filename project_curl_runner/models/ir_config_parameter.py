from odoo import models, api





class IrConfigParameter(models.Model):
    _inherit = 'ir.config_parameter'
    


    @api.model_create_multi
    def create(self, vals_list):
        prefix = self.env.context.get("project_param_prefix") or self.env.context.get("task_param_prefix")
        if prefix:
            for vals in vals_list:
                key = vals.get("key")
                if key and not key.startswith(prefix):
                    vals["key"] = f"{prefix}{key}"
        return super(IrConfigParameter, self).create(vals_list)


    def write(self, vals):
        prefix = self.env.context.get("project_param_prefix") or self.env.context.get("task_param_prefix")
        if prefix:
            key = vals.get("key")
            if key and not key.startswith(prefix):
                vals = dict(vals)  # copiar para no tocar el dict original
                vals["key"] = f"{prefix}{key}"
        return super(IrConfigParameter, self).write(vals)
