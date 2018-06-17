## -*- coding: utf-8 -*-

from openerp import models, fields, api, _, tools
from openerp.exceptions import UserError, RedirectWarning, ValidationError
import shutil
import logging
_logger = logging.getLogger(__name__)
class PartnerSector(models.Model):
    _name="partner.sector"
    _description="Sector"
    name = fields.Char(string="Sector")