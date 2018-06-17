## -*- coding: utf-8 -*-

from openerp import models, fields, api, _, tools
from openerp.exceptions import UserError, RedirectWarning, ValidationError
import shutil
import logging
_logger = logging.getLogger(__name__)
class ProductTemplate(models.Model):
    _inherit="product.template"
    container_id = fields.Many2one('product.container', string="Envase")
    liters_container = fields.Float(string='Litros por Envase',
                               help='Litros por envase', digits=(12, 3))
    family_id = fields.Many2one('product.family', string="Familia")
    marca_id = fields.Many2one('product.marca', string="Marca")