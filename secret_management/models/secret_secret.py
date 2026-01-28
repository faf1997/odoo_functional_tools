# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SecretSecret(models.Model):
    _name = 'secret.secret'
    _description = 'Client Credentials'
    _order = 'partner_id, key'

    name = fields.Char(
        string='Name',
        compute='_compute_name',
        store=True
    )
    partner_id = fields.Many2one(
        'res.partner',
        string='Partner',
        required=True,
        ondelete='cascade',
        index=True
    )
    key = fields.Char(
        string='Key',
        required=True,
        index=True
    )
    value = fields.Char(
        string='Value',
        required=True
    )
    active = fields.Boolean(
        string='Active',
        default=True
    )

    @api.depends('partner_id', 'key')
    def _compute_name(self):
        """Compute name field based on partner and key"""
        for record in self:
            if record.partner_id and record.key:
                record.name = f"{record.partner_id.name} - {record.key}"
            else:
                record.name = "New Secret"

    @api.constrains('partner_id', 'key', 'active')
    def _check_unique_key_per_partner(self):
        """Validate that key is unique per partner for active records"""
        for record in self:
            if record.active and record.partner_id and record.key:
                domain = [
                    ('partner_id', '=', record.partner_id.id),
                    ('key', '=', record.key),
                    ('active', '=', True),
                    ('id', '!=', record.id)
                ]
                existing = self.search(domain, limit=1)
                if existing:
                    raise ValidationError(
                        f"Ya existe una credencial activa con la clave '{record.key}' "
                        f"para el partner '{record.partner_id.name}'."
                    )

    _sql_constraints = [
        (
            'partner_key_active_unique',
            'UNIQUE(partner_id, key, active)',
            'La clave debe ser única por partner para credenciales activas!'
        )
    ]
