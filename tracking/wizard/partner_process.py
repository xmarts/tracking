# -*- coding: utf-8 -*-

import time

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError


class PartnerProcess(models.TransientModel):
    _name = "res.partner.process"
    _description = "Procesar"

    type = fields.Selection([
        ('ENTREGA','Entrega'),
        ('VENTA','Venta')
        ], string='Type', copy=False, default='VENTA', required=True,)

    inicio = fields.Datetime(
        string="Fecha Inicio"
    )
    fecha_fin = fields.Datetime(
        string="Fecha Fin"
    )
    entry_date = fields.Datetime(
        string="Fecha de Entrega"
    )
    zona =  fields.Many2one(
        'res.zona', string="Zona"
    )

    @api.model
    def _count(self):
        return len(self._context.get('active_ids', []))
    count = fields.Integer(default=_count, string='# of Rutas')

    @api.multi
    def process(self):
        partner = self.env['res.partner'].browse(self._context.get('active_ids', []))
        zona = ''
        for rec in partner:
            zona = rec.zona.id
            self.zona = rec.zona.id
        res_p =self.env['res.partner'].search([('zona', '=', zona)])
        for record in res_p:
            empleado = self.env['hr.employee'].search([('address_home_id', '=', record.id)])
            for emp in empleado:
                if emp.ruta_open == False:
                    emp.ruta_open = True
        total = len(partner)
        route = self.env['route.order']
        for p in partner:
            shipping= self.env['res.partner'].search([('parent_id','=',p.id),('type','=','delivery')], limit=1)
            shipping_id = False
            if shipping:
                shipping_id = shipping.id
            else:
                shipping_id = p.id

            vals = {
                'name': 'New',
                'partner_id': p.id,
                'partner_shipping_id':shipping_id,
                'type': self.type,
                'manage_id':p.zona.user_id.id,
                'zone_id': p.zona.id,
                'validate_filters': False
            }
            route.create(vals)
    @api.multi
    def proccess_and_updated(self):
        if self.inicio and self.fecha_fin:
            quo = self.env['pos.quotation'].search([])
            partner = self.env['res.partner'].browse(self._context.get('active_ids', []))
            for quotations in quo:
                zona = ''
                for rec in partner:
                    zona = rec.zona2.id
                print(zona, 'qaaaaaaaaaaaaaaaaaaaa', self.inicio, self.fecha_fin, 'Fechas')
                if quotations.state == 'waiting_transfer' and zona == quotations.zona.id and quotations.create_date >= self.inicio and quotations.create_date <= self.fecha_fin:
                    print(quotations.name,'AAAAAAAAAAAAAAAAAAAAAAAAAA', quotations.create_date)
                    if self.entry_date:
                        quotations.delivery_date = self.entry_date
                    else:
                        raise UserError(_('Error. el Campo Fecha de Entrega debe llenarse para actualizar la informacion'))
            route_order = self.env['route.order'].search([])
            for route in route_order:
                zona = ''
                for rec in partner:
                    zona = rec.zona2.id
                if route.zona_repartos:
                    if route.state == '0' and zona == route.zona_repartos.id and route.create_date >= self.inicio and route.create_date <= self.fecha_fin and route.validate_filters == True:
                        if self.entry_date:
                            route.date_order = self.entry_date
                        else:
                            raise UserError(_('Error. el Campo Fecha de Entrega debe llenarse para actualizar la informacion'))
        else:
            raise UserError(_('Error. Los campos Fecha inicio y fecha fin deben llenarse'))



    @api.multi
    def process2(self):
        partner = self.env['res.partner'].browse(self._context.get('active_ids', []))
        total = len(partner)
        route = self.env['route.order']
        for p in partner:
            shipping= self.env['res.partner'].search([('parent_id','=',p.id),('type','=','delivery')], limit=1)
            shipping_id = False
            if shipping:
                shipping_id = shipping.id
            else:
                shipping_id = p.id

            vals = {
                'name': 'New',
                'partner_id': p.id,
                'partner_shipping_id':shipping_id,
                'manage_id':p.zonalac.user_id.id,
                'zone_id': p.zonalac.id
            }
            route.create(vals)