# -*- coding: utf-8 -*-
# Copyright YEAR(S), AUTHOR(S)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api, _
import datetime

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def compute_onchange_invoice_line_ids(self):
        taxes_grouped = self.get_taxes_values()
        tax_lines = self.tax_line_ids.filtered('manual')
        for tax in taxes_grouped.values():
            tax_lines += tax_lines.new(tax)
        self.tax_line_ids = tax_lines
        return

class PosOrder(models.Model):
    _inherit = 'pos.order'

    @api.multi
    def action_pos_order_invoice_create(self):
        invoice_obj = self.env["account.invoice"]
        invoice_line_obj = self.env["account.invoice.line"]

        for rec in self:
            # Create Invoice
            if rec.partner_id:
                curr_invoice = {
                    'partner_id': rec.partner_id.id,
                    'account_id': rec.partner_id.property_account_receivable_id.id,
                    'state': 'draft',
                    'type':'out_invoice',
                    'date_invoice':datetime.date.today(),
                    'origin': "PosOrder: " + rec.name,
                    'sequence_number_next_prefix': False
                }

                inv_ids = invoice_obj.create(curr_invoice)
                inv_id = inv_ids.id

                if inv_ids:
                    for x in rec.lines:

                        # Create Invoice line
                        curr_invoice_line = {
                            'name': x.product_id.name,
                            'product_id': x.product_id.id,
                            'price_unit': x.price_unit or 0,
                            'quantity': x.qty,
                            'account_id': x.product_id.categ_id.property_account_income_categ_id.id,
                            'invoice_id': inv_id,
                            'uom_id': x.product_id.uom_id.id,
                            'invoice_line_tax_ids': [(6,0,x.product_id.taxes_id.ids)]
                        }

                        inv_line_ids = invoice_line_obj.create(curr_invoice_line)
                        inv_line_ids._set_taxes()
                inv_ids.compute_onchange_invoice_line_ids()
                inv_ids.invoice_line_move_line_get()
                inv_ids.get_taxes_values()
                inv_ids.action_invoice_open()
                rec.account_move = inv_ids.move_id.id