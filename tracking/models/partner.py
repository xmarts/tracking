## -*- coding: utf-8 -*-

from openerp import models, fields, api, _, tools
from openerp.exceptions import UserError, RedirectWarning, ValidationError
import shutil
import logging
_logger = logging.getLogger(__name__)


id_line = []
day_of_route = ''

class ResPartner(models.Model):
    _inherit="res.partner"


    sequence = fields.Integer(string="Secuencia")
    partner_type_lx = fields.Selection([('rutas','Ruta'),('maquila','Maquila'),('autoservicios','Autoservicios'),('mayorista','Mayorista'),('noident','No Identificado')], string="Tipo Cliente", default='rutas')
    phone = fields.Char(string="Telefono")
    name_commercial = fields.Char(string="Nombre Comercial")
    sector_id = fields.Many2one('partner.sector', string="Sector")
    categorysector_id = fields.Many2one('category.sector', string="Categoria del Sector")
    zona = fields.Many2one('res.zona', string="Zona Preventa/Venta")
    zonalac = fields.Many2one('res.zona', string="Zona Preventa/Venta Lacteos")
    zona2 = fields.Many2one('res.zona', string="Zona Reparto")
    dia_lunes_seq =fields.Integer(string="Lunes")    
    dia_martes_seq =fields.Integer(string="Martes")
    dia_miercoles_seq =fields.Integer(string="Miercoles")
    dia_jueves_seq =fields.Integer(string="Jueves")
    dia_viernes_seq =fields.Integer(string="Viernes")
    dia_sabado_seq =fields.Integer(string="Sabado")
    dia_domingo_seq =fields.Integer(string="Domingo")


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
    day4 = fields.Selection(string="Día de Entrega 4 ",
                            selection=[('monday', 'Lunes'), ('tuesday', 'Martes'), ('wednesday', 'Miércoles'),
                                       ('thursday', 'Jueves'), ('friday', 'Viernes'), ('saturday', 'Sábado'),
                                       ('sunday', 'Domingo')])
    day5 = fields.Selection(string="Día de Entrega 5 ",
                            selection=[('monday', 'Lunes'), ('tuesday', 'Martes'), ('wednesday', 'Miércoles'),
                                       ('thursday', 'Jueves'), ('friday', 'Viernes'), ('saturday', 'Sábado'),
                                       ('sunday', 'Domingo')])
    day6 = fields.Selection(string="Día de Entrega 6 ",
                            selection=[('monday', 'Lunes'), ('tuesday', 'Martes'), ('wednesday', 'Miércoles'),
                                       ('thursday', 'Jueves'), ('friday', 'Viernes'), ('saturday', 'Sábado'),
                                       ('sunday', 'Domingo')])
    day7 = fields.Selection(string="Día de Entrega 7 ",
                            selection=[('monday', 'Lunes'), ('tuesday', 'Martes'), ('wednesday', 'Miércoles'),
                                       ('thursday', 'Jueves'), ('friday', 'Viernes'), ('saturday', 'Sábado'),
                                       ('sunday', 'Domingo')])
    dia_lunes = fields.Boolean(string="Día de Entrega 1", default=False)
    dia_martes = fields.Boolean(string="Día de Entrega 2", default=False)
    dia_miercoles = fields.Boolean(string="Día de Entrega 3", default=False)
    dia_jueves = fields.Boolean(string="Día de Entrega 4", default=False)
    dia_viernes = fields.Boolean(string="Día de Entrega 5", default=False)
    dia_sabado = fields.Boolean(string="Día de Entrega 6", default=False)
    dia_domingo = fields.Boolean(string="Día de Entrega 7", default=False)

    dia_ruta2_lunes = fields.Boolean(string="Día Entrega Lacteos 1", default=False)
    dia_ruta2_martes = fields.Boolean(string="Día Entrega Lacteos 2", default=False)
    dia_ruta2_miercoles = fields.Boolean(string="Dde Entrega Lacteos 3", default=False)
    dia_ruta2_jueves = fields.Boolean(string="Día Entrega Lacteos 4", default=False)
    dia_ruta2_viernes = fields.Boolean(string="Día Entrega Lacteos 5", default=False)
    dia_ruta2_sabado = fields.Boolean(string="Día Entrega Lacteos 6", default=False)
    dia_ruta2_domingo = fields.Boolean(string="Día Entrega Lacteos 7", default=False)

    sellersecundary_id = fields.Many2one('res.users', string="Vendedor Secundario")
    process = fields.Boolean(string="A procesar", default=False)
    date = fields.Date(string="Fecha")
    channelsales_id = fields.Selection(string="Canal de Ventas",
                                       selection=[('local', 'Locales'), ('autoservice', 'Autoservicio'), ('distribuitor', 'Distribuidores'),
                                       ('export', 'Exportaciones'), ('special', 'Especiales')])
    whithout_invoice = fields.Boolean(string="Sin Factura", default=False)

    usa_folio = fields.Boolean(string="Usa Folio ?", default=False, help="Se marca cuando el cliente usa un folio para registrar su venta, por ejemplo OXXO.")

    codigo_comprador = fields.Many2one('codigo.comprador',string="Codigo Comprador")
    plaza = fields.Char(string="Plaza")

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


    # @api.multi
    # def  assgin_seqquence_day(self):
    #     sequence_line = self.env['sequence.line.wizard']
    #     sequence_line.search([]).unlink()
    #     self.clean_id()
    #     partner = self.env['res.partner'].browse(self._context.get('active_ids', []))
    #     for rec in partner:
    #         if rec.id not in id_line:
    #               id_line.append(rec.id)
    #     cli = self.env['res.partner'].search([('id','in', id_line)])
    #     vals = []
    #     for x_cli in cli:

    #         vals.append({
    #             'id_partner': x_cli.id,
    #             'name': x_cli.name,
    #             'sequence': x_cli.dia_lunes_seq
    #         })
    #     print(vals)
    #     sequence_line.create(vals)
    #     # self.env['sequence.assign.wizard'].aupdated_information()

    #     action = {
    #         "type": "ir.actions.act_window",
    #         "view_mode": "form",
    #         "res_model": "sequence.assign.wizard",
    #         "target": "new"
    #     }
    #     return action

    # @api.multi
    # def clean_id(self):
    #     del id_line[:]



