from odoo import models, fields, api, _
from odoo.tools.safe_eval import wrap_module
import requests as _requests
import odoo
import logging

_logger = logging.getLogger(__name__)


class IrActionsServer(models.Model):
    _inherit = 'ir.actions.server'

    def _get_eval_context(self, action=None):
        ctx = super(IrActionsServer, self)._get_eval_context(action)
        # Exponer SOLO atributos permitidos del módulo:
        ctx["requests"] = wrap_module(_requests, {"request", "get", "post", "put", "patch", "delete"})
        return ctx
