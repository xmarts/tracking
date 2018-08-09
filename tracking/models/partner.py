## -*- coding: utf-8 -*-

from openerp import models, fields, api, _, tools
from openerp.exceptions import UserError, RedirectWarning, ValidationError
import shutil
import logging
_logger = logging.getLogger(__name__)
class ResPartner(models.Model):
    _inherit="res.partner"
    phone = fields.Char(string="Telefono")
    name_commercial = fields.Char(string="Nombre Comercial")
    sector_id = fields.Many2one('partner.sector', string="Sector")
    categorysector_id = fields.Many2one('category.sector', string="Categoria del Sector")
    zona = fields.Many2one('res.zona', string="Zona Preventa")
    zona2 = fields.Many2one('res.zona2', string="Zona Reparto")
    day1 = fields.Selection(string="Día de Entrega 1 ",
                            selection=[('monday', 'Lunes'), ('tuesday', 'Martes'), ('wednesday', 'Miércoles'),
                                       ('thursday', 'Jueves'), ('friday', 'Viernes'), ('saturday', 'Sábado'),
                                       ('sunday', 'Domingo')])
    day2 = fields.Selection(string="Día de Entrega 2 ",
                            selection=[('monday', 'Lunes'), ('tuesday', 'Martes'), ('wednesday', 'Miércoles'),
                                       ('thursday', 'Jueves'), ('friday', 'Viernes'), ('saturday', 'Sábado'),
                                       ('sunday', 'Domingo')])
    day3 = fields.Selection(string="Día de Entrega 3 ",
                            selection=[('monday', 'Lunes'), ('tuesday', 'Martes'), ('wednesday', 'Miércoles'),
                                       ('thursday', 'Jueves'), ('friday', 'Viernes'), ('saturday', 'Sábado'),
                                       ('sunday', 'Domingo')])
    sellersecundary_id = fields.Many2one('res.users', string="Vendedor Secundario")
    process = fields.Boolean(string="A procesar", default=False)
    date = fields.Date(string="Fecha")
    channelsales_id = fields.Selection(string="Canal de Ventas",
                                       selection=[('local', 'Locales'), ('autoservice', 'Autoservicio'), ('distribuitor', 'Distribuidores'),
                                       ('export', 'Exportaciones'), ('special', 'Especiales')])
    whithout_invoice = fields.Boolean(string="Sin Factura", default=False)
    @api.model
    def create(self, vals):
        child_id = []
        if 'child_ids' in vals:
            vals['type'] = 'contact';
            print(vals)
            child_id.append(vals['child_ids'])
            if len(child_id[0]) == 0:
                raise UserError('Es necesario dar de alta una  Dirección de Entrega')
        return super(ResPartner, self).create(vals)
