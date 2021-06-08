## -*- coding: utf-8 -*-
from odoo.exceptions import UserError, ValidationError
from openerp import models, fields, api, _, tools
import logging
_logger = logging.getLogger(__name__)
class PosSession(models.Model):
    _inherit = 'pos.session'
    sync = fields.Boolean(string="Sync Warehouse", default=False)
    last_sysc = fields.Date(string="Last Sync")


    @api.constrains('user_id', 'state')
    def _check_unicity(self):
        # open if there is no session in 'opening_control', 'opened', 'closing_control' for one user
        if self.search_count([
                ('state', 'not in', ('closed', 'closing_control')),
                ('user_id', '=', self.user_id.id),
                ('rescue', '=', False)
            ]) > 50:
            raise ValidationError(_("You cannot create two active sessions with the same responsible."))

    @api.multi
    def login(self):
        for rec in self:
            rec.ensure_one()
            rec.write({
                'login_number': rec.login_number + 1,
            })

    def _confirm_orders(self):
        for session in self:
            company_id = session.config_id.journal_id.company_id.id
            orders = session.order_ids.filtered(lambda order: order.state == 'paid')
            journal_id = self.env['ir.config_parameter'].sudo().get_param(
                'pos.closing.journal_id_%s' % company_id, default=session.config_id.journal_id.id)
            if not journal_id:
                raise UserError(_("You have to set a Sale Journal for the POS:%s") % (session.config_id.name,))

            move = self.env['pos.order'].with_context(force_company=company_id)._create_account_move(session.start_at, session.name, int(journal_id), company_id)
            orders.with_context(force_company=company_id)._create_account_move_line(session, move)
            for order in session.order_ids.filtered(lambda o: o.state not in ['done', 'invoiced']):
                if order.state not in ('paid', 'pending'):
                    raise UserError(
                        _("You cannot confirm all orders of this session, because they have not the 'paid' status.\n"
                          "{reference} is in state {state}, total amount: {total}, paid: {paid}").format(
                            reference=order.pos_reference or order.name,
                            state=order.state,
                            total=order.amount_total,
                            paid=order.amount_paid,
                        ))
                order.action_pos_order_done()
            orders_to_reconcile = session.order_ids._filtered_for_reconciliation()
            orders_to_reconcile.sudo()._reconcile_payments()