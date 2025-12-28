# -*- coding: utf-8 -*-

from datetime import datetime, time
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT

 

class xx_car_work_order(models.Model):
    _inherit =  'mizan.car.work.procedure.master'

    drum_counter = fields.Char(string="عداد وقت الدخول")

    drum_counter_exit = fields.Char(string="عداد وقت الخروج")
    

    def sale_order(self):
        for rec in self:
            res = super(xx_car_work_order,self).sale_order()
            rec.sale_order_id.action_confirm()
            rec.call_invoice()

           
    def call_invoice(self):
        for rec in self:
            invoice = self.env['account.move'].search([('work_order_id', '=', rec.id)])

            action = self.env.ref('account.action_move_out_invoice_type')
            result = action.read()[0]
            result.pop('id', None)
            result['context'] = {}
            result['domain'] = [('id', '=', invoice.id),('type','in',['out_refund','out_invoice'])]

            if invoice:
                res = self.env.ref('account.view_move_form', False)
                result['views'] = [(res and res.id or False, 'form')]
                result['res_id'] = invoice.id or False
            return result

    def register_payment(self):
        advanced_amount = 0
        remaining_amount = 0
        for rec in self:
            payment = self.env['mizan.register.payment'].search([('header_id', '=', rec.entry_card_id.id),('state', '!=', 'cancel'),('work_order_id','=', rec.id)])
 
            for line in payment:
                advanced_amount = advanced_amount + line.payment_amount
           
            if advanced_amount >=  rec.total_all_with_tax:
                raise ValidationError(
                    "اكتمل الدفع  .. لا يمكن انشاء مفوعات جديدة ")

             
            remaining_amount = rec.total_all_with_tax - advanced_amount

            return {
                'name': _('Register Payment'),
                'view_mode': 'form',
                'res_model': 'mizan.register.payment',
                'view_id': self.env.ref('qimamhd_mizan_car_13.mizan_payment_view').id,
                'type': 'ir.actions.act_window',
                'context': {'default_invoice_amount': rec.total_all_with_tax,
                            'default_advanced_amount': advanced_amount,
                            'default_remaining_amount': remaining_amount, 'default_branch_id': rec.entry_card_id.branch_id.id,
                            'default_payment_note': "دفعة مقدمة لامر العمل",

                            'default_header_id': rec.entry_card_id.id, 'default_work_order_id': rec.id, 'default_payment_amount': remaining_amount if remaining_amount else 0,
                            },
                'target': 'current'
            }

class xx_car_checkup_spare_parts_lines(models.Model):
    _inherit = 'mizan.car.spare.parts.lines'
    
    @api.onchange('qty_done')
    def set_qty_done(self):
        for rec in self:
            rec.qty = rec.qty_done



class xx_checkup_register_payment(models.Model):
    _inherit = 'mizan.register.payment'

    state = fields.Selection(selection_add= [("cancel", "ملغي")])
    payment_id = fields.Many2one('account.payment', )


    def create_payment_wo(self):
        for rec in self:
            if rec.payment_amount <= 0:
                raise ValidationError(
                    "يجب تحديد المبلغ اولا")

            payment = self.env['mizan.register.payment'].search([('work_order_id','=', rec.header_id.work_order_id.id),('state', '=', 'posted')])
            advanced_amount = 0
            for line in payment:
                advanced_amount = advanced_amount + line.payment_amount

           
            account_payment = self.env['account.payment'].search([('work_order_id', '=', rec.header_id.work_order_id.id),('state', '=', 'posted')])
            amount_total = rec.header_id.work_order_id.total_all_with_tax

            ready_amount = 0
            for line in account_payment:
                ready_amount = ready_amount + line.amount
              
            if ready_amount >= amount_total:
                raise ValidationError(
                    "اكتمل الدفع  في شاشة مدفوعات الفوترة لامر العمل المحدد .. لا يمكن انشاء مفوعات جديدة ")
          
            if advanced_amount >= amount_total:
                raise ValidationError(
                    "اكتمل الدفع للحجز .. لا يمكن انشاء مدفوعات جديدة ")



            self.inbound_payment_method = self.env['account.payment.method'].search([('payment_type','=', 'inbound')],limit=1)
            
            if not self.inbound_payment_method:
                self.inbound_payment_method = self.env['account.payment.method'].create({
                    'name': 'inbound',
                    'code': 'IN',
                    'payment_type': 'inbound',
                })
            payment = self.env['account.payment'].create({
                'payment_date': self.pay_date,
                'payment_method_id': self.inbound_payment_method.id,
                'payment_type': 'inbound',
                'partner_type': 'customer',
                'partner_id': self.header_id.partner_id.id,
                'amount': self.payment_amount,
                'journal_id': self.journal_id.id,
                'company_id': self.header_id.company_id.id,
                'branch_id': self.header_id.branch_id.id,
                'currency_id': self.env.company.currency_id.id,
                'payment_difference_handling': 'reconcile',
                'communication': self.payment_note,
                'entry_card_id': self.header_id.id,
                'work_order_id': self.header_id.work_order_id.id,
                  })
            payment.post()
            self.write({'state': 'posted'})
            self.write({'payment_id': payment.id})

            payment = self.env['mizan.register.payment'].search([('work_order_id','=', rec.header_id.work_order_id.id),('state', '!=', 'cancel')])
            advanced_amount = 0
            for line in payment:
                advanced_amount = advanced_amount + line.payment_amount
            wo = self.env['mizan.car.work.procedure.master'].search([('id', '=', rec.header_id.work_order_id.id)])

            wo.write({'advance_amount': advanced_amount})

    def cancel_payment_btn(self):
        for rec in self:
            if not self.user_has_groups('qimamhd_mizan_marahel_extend.group_cancel_register_payment'):
              raise ValidationError(
                    "لا توجد لديك صلاحية الغاء المدفوعات")
            else:
                rec.write({'state': 'cancel'})
                if self.payment_id:
                    self.payment_id.action_draft()
                    self.payment_id.cancel()

                payment = self.env['mizan.register.payment'].search([('header_id', '=', rec.header_id.work_order_id.id),('state', '!=', 'cancel')])
            
                advanced_amount = 0
                for line in payment:
                    advanced_amount = advanced_amount + line.payment_amount

                wo = self.env['mizan.car.work.procedure.master'].search([('id', '=', rec.header_id.work_order_id.id)])

                wo.write({'advance_amount': advanced_amount})
 
    def call_payments(self):
        for rec in self:
            action = self.env.ref('account.action_account_payments')
            result = action.read()[0]
            result.pop('id', None)
            result['context'] = {}
            result['domain'] = [('work_order_id', '=', rec.header_id.work_order_id.id)]
            return result
    def unlink(self):
        if not self.user_has_groups('qimamhd_mizan_marahel_extend.group_cancel_register_payment'):
              raise ValidationError(
                    "لا توجد لديك صلاحية حذف المدفوعات")

        else:

            if self.payment_id:
                self.payment_id.write({'communication':"تم حذف السند من المصدر من امر العمل" })
                self.payment_id.action_draft()
                self.payment_id.cancel()
            return super(xx_checkup_register_payment,self).unlink()