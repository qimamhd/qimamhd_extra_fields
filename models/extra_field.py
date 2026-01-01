# -*- coding: utf-8 -*-

from datetime import datetime, time
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
 
 
class SaleExtraFieldConfig(models.Model):
    _name = 'sale.extra.field.config'
    _description = 'Sale Extra Field Configuration'

    field_name = fields.Selection([
        ('x_extra_text_1', 'Extra Text 1'),
        ('x_extra_text_2', 'Extra Text 2'), 
        ('x_extra_text_3', 'Extra Text 3'),
        ('x_extra_text_4', 'Extra Text 4'),
        ('x_extra_text_5', 'Extra Text 5'),
      
        ('x_extra_number_1', 'Extra Number 1'),
        ('x_extra_number_2', 'Extra Number 2'),
        ('x_extra_number_3', 'Extra Number 3'),
        ('x_extra_number_4', 'Extra Number 4'),
        ('x_extra_number_5', 'Extra Number 5'),
                    
        ('x_extra_date_1', 'Extra Date 1'),
        ('x_extra_date_2', 'Extra Date 2'),
        ('x_extra_date_3', 'Extra Date 3'),
        ('x_extra_date_4', 'Extra Date 4'),
        ('x_extra_date_5', 'Extra Date 5'),

        ('x_extra_boolean_1', 'Extra Boolean 1'),
        ('x_extra_boolean_2', 'Extra Boolean 2'),
        ('x_extra_boolean_3', 'Extra Boolean 3'),
        ('x_extra_boolean_4', 'Extra Boolean 4'),
        ('x_extra_boolean_5', 'Extra Boolean 5'),

    ], required=True)

    label = fields.Char(string='Label',required=True)
    visible = fields.Boolean(default=True)
    required = fields.Boolean(default=False)

    _sql_constraints = [
        ("extra_field_unique",
         "UNIQUE(field_name)",
         "تنبيه .. نوع الحقل تم اضافتة مسبقا لا يمكن الاستمرار"),
    ]