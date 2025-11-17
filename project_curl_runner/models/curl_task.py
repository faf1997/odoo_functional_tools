from odoo import api, fields, models
from odoo.exceptions import UserError
from datetime import datetime
import requests
import json
import io
import tokenize
import token as tokenmod
import uncurl
import re
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta
from odoo.tools.safe_eval import safe_eval



class CurlTask(models.Model):
    _name = "curl.task"
    _description = "Curl Task"
    _order = "sequence, id"

    sequence = fields.Integer()

    name = fields.Char(
        required=True,
        default=lambda self: self._default_name()
    )

    command = fields.Text(
        default=lambda self: self._default_command(),
        required=True,
        help='Este campo define el comando curl a ejecutar. Se debe ingresar el comando completo, incluyendo los parámetros y opciones.'
    )

    code = fields.Text(
        required=True,
        default=lambda self: self._default_code(),
        help='Este campo define el código python a ejecutar. luego de obtener la respuesta, del comando curl. Variable del curl: resp.'
    )

    status_code = fields.Integer(
        string='Status Code',
        default=200,
        required=True,
        help='Este campo define cual el código de respuesta esperado de la petición curl. Si el código no es el esperado, la tarea se marcará como fallida.'
    )

    status = fields.Selection(
        string='Status',
        selection=[('success', 'Success'), ('failed', 'Failed')],
        default='success',
        required=True,
        help='Este campo define el estado de la tarea. Si la tarea es exitosa, el campo se marcará como success. Si la tarea es fallida, el campo se marcará como failed.'
    )

    action_server_id = fields.Many2one(
        "ir.actions.server",
        string="Server Action",
        ondelete="set null",
        store=True,
        domain=[("name", "ilike", "curl_%")]
    )

    project_task_ids = fields.Many2many(
        "project.task",
        "project_task_curl_rel",
        "curl_id",
        "task_id",
        store=True,
        string="Project Tasks"
    )

    model_id = fields.Many2one(
        "ir.model",
        string="Model",
        ondelete="set null",
        help="Modelo de Odoo sobre el cual se evaluarán expresiones",
        default=lambda self: self.env['ir.model']._get_id(self._name)
    )

    config_parameter_ids = fields.Many2many(
        comodel_name="ir.config_parameter",
        relation="curl_task_config_parameter_rel",
        column1="curl_task_id",
        column2="param_id",
        string="Config Parameters",
        help="Parámetros del sistema que esta tarea puede consultar.",
        store=True,
        domain=[("key", "ilike", "task_param_%")]
    )


    def action_curl_to_request(self):
        self.ensure_one()
        request = self.get_request()
        if request:
            self.write({
                'code': f'{self.code}\n{request}'
            })


    def get_request(self):
        self.ensure_one()
        clear_comments_and_doc_strings = self.strip_python_comments(
            self.command,
            True
        ).strip()
        render_curl = ''
        if 'curl' in clear_comments_and_doc_strings:
            render_curl = "resp = " + uncurl.parse(clear_comments_and_doc_strings)
            # render_curl = "resp = " + uncurl.parse(self.render_double_braces(
            #     template = clear_comments_and_doc_strings,
            #     record_model = self._name,
            #     record_id = self.id or self.id
            # ))

        return render_curl


    def prepare_ir_actions_server_record(self):#acción para crear el registro ir.action.server
        self.ensure_one()

        clear_comments_and_doc_strings_in_code = self.strip_python_comments(
            self.code,
            True
        ).strip()

        clear_comments_and_doc_strings_in_code = self.render_double_braces(
            template = clear_comments_and_doc_strings_in_code,
            record_model = self._name,
            record_id = self.id
        )

        if not self.action_server_id:
            ir_actions_server = self.env['ir.actions.server'].create({
                'name': self.name,
                'state': 'code',
                'model_id': self.model_id.id or self.model_id.id,#self.env['ir.model']._get_id(self._name),#model_id
                'code': clear_comments_and_doc_strings_in_code
            })
            self.sudo().write({
                'action_server_id': ir_actions_server.id or ir_actions_server.id
            })
            self._related_fix()
            return self.action_server_id.id or self.action_server_id.id

        self.action_server_id.sudo().write({
            'name': self.name,
            'code': clear_comments_and_doc_strings_in_code,
            'model_id': self.model_id.id or self.model_id.id
        })
        self._related_fix()
        return self.action_server_id.id or self.action_server_id.id


    def launch_action_server(self):
        self.ensure_one()
        if not self.action_server_id:
            raise UserError('No está creada la acción del servidor para ejecutar el código')

        self.action_server_id.run()
        return self.action_server_id.id or self.action_server_id.id


    def _related_fix(self):
        self.ensure_one()
        for task in self.project_task_ids:
            task.write({'curl_ids': [(4, self.id)]})


    def strip_python_comments(self, source: str, remove_docstrings: bool = True) -> str:
        out = []
        prev_type = tokenmod.INDENT
        last_lineno = 0
        last_col = 0
        for tok_type, tok_str, (sline, scol), (eline, ecol), _ in tokenize.generate_tokens(io.StringIO(source).readline):
            if sline > last_lineno:
                last_col = 0
            if scol > last_col:
                out.append(" " * (scol - last_col))
            skip = False
            if tok_type == tokenize.COMMENT:
                skip = True
            elif remove_docstrings and tok_type == tokenmod.STRING:
                if prev_type in (tokenmod.INDENT, tokenmod.NEWLINE) or scol == 0:
                    skip = True
            if not skip:
                out.append(tok_str)
            prev_type = tok_type
            last_col = ecol
            last_lineno = eline
        return "".join(out)


    @api.model
    def render_double_braces(self, template: str, record_model=None, record_id=None, extra_context=None):
        eval_ctx = {
            "env": self.env,
            "uid": self.env.uid,
            "user": self.env.user,
            "context": dict(self.env.context),
            "datetime": datetime,
            "date": date,
            "relativedelta": relativedelta,
            # "json": json,
        }

        # 1) Resolver modelo/registro por prioridad: args -> context -> self (si no es vacío)
        model_name = record_model or self.env.context.get("active_model")
        rid = record_id or self.env.context.get("active_id")

        # si no vino nada y self es un recordset concreto, usar self
        if not model_name and getattr(self, "_name", None) and len(self) == 1:
            model_name = self._name
            rid = self.id or self.id

        records = self.env[model_name].browse(rid) if (model_name and rid) else self.env[model_name] if model_name else self.env["ir.model"].browse()

        if model_name:
            eval_ctx.update({
                "model": self.env[model_name],
                "record": records[:1],
                "records": records,
            })

        if extra_context:
            eval_ctx.update(extra_context)

        def _to_text(v):
            if isinstance(v, (dict, list)):
                return json.dumps(v, ensure_ascii=False)
            return "" if v is None else str(v)

        P3 = re.compile(r"\{\{\{(.*?)\}\}\}", re.DOTALL)

        def _repl(m):
            expr = m.group(1).strip()
            try:
                val = safe_eval(expr, eval_ctx, mode="eval", nocopy=True)
            except Exception as e:
                raise UserError(f"Error al evaluar '{{{{{{{expr}}}}}}}': {e}")
            return _to_text(val)

        return P3.sub(_repl, template)


    @api.constrains('name', 'model_id', 'status_code')
    def _constrains_data(self):
        for rec in self:
            if not rec.model_id:
                raise UserError("No se asignó el modelo en el registro")
            if not rec.status_code:
                raise UserError("No se asignó el status code en el registro")
            if not rec.name:
                raise UserError("No se asignó el nombre en el registro")


    @api.model
    def _default_name(self):
        ts = fields.Datetime.context_timestamp(self, fields.Datetime.now())
        return f"curl_task_{ts.strftime('%Y%m%d_%H%M%S')}"


    @api.model
    def _default_code(self):
        return """# 1. puedes acceder a otros modelos usando env['model.name'].search([('field', '=', 'value')])
# 2. resp accede a la respuesta del curl.
# 3. ejemplo de acción en ir.actions.client:
# action = {
#     "type": "ir.actions.client",
#     "tag": "display_notification",
#     "params": {
#         "title": "Listo",
#         "message": "Hubo un error.",
#         "type": "danger",      # success | warning | danger | info
#         "sticky": True,        # True = no se cierra sola
#         # "next": {"type": "ir.actions.act_window_close"},  # opcional, acción a ejecutar luego
#     }
# }
""" + ("\n"*11)

    @api.model
    def _default_command(self):
        return """# 1. puedes acceder a otros modelos usando {{{env['model.name'].search([('field', '=', 'value')])}}}
# 2. recomendado usar env['ir.config_parameter'].def get_param(key, default=False) para acceder a parámetros de configuración.
# 3. no puedes dejar comentarios, solo usar comandos curl como si se ejecutase en bash.
# ejemplo de curl con parámetros:

# curl "{{{env['ir.config_parameter'].sudo().get_param('web.base.url', default=False)}}}"
        """ + ("\n"*6)