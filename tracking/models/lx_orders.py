# -*- coding: utf-8 -*-

from odoo import fields, models

class LxOrders (models.Model):
    _name = 'lx.orders'
    id = fields.Integer(string="Id")
    id_report = fields.Integer(string="Id Lx")
    route_orders_id=fields.Many2one('route.orders', string='Route Order', requiered=True)
    product_id = fields.Many2one('product.product', string='Product')
    qty = fields.Integer(string="Qty")
    promotion_id = fields.Integer(string="Promotion")
    create_date = fields.Datetime('Created on', index=True, readonly=True)
    create_uid = fields.Many2one('res.users', string='Created by', index=True, readonly=True)
    write_date = fields.Datetime('Update on', index=True, readonly=True)
    write_uid = fields.Many2one('res.users', string='Updated by', index=True, readonly=True)
