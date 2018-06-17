## -*- coding: utf-8 -*-

from openerp import models, fields, api, _, tools
from openerp.exceptions import UserError, RedirectWarning, ValidationError
import shutil
import logging
_logger = logging.getLogger(__name__)
class SaleOrder(models.Model):
    _inherit = "sale.order"
    reason_rejection = fields.Many2one('reason.rejection',string="Motivo de Rechazo")
    zona = fields.Char(string="Zona")

    @api.onchange('partner_id')
    def zonapartner(self):
        self.zona = self.partner_id.zona

    @api.multi
    def recompute_coupon_lines2(self):
        #raise UserError(_("hola"))
        hi = self.id
        for order in self:
            order._remove_invalid_reward_lines2()
            order._create_new_no_code_promo_reward_lines2()
            order._update_existing_reward_lines2()

    def _remove_invalid_reward_lines2(self):
        '''Unlink reward order lines that are not applicable anymore'''
        invalid_lines = self.env['sale.order.line']
        for order in self:
            new_applicable_programs = order._get_applicable_no_code_promo_program() + order._get_applicable_programs()
            old_applicable_programs = order.no_code_promo_program_ids + order.applied_coupon_ids.mapped(
                'program_id') + order.code_promo_program_id
            programs_to_remove = old_applicable_programs - new_applicable_programs
            products_to_remove = (programs_to_remove).mapped('discount_line_product_id')
            self.generated_coupon_ids.filtered(
                lambda coupon: coupon.program_id.discount_line_product_id.id in products_to_remove.ids).write(
                {'state': 'expired'})
            order.no_code_promo_program_ids -= programs_to_remove
            order.code_promo_program_id -= programs_to_remove
            order.applied_coupon_ids -= order.applied_coupon_ids.filtered(
                lambda coupon: coupon.program_id in programs_to_remove)
            invalid_lines |= order.order_line.filtered(lambda line: line.product_id.id in products_to_remove.ids)
            order.write({'order_line': [(2, line.id, False) for line in invalid_lines]})

    def _create_new_no_code_promo_reward_lines2(self):
        '''Apply new programs that are applicable'''
        self.ensure_one()
        order = self
        programs = order._get_applicable_no_code_promo_program()
        for program in programs:
            error_status = program._check_promo_code(order, False)
            if not error_status.get('error') and program.promo_applicability == 'on_next_order':
                order._create_reward_coupon(program)
                order.no_code_promo_program_ids |= program
            elif not error_status.get('error') and program.discount_line_product_id.id not in self.order_line.mapped(
                    'product_id').ids:
                self.write({'order_line': [(0, False, order._get_reward_line_values(program))]})
                order.no_code_promo_program_ids |= program

    def _update_existing_reward_lines2(self):
        '''Update values for already applied rewards'''
        self.ensure_one()
        order = self
        applied_programs = order.no_code_promo_program_ids + \
                           order.applied_coupon_ids.mapped('program_id') + \
                           order.code_promo_program_id
        for program in applied_programs:
            values = order._get_reward_line_values(program)
            lines = order.order_line.filtered(lambda line: line.product_id == program.discount_line_product_id)
            # Remove reward line if price or qty equal to 0
            if values['product_uom_qty'] and values['price_unit']:
                order.write({'order_line': [(1, line.id, values) for line in lines]})
            else:
                if program.reward_type != 'free_shipping':
                    order.write({'order_line': [(2, line.id, False) for line in lines]})
                else:
                    values.update(price_unit=0.0)
                    order.write({'order_line': [(1, line.id, values) for line in lines]})
