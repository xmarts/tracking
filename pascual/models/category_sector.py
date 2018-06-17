## -*- coding: utf-8 -*-

from openerp import models, fields, api, _, tools
from openerp.exceptions import UserError, RedirectWarning, ValidationError
import shutil
import logging
_logger = logging.getLogger(__name__)
class CategorySector(models.Model):
    _name="category.sector"
    _description="Categorías del Sector de Clientes"
    name = fields.Char(string="Categoria del Sector")