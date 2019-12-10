# -*- coding: utf-8 -*-

import time

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError
from datetime import datetime, date

class PartnerProcess(models.Model):
	_name = "quotation.pos.report"
	_description = "Reporte de carga"

	employee_id = fields.Many2one('hr.employee', string='Empleado')
	date = fields.Date(string='Fecha de pedidos', default=date.today())
