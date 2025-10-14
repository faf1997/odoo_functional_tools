from datetime import timedelta, datetime, time
from odoo import models, fields, api
from typing import List, Dict
import pytz
import requests
import logging

_logger = logging.getLogger(__name__)


class ResourceCalendarLeaves(models.Model):
    _inherit = 'resource.calendar.leaves'

    country_id =fields.Many2one(
        'res.country',
        string='País',
        default=lambda self: self.env.company.country_id.id,
    )

    is_cron_holiday = fields.Boolean(
        string='Es feriado cron',
        default=False,
    )

    def get_holidays(self, year: int)-> List[Dict]:
        """
        Obtiene la lista de feriados de Argentina para el año especificado.
        Retorna una lista de diccionarios con keys: "fecha", "tipo", "nombre".
        Usa la API de ArgentinaDatos / Feriados.
        """
        url = f"https://api.argentinadatos.com/v1/feriados/{year}"
        resp = requests.get(url)
        # resp.raise_for_status()
        if resp.status_code == 200:

        # Se espera que la respuesta sea JSON con estructura:
        # [ { "fecha": "YYYY-MM-DD", "tipo": "...", "nombre": "..." }, ... ]
            feriados = resp.json()
            # feriados.
            return feriados

        else:
            _logger.error(f"Error al obtener los feriados Argentinos: {resp.status_code}")
        return {}


    def _utc_day_bounds_from_local(self, date_str):
        d = fields.Date.from_string(date_str)
        tzname = self.env.user.tz or self.env.context.get('tz') or 'America/Argentina/Buenos_Aires'
        tz = pytz.timezone(tzname)
        dt_from_local = tz.localize(datetime.combine(d, time(0, 0, 0)))
        dt_to_local = dt_from_local + timedelta(days=1)
        dt_from_utc = dt_from_local.astimezone(pytz.UTC)
        dt_to_utc = dt_to_local.astimezone(pytz.UTC)
        return (fields.Datetime.to_string(dt_from_utc), fields.Datetime.to_string(dt_to_utc))


    def create_holidays(self, ):
        argentina = self.env.ref("base.ar")
        if argentina and self.env.company.country_id.id == argentina.id:
            holidays = self.get_holidays(fields.Date.context_today(self).year)
            vals_list = []
            self.search([('country_id', '=', argentina.id), ('is_cron_holiday', '=', True)]).unlink()
            for holiday in holidays:
                date_from, date_to = self._utc_day_bounds_from_local(holiday['fecha'])
                rec = {
                    'name': holiday['nombre'],
                    # 'date_from': holiday['fecha'] + " 00:00:00",
                    # 'date_to': holiday['fecha'] + " 23:59:59",
                    'date_from': date_from,
                    'date_to': date_to,
                    'country_id': argentina.id,
                    'time_type': 'leave',
                    'is_cron_holiday': True,
                }
                vals_list.append(rec)
                _logger.error(f"Feriado: {rec['date_from']} {rec['date_to']}") 
            RCL = self.with_context(is_cron_holiday=True)
            RCL.create(vals_list)

    @api.constrains('date_from', 'date_to', 'calendar_id')
    def _check_compare_dates(self):
        if self.env.context.get('is_cron_holiday'):
            return
        try:
            super()._check_compare_dates()
        except Exception as e:
            _logger.error(f"Error al crear los feriados: {e}")
          
            



    