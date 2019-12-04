# -*- coding: utf-8 -*-

import time

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError

class PartnerProcess(models.TransientModel):
    _name = "quotatio.pos.report"
    _description = "Reporte de carga"