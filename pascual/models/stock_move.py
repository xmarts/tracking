## -*- coding: utf-8 -*-

from openerp import models, fields, api, _, tools
from openerp.exceptions import UserError, RedirectWarning, ValidationError
import shutil
import logging
_logger = logging.getLogger(__name__)
class StockMove(models.Model):
    _inherit = "stock.move"
    zona = fields.Many2one('res.zona', related="picking_partner_id.zona", store=True)