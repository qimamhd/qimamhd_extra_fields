# -*- coding: utf-8 -*-
from datetime import datetime, time
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT

class SaleOrder(models.Model):
    _inherit = 'sale.order'

   # Extra fields
    x_extra_text_1 = fields.Char()
    x_extra_text_2 = fields.Char()
    x_extra_number_1 = fields.Float()
    x_extra_date_1 = fields.Date()
    x_extra_boolean_1 = fields.Boolean()

    # Helper fields
    x_extra_text_1_visible = fields.Boolean(compute='_compute_extra_flags')
    x_extra_text_1_required = fields.Boolean(compute='_compute_extra_flags')

    x_extra_text_2_visible = fields.Boolean(compute='_compute_extra_flags')
    x_extra_text_2_required = fields.Boolean(compute='_compute_extra_flags')

    x_extra_number_1_visible = fields.Boolean(compute='_compute_extra_flags')
    x_extra_number_1_required = fields.Boolean(compute='_compute_extra_flags')

    x_extra_date_1_visible = fields.Boolean(compute='_compute_extra_flags')
    x_extra_date_1_required = fields.Boolean(compute='_compute_extra_flags')

    x_extra_boolean_1_visible = fields.Boolean(compute='_compute_extra_flags')
    x_extra_boolean_1_required = fields.Boolean(compute='_compute_extra_flags')
   
    @api.depends('id')
    def _compute_extra_flags(self):
        configs = self.env['sale.extra.field.config'].search([])
        config_map = {c.field_name: c for c in configs}

        for rec in self:
            for field_name, config in config_map.items():
                visible_field = f'{field_name}_visible'
                required_field = f'{field_name}_required'

                if visible_field in rec._fields:
                    rec[visible_field] = bool(config.visible)

                if required_field in rec._fields:
                    rec[required_field] = bool(config.required)

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