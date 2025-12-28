# -*- coding: utf-8 -*-

from datetime import datetime, time
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT


class SaleExtraFieldConfig(models.Model):
    _name = 'sale.extra.field.config'
    _description = 'Sale Extra Field Configuration'

    name = fields.Char(string='Field Name', required=True)
    field_type = fields.Selection([
        ('char', 'Text'),
        ('float', 'Number'),
        ('boolean', 'Checkbox'),
        ('date', 'Date'),
        ('selection', 'Selection'),
    ], string='Field Type', required=True)
    default_label = fields.Char(string='Default Label', required=True)
    custom_label = fields.Char(string='Custom Label')
    required = fields.Boolean(string='Required')
    visible = fields.Boolean(string='Visible', default=False)
    selection_values = fields.Text(string='Selection Values (if type=Selection)')
