# -*- coding: utf-8 -*-

from datetime import datetime, time
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT

class AccountMove(models.Model):
    _inherit = 'account.move'

    def _get_extra_fields(self):
        return self.env['sale.extra.field.config'].search([('visible', '=', True)])

    def _compute_extra_values(self):
        for move in self:
            for field in self._get_extra_fields():
                if field.field_type == 'char':
                    move[field.name] = ''
                elif field.field_type == 'float':
                    move[field.name] = 0.0
                elif field.field_type == 'boolean':
                    move[field.name] = False
                elif field.field_type == 'date':
                    move[field.name] = fields.Date.today()


    @api.model
    def default_get(self, fields_list):
        res = super(AccountMove, self).default_get(fields_list)
        self._compute_extra_values()  # تهيئة القيم الافتراضية قبل العرض
        return res
