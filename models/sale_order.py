# -*- coding: utf-8 -*-

from datetime import datetime, time
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT

 
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _get_extra_fields(self):
        fields = self.env['sale.extra.field.config'].search([('visible','=',True)])
        return fields

    def _compute_extra_values(self):
        for order in self:
            for field in self._get_extra_fields():
                # إذا الحقل من نوع char
                if field.field_type == 'char':
                    order[field.name] = ''
                elif field.field_type == 'float':
                    order[field.name] = 0.0
                elif field.field_type == 'boolean':
                    order[field.name] = False


    @api.model
    def default_get(self, fields_list):
        res = super(SaleOrder, self).default_get(fields_list)
        self._compute_extra_values()
        return res

    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        extra_fields = self.env['sale.extra.field.config'].search([('visible', '=', True)])
        for field in extra_fields:
            invoice_vals[field.name] = self[field.name]
        return invoice_vals