class WizardAssignSequence(models.Model):
    _name = 'sequence.assign.wizard'

    @api.model
    def default_get(self, fields_list):
        global day_of_route
        print(day_of_route)
        res = super(WizardAssignSequence, self).default_get(fields_list)
        partner = id_line
        if not partner:
            return {}
        vals = []
        cliente = self.env['res.partner']
        # for x_cli in cliente.browse(partner):
        for x_cli in cliente.search([('id','in', partner)],\
                                    order='dia_lunes_seq asc,\
                                    dia_martes_seq asc,\
                                    dia_miercoles_seq asc,\
                                    dia_viernes_seq asc ,\
                                    dia_jueves_seq asc,\
                                    dia_sabado_seq asc'):
            vals.append((0,0,{
                'id_partner': x_cli.id,
                'name': x_cli.name,
                'sequence': x_cli.dia_lunes_seq,
            }))
        print(vals)
        res.update(sequence_lines = vals)
        day_of_route = ''
        return res

    dias = fields.Selection(
        [('lunes','Lunes'),
        ('martes','Martes'),
        ('miercoles','Miercoles'),
        ('jueves','Jueves'),
        ('viernes','Viernes'),
        ('sabado','Sabado'),
        ('domingo','Domingo')
        ], default='lunes', string="Dias"
    )
    sequence_lines = fields.One2many('sequence.line.wizard','sequence_id','Lineas Sequence')

    @api.multi
    def assign(self):
        for rec in self.sequence_lines:
            print(rec.id_partner.id, rec.sequence)
            partner = self.env['res.partner'].browse(self._context.get('active_ids', []))
            clientes = self.env['res.partner'].search([('id', 'in', partner)])
            for part in clientes:
               if rec.id_partner.id == part.id:
                    if rec.dias == 'lunes':
                        part.dia_lunes_seq
                        print(rec.sequence, 'LINE')
            # for line in rec.sequence_lines:
                # rec.dia_lunes_seq = rec.sequence
            # if self.dias == 'martes':
            #     rec.dia_martes_seq = rec.sequence
            # if self.dias == 'miercoles':
            #     rec.dia_miercoles_seq = rec.sequence
            # if self.dias == 'jueves':
            #     rec.dia_jueves_seq = rec.sequence
            # if self.dias == 'viernes':
            #     rec.dia_viernes_seq = rec.sequence
            # if self.dias == 'sabado':
            #     rec.dia_sabado_seq = rec.sequence
            # if self.dias == 'domingo':
            #     rec.dia_domingo_seq = rec.sequence


class LineSequenceWizard(models.Model):
    _name = 'sequence.line.wizard'
    _order = 'sequence'

    sequence_id = fields.Many2one('sequence.assign.wizard', string="Lineas de secuencia")
    id_partner = fields.Many2one('res.partner', string="Cliente")
    name = fields.Char(string="Nombre")
    sequence = fields.Integer(string="Secuencia")
    test = fields.Boolean(
        string='Field Label',
    )

class DiasTransientModel(models.TransientModel):
    _name = 'select.day.routes'

    dias = fields.Selection(
        [('lunes','Lunes'),
        ('martes','Martes'),
        ('miercoles','Miercoles'),
        ('jueves','Jueves'),
        ('viernes','Viernes'),
        ('sabado','Sabado'),
        ('domingo','Domingo')
        ], default='lunes', string="Dias"
    )

    @api.multi
    def select_day(self):
        global day_of_route
        
        day_of_route = self.dias

        self.clean_id()
        partner = self.env['res.partner'].browse(self._context.get('active_ids', []))
        for rec in partner:
            if rec.id not in id_line:
                  id_line.append(rec.id)
        action = {
            "type": "ir.actions.act_window",
            "src_model": 'res.partner',
            "key2": 'client_action_multi',
            "view_mode": "form,tree",
            "res_model": "sequence.assign.wizard",
            "target": "new"
        }
        return action or {'type': 'ir.actions.act_window_close'}

    @api.multi
    def clean_id(self):
        del id_line[:]


class CodigoComprador(models.Model):
  """Modelo para codigo de comprador"""
  _name = 'codigo.comprador'

  name = fields.Char(
      string='Codigo',
  )
    