## -*- coding: utf-8 -*-

from openerp import models, fields, api, _, tools
import logging
_logger = logging.getLogger(__name__)
class PosSession(models.Model):
    _inherit = 'pos.session'
    sync = fields.Boolean(string="Sync Warehouse", default=False)
    last_sysc = fields.Date(string="Last Sync")
