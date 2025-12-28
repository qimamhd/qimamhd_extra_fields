
from datetime import datetime, time
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT

class entry_card(models.Model):
    _inherit = 'mizan.car.entry.card.master'
    
    def create_checkup_procedure(self):
        for rec in self:
                part_results = self.env['mizan.car.checkup.procedure.master'].search([('entry_card_id','=', rec.id)])

                if not part_results:
                        results_tmp = {
                            'partner_id': rec.partner_id.id,
                            'state': 'execute_started',
                            'car_panel_no': rec.car_panel_no,
                            'partner_mobile': rec.partner_mobile,
                            'car_size_id': rec.car_size_id.id,
                            'car_model': rec.car_model,
                            'car_type_id': rec.car_type_id.id,
                            'entry_card_id': rec.id,
                            'vin_no': rec.vin_no,
                            'sale_man_id': rec.sale_man_id.id,
                            'drum_counter': rec.drum_counter,
                            'create_date': datetime.today()

                        }

                        checkup_procedure = self.env['mizan.car.checkup.procedure.master'].create(results_tmp)
                        rec.write({'checkup_id': checkup_procedure.id})
                        rec.write({'state': 'execute_started'})
                        wo_procedure = checkup_procedure.create_work_order_procedure()
                        
                        action = self.env.ref('qimamhd_mizan_car_13.action_work_procedure_view')
                        result = action.read()[0]
                        result.pop('id', None)
                        # result['context'] = {'default_search_result': ''}
                        result['domain'] = [('checkup_id', '=', checkup_procedure.id)]
                        if wo_procedure:
                            res = self.env.ref('qimamhd_mizan_car_13.work_procedure_form_view', False)
                            result['views'] = [(res and res.id or False, 'form')]
                            result['res_id'] = wo_procedure.id or False

                        return result


 