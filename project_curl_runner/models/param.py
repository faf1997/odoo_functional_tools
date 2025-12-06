from tokenize import String
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.fields import Command


#Este modelo es para evitar dar acceso a configuraciones del sistema en 
# odoo y poder replicar variables con el mismo nombre sin necesitar
# cambiar los nombres de las variables por proyecto clonado.

#TODO: terminar de armar la lógica de este modelo, para que se pueda usar en el proyecto y en las tareas.

class ProjectParam(models.Model):
    _name = 'project.param'


    key = fields.Char(
        string='Key',
        required=True,
        copy=True,
    )

    Value_str = fields.Char(
        string='Value',
        required=True,
        copy=True,
    )

    value_int = fields.Integer(
        string='Value',
        required=True,
        copy=True,
    )

    value_float = fields.Float(
        string='Value',
        required=True,
        copy=True
    )

    value_type = fields.Selection(
        string='Type',
        selection=[
            ('int', 'Integer'),
            ('float', 'Float'),
            ('str', 'String'),
        ],
        required=True,
        copy=True,
    )

    model = fields.Selection(
        string='Model',
        selection=[
            ('p', 'Project'),
            ('t', 'Task'),
        ],
        required=True,
        copy=True,
    )

    record_id = fields.Integer(#dejamos un integer, porque debe relacionarse a dos modelos diferentes
        string='Record id',
        copy=False#esto se debe ajustar en el método copy o create, debe asignarse el id del nuevo registro
    )


    @api.constrains('value_str', 'value_int', 'value_float')
    def _constrains_value_type(self):
        for rec in self:
            if not rec.value_type:
                raise ValidationError(_('A data type must be selected'))


    def get_param(self, key):
        pass


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
