# -*- coding: utf-8 -*-

from datetime import datetime, time
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT

 


class xx_car_checkup_order(models.Model):
    _inherit =   'mizan.car.checkup.procedure.master'



    drum_counter = fields.Char(string="عداد وقت الدخول")

    drum_counter_exit = fields.Char(string="عداد وقت الخروج")


    

    def create_work_order_procedure(self):
        for rec in self:
            part_results = self.env['mizan.car.work.procedure.master'].search([('checkup_id', '=', rec.id)])

            if not part_results:
                pricelist = self.env['product.pricelist'].search([('branch_id', '=', rec.entry_card_id.branch_id.id)])
 
                results_tmp = {
                    'partner_id': rec.partner_id.id,
                    'state': 'work_order_started',
                    'car_panel_no': rec.car_panel_no,
                    'partner_mobile': rec.partner_mobile,
                    'car_size_id': rec.car_size_id.id,
                    'car_model': rec.car_model,
                    'car_type_id': rec.car_type_id.id,
                    'vin_no': rec.vin_no,
                    'sale_man_id': rec.sale_man_id.id,
                    'drum_counter':  rec.entry_card_id.drum_counter,
                    'checkup_id': rec.id,

                    'entry_card_id': rec.entry_card_id.id,
                    'branch_id': rec.entry_card_id.branch_id.id,
                    'pricelist_id': pricelist.id,
                    'create_date': datetime.today()

                }

                wo_procedure = self.env['mizan.car.work.procedure.master'].create(results_tmp)
                rec.write({'work_order_id': wo_procedure.id})
                rec.entry_card_id.write({'work_order_id':wo_procedure.id})
                rec.write({'state': 'work_order_started'})
                rec.entry_card_id.write({'state': 'work_order_started'})

                for line in rec.result_lines:
                    if line.selected:
                        
                          
                        products = self.env['mizan.car.work.procedure.line'].create({
                            # 'search_result': '',

                            'product_id': line.checkup_part_id.id,
                            'name': line.name,
                            'unit_price': rec.get_price_of_product(line.checkup_part_id),
                            'product_tax': line.checkup_part_id.taxes_id.id,

                            'technical_name': line.technical_name.ids if line.technical_name else False,
                            'header_id': wo_procedure.id,

                        })
                wo_procedure._cal_spare_parts_amounts()
                wo_procedure._cal_services_amounts()

                 
                return wo_procedure
 

class xx_car_checkup_sub_lines_line_add(models.Model):
    _inherit = 'mizan.car.checkup.procedure.line'
    
    checkup_part_result_id = fields.Many2many('mizan.default.results', string="نتيجة الفحص",
                                              copy=False,domain="[('product_id','=',product_tmpl_id)]")
