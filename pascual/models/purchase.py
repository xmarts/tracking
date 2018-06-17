## -*- coding: utf-8 -*-

from openerp import models, fields, api, _, tools
from openerp.exceptions import UserError, RedirectWarning, ValidationError
import shutil
import logging
_logger = logging.getLogger(__name__)
class PurchaseOrder(models.Model):
    _inherit = "purchase.order"
    personal_id = fields.Many2one('res.users', string='Encargado',help='Personal encargado de la compra ')

    @api.multi
    def button_confirm(self):
        for order in self:
            attachment_obj = self.env['ir.attachment']
            adjuntos = attachment_obj.search([('res_model', '=', 'purchase.order'),
                                              ('res_id', '=', order.id)])
            if len(adjuntos) == 0:
                raise UserError(_("Error:Tiene que adjuntar un archivo"))
            else:
                if order.state not in ['draft', 'sent']:
                    continue
                order._add_supplier_to_product()
                # Deal with double validation process
                if order.company_id.po_double_validation == 'one_step' \
                        or (order.company_id.po_double_validation == 'two_step' \
                                    and order.amount_total < self.env.user.company_id.currency_id.compute(
                                order.company_id.po_double_validation_amount, order.currency_id)) \
                        or order.user_has_groups('purchase.group_purchase_manager'):
                    order.button_approve()
                else:
                    order.write({'state': 'to approve'})
        return True