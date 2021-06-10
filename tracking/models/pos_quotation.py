# -*- coding: utf-8 -*-
# Copyright 2019, XMARTS
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, _, api

class PosQuotationLX(models.Model):
	_inherit = 'pos.quotation'

	is_lx_delivery = fields.Boolean(
	    string='Entrega de LXTRACK',
	    default=False
	)
	delivery_date = fields.Date(
	    string='Fecha Entrega',
	)
	sync_lx = fields.Boolean(
	    string='Sincronizado con LXTRACK ?',
	    default=False
	)
	state = fields.Selection([
        ('waiting_transfer', 'Waiting Transfer'),
        ('delivery_success', 'Delivery Success'),
        ('removed', 'Removed'),
        ('cancel', 'Cancelado')
    ], default='waiting_transfer', string='State')
	employee_id = fields.Many2one('hr.employee',string="Encargado", related="partner_id.zona2.user_id")
	partner_shipping_id = fields.Many2one('res.partner',string='Direccion de entrega')
	shop_ids = fields.Many2many('pos.shop', 'pos_quotation_pos_shop_rel', 'quotation_id', 'shop_id','Shop', required=False)
	zona = fields.Many2one('res.zona', string="Zona", related="partner_id.zona2", store=True)



class PosQuotationLine(models.Model):
	_inherit = 'pos.quotation.line'

	is_product_promo = fields.Boolean(
		string='Es Promocion?',
		default=False
	)