## -*- coding: utf-8 -*-

from openerp import models, fields, api, _, tools
import logging
_logger = logging.getLogger(__name__)
class SaleOrder(models.Model):
    _inherit = "sale.order"
    lxorder_id = fields.Integer(string='LxOrder', help='LxOrder')

