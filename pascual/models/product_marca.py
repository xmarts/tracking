## -*- coding: utf-8 -*-

from openerp import models, fields, api, _, tools
from openerp.exceptions import UserError, RedirectWarning, ValidationError
import shutil
import logging
_logger = logging.getLogger(__name__)
class ProductMarca(models.Model):
    _name="product.marca"
    _description="Tipo de Marca del Producto"
    name = fields.Char(string="Marca")