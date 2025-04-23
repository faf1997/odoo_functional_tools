# fields_module/models/ir_model_fields.py

from odoo import models, fields, api, _

class IrModelFields(models.Model):
    _inherit = 'ir.model.fields'

    # Ya existente: el Many2one para abrir el módulo
    module_name = fields.Many2one(
        'ir.module.module',
        string='Module',
        compute='_compute_module_info',
        store=False,
    )
    # Nuevo: guarda el nombre técnico (el campo `name` de ir.module.module)
    module_name_technical = fields.Char(
        string='Technical Name',
        compute='_compute_module_info',
        store=False,
    )

    def _compute_module_info(self):
        IrModelData = self.env['ir.model.data']
        IrModule    = self.env['ir.module.module']
        for rec in self:
            xml = IrModelData.search([
                ('model', '=', 'ir.model.fields'),
                ('res_id', '=', rec.id),
            ], limit=1)
            if xml and xml.module:
                # link al registro ir.module.module
                module = IrModule.search([('name', '=', xml.module)], limit=1)
                rec.module_name = module
                # muestra solamente el valor técnico
                rec.module_name_technical = xml.module
            else:
                rec.module_name = False
                rec.module_name_technical = False

    def action_open_module(self):
        """Devuelve la ventana formulario del módulo asociado."""
        self.ensure_one()
        if not self.module_name:
            return {'type': 'ir.actions.act_window_close'}
        return {
            'type': 'ir.actions.act_window',
            'name': _('Module'),
            'res_model': 'ir.module.module',
            'view_mode': 'form',
            'res_id': self.module_name.id,
            'target': 'current',
        }