# -*- coding: utf-8 -*-
import logging

from odoo import http
from odoo.http import request
from modules.tracking.odooclient import client
import json
from collections import OrderedDict


_logger = logging.getLogger(__name__)


class trackController(http.Controller):
    #parameter = {"CAT_CL":'2017-10-09 16:47:55',"CAT_PR":'-'}

    @http.route('/track', type='http', auth='user', methods=['GET'])
    def pos_web(self, debug=False,**k):
        print("valor par: %s"+ request.params['CAT_CL'])
        try:
            if request.params['CAT_CL']:
                partner_model = request.env['res.partner']
                fecha_inicio = str(request.params['CAT_CL']) + '.0'
                partner_ids = partner_model.sudo().search([('write_date','>=',fecha_inicio)])
                cont=str(len(partner_ids))
                data=str(request.params['CAT_CL']+' '+cont)
                partner_list = {'clientes': []}
                if partner_ids:
                    insertcliente=""
                    for p in partner_ids:
                        if str(p.active) == False:
                            activo = 0
                        else:
                            activo = 1
                        insertcliente = insertcliente + "INSERT OR REPLACE INTO CLIENTE(id,id_servidor,nombre,nombre_comercial,sitio_web,puesto_trabajo,tel,movil,fax,email,id_precio_lista,active)" + " VALUES((select id from cliente where id_servidor=" + str(p.id) + "), " + str(p.id) + ",'" + str(p.name) + "','" + str(p.display_name) + "','" + str(p.website) + "','" + str(p.function) + "','" + str(p.phone) + "','" + str(p.mobile) + "',,'" + str(p.email) + "',," + str(activo) + ");"
                    vals = {
                        data:insertcliente
                    }
                    partner_list['clientes'].append(vals)
                return json.dumps(partner_list)
        except Exception as e:
            print(e)
        return json.dumps({'status': 0, 'data': 'Some problem with API'})
        #return request.render('tracking.index')

