# -*- coding: utf-8 -*-

from datetime import datetime, time
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT

class ExtraFieldSetting(models.Model):
    _name = 'sale.extra.field.config'

    field_name = fields.Selection([
        ('x_extra_text_1', 'Extra Text 1'),
        ('x_extra_text_2', 'Extra Text 2'),
        ('x_extra_number_1', 'Extra Number 1'),
        ('x_extra_date_1', 'Extra Date 1'),
    ], required=True)

    label = fields.Char(string="Label")
    visible = fields.Boolean(default=True)
    required = fields.Boolean(default=False)
