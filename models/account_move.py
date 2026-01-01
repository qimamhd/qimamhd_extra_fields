# -*- coding: utf-8 -*-

from datetime import datetime, time
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
 
class AccountMove(models.Model):
    _inherit = 'account.move'

    # ======================
    # TEXT
    # ======================
    x_extra_text_1 = fields.Char()
    x_extra_text_2 = fields.Char()
    x_extra_text_3 = fields.Char()
    x_extra_text_4 = fields.Char()
    x_extra_text_5 = fields.Char()

    # ======================
    # NUMBER
    # ======================
    x_extra_number_1 = fields.Float()
    x_extra_number_2 = fields.Float()
    x_extra_number_3 = fields.Float()
    x_extra_number_4 = fields.Float()
    x_extra_number_5 = fields.Float()

    # ======================
    # DATE
    # ======================
    x_extra_date_1 = fields.Date()
    x_extra_date_2 = fields.Date()
    x_extra_date_3 = fields.Date()
    x_extra_date_4 = fields.Date()
    x_extra_date_5 = fields.Date()

    # ======================
    # BOOLEAN
    # ======================
    x_extra_boolean_1 = fields.Boolean()
    x_extra_boolean_2 = fields.Boolean()
    x_extra_boolean_3 = fields.Boolean()
    x_extra_boolean_4 = fields.Boolean()
    x_extra_boolean_5 = fields.Boolean()

    # ======================
    # Helpers for visibility / required
    # ======================
   @api.depends('x_extra_text_1', 'x_extra_text_2', 'x_extra_text_3', 'x_extra_text_4', 'x_extra_text_5',
        'x_extra_number_1', 'x_extra_number_2', 'x_extra_number_3', 'x_extra_number_4', 'x_extra_number_5',
        'x_extra_date_1', 'x_extra_date_2', 'x_extra_date_3', 'x_extra_date_4', 'x_extra_date_5',
        'x_extra_boolean_1', 'x_extra_boolean_2', 'x_extra_boolean_3', 'x_extra_boolean_4', 'x_extra_boolean_5')
    def _compute_extra_flags(self):
        configs = self.env['sale.extra.field.config'].search([])
        config_map = {c.field_name: c for c in configs}

        for rec in self:
            for fname, config in config_map.items():
                visible_field = f'{fname}_visible'
                required_field = f'{fname}_required'

                if visible_field in rec._fields:
                    rec[visible_field] = bool(config.visible)

                if required_field in rec._fields:
                    rec[required_field] = bool(config.required)

    # Define helpers fields
    x_extra_text_1_visible = fields.Boolean(compute='_compute_extra_flags')
    x_extra_text_1_required = fields.Boolean(compute='_compute_extra_flags')
    x_extra_text_2_visible = fields.Boolean(compute='_compute_extra_flags')
    x_extra_text_2_required = fields.Boolean(compute='_compute_extra_flags')
    x_extra_text_3_visible = fields.Boolean(compute='_compute_extra_flags')
    x_extra_text_3_required = fields.Boolean(compute='_compute_extra_flags')
    x_extra_text_4_visible = fields.Boolean(compute='_compute_extra_flags')
    x_extra_text_4_required = fields.Boolean(compute='_compute_extra_flags')
    x_extra_text_5_visible = fields.Boolean(compute='_compute_extra_flags')
    x_extra_text_5_required = fields.Boolean(compute='_compute_extra_flags')

    # Number helpers
    x_extra_number_1_visible = fields.Boolean(compute='_compute_extra_flags')
    x_extra_number_1_required = fields.Boolean(compute='_compute_extra_flags')
    x_extra_number_2_visible = fields.Boolean(compute='_compute_extra_flags')
    x_extra_number_2_required = fields.Boolean(compute='_compute_extra_flags')
    x_extra_number_3_visible = fields.Boolean(compute='_compute_extra_flags')
    x_extra_number_3_required = fields.Boolean(compute='_compute_extra_flags')
    x_extra_number_4_visible = fields.Boolean(compute='_compute_extra_flags')
    x_extra_number_4_required = fields.Boolean(compute='_compute_extra_flags')
    x_extra_number_5_visible = fields.Boolean(compute='_compute_extra_flags')
    x_extra_number_5_required = fields.Boolean(compute='_compute_extra_flags')

    # Date helpers
    x_extra_date_1_visible = fields.Boolean(compute='_compute_extra_flags')
    x_extra_date_1_required = fields.Boolean(compute='_compute_extra_flags')
    x_extra_date_2_visible = fields.Boolean(compute='_compute_extra_flags')
    x_extra_date_2_required = fields.Boolean(compute='_compute_extra_flags')
    x_extra_date_3_visible = fields.Boolean(compute='_compute_extra_flags')
    x_extra_date_3_required = fields.Boolean(compute='_compute_extra_flags')
    x_extra_date_4_visible = fields.Boolean(compute='_compute_extra_flags')
    x_extra_date_4_required = fields.Boolean(compute='_compute_extra_flags')
    x_extra_date_5_visible = fields.Boolean(compute='_compute_extra_flags')
    x_extra_date_5_required = fields.Boolean(compute='_compute_extra_flags')

    # Boolean helpers
    x_extra_boolean_1_visible = fields.Boolean(compute='_compute_extra_flags')
    x_extra_boolean_1_required = fields.Boolean(compute='_compute_extra_flags')
    x_extra_boolean_2_visible = fields.Boolean(compute='_compute_extra_flags')
    x_extra_boolean_2_required = fields.Boolean(compute='_compute_extra_flags')
    x_extra_boolean_3_visible = fields.Boolean(compute='_compute_extra_flags')
    x_extra_boolean_3_required = fields.Boolean(compute='_compute_extra_flags')
    x_extra_boolean_4_visible = fields.Boolean(compute='_compute_extra_flags')
    x_extra_boolean_4_required = fields.Boolean(compute='_compute_extra_flags')
    x_extra_boolean_5_visible = fields.Boolean(compute='_compute_extra_flags')
    x_extra_boolean_5_required = fields.Boolean(compute='_compute_extra_flags')

    
    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super().fields_view_get(view_id, view_type, toolbar, submenu)

        if view_type == 'form':
            configs = self.env['sale.extra.field.config'].search([])
            for c in configs:
                if c.field_name in res['fields']:
                    res['fields'][c.field_name]['string'] = c.label
        return res