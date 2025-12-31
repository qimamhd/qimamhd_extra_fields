# -*- coding: utf-8 -*-

from datetime import datetime, time
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT

 
class AccountMove(models.Model):
    _inherit = 'account.move'

    x_extra_text_1 = fields.Char()
    x_extra_text_2 = fields.Char()
    x_extra_number_1 = fields.Float()
    x_extra_date_1 = fields.Date()

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super().fields_view_get(view_id, view_type, toolbar, submenu)

        if view_type == 'form':
            settings = self.env['extra.field.setting'].search([])
            for s in settings:
                if s.field_name in res['fields']:
                    res['fields'][s.field_name]['string'] = (
                        s.label or res['fields'][s.field_name]['string']
                    )
                    res['fields'][s.field_name]['required'] = s.required
                    res['fields'][s.field_name]['invisible'] = not s.visible

        return res
