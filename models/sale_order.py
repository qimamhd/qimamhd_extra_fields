# -*- coding: utf-8 -*-
from datetime import datetime, time
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    x_extra_text_1 = fields.Char()
    x_extra_text_2 = fields.Char()
    x_extra_number_1 = fields.Float()
    x_extra_date_1 = fields.Date()
    extra_visible_map = fields.Serialized(
        compute='_compute_extra_flags', store=False
    )
    extra_required_map = fields.Serialized(
        compute='_compute_extra_flags', store=False
    )
   
    @api.depends('id')
    def _compute_extra_flags(self):
        configs = self.env['sale.extra.field.config'].search([])
        visible_map = {}
        required_map = {}

        for c in configs:
            visible_map[c.field_name] = bool(c.visible)
            required_map[c.field_name] = bool(c.required)

        for rec in self:
            rec.extra_visible_map = visible_map
            rec.extra_required_map = required_map

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
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super().fields_view_get(view_id, view_type, toolbar, submenu)

        if view_type == 'form':
            configs = self.env['sale.extra.field.config'].search([])

            for c in configs:
                if c.field_name in res['fields']:
                    res['fields'][c.field_name]['string'] =   c.label
                    res['fields'][c.field_name]['required'] = bool(c.required)

        return res

    def _prepare_invoice(self):
        vals = super()._prepare_invoice()
        fields = [
            'x_extra_text_1',
            'x_extra_text_2',
            'x_extra_number_1',
            'x_extra_date_1',
        ]
        for f in fields:
            vals[f] = getattr(self, f)
        return vals