# -*- coding: utf-8 -*-
import logging

from odoo import http
from odoo.http import request
from modules.tracking.odooclient import client
import json
from collections import OrderedDict


_logger = logging.getLogger(__name__)


class trackController(http.Controller):
    parameter = {"CAT_CL":'2017-10-09 16:47:55',"CAT_PR":'-'}

    @http.route('/track', type='http', auth='user', methods=['GET'])
    def pos_web(self, debug=False, params=parameter,**k):
        odoo = client.OdooClient(protocol='xmlrpc', host='localhost', dbname='odoo', port=8069, debug=True)
        odoo.ServerInfo()
        odoo.Authenticate('admin', 'admin')
        print(params.items())
        for key, valor in params.items():
            if key == 'CAT_CL':
                insertcliente = ''
                output = ""
                fecha_inicio = str(valor) + '.0'
                cont = odoo.SearchCount('res.partner',
                                        [('write_date', '>=', fecha_inicio)])
                print("cont %s"%cont)
                if cont == 0:
                    output = 'clientes = {}'
                else:
                    output = output  + 'clientes = {' + ' "' + valor + '" ' + str(cont) + ':['
                    partners = odoo.SearchRead('res.partner',
                                               [('write_date', '>=', fecha_inicio)],
                                               ['name', 'display_name', 'website', 'function', 'phone', 'mobile',
                                                'email',
                                                'active'])
                    print("Partnerssss %s" % len(partners))
                    for p in partners:
                        if str(p['active']) == False:
                            activo = 0
                        else:
                            activo = 1
                        insertcliente = insertcliente  + "INSERT OR REPLACE INTO CLIENTE(id,id_servidor,nombre,nombre_comercial,sitio_web,puesto_trabajo,tel,movil,fax,email,id_precio_lista,active)" + "\n\t\t VALUES((select id from cliente where id_servidor=" + str(
                            p['id']) + "), " + str(p['id']) + ",'" + str(p['name']) + "','" + str(
                            p['display_name']) + "','" + str(p['website']) + "','" + str(p['function']) + "','" + str(
                            p['phone']) + "','" + str(p['mobile']) + "',,'" + str(p['email']) + "',," + str(
                            activo) + ");"
                    val = insertcliente  + ']'
                    output += val + '}'
                    json.dumps(output)

                return output

        return request.render('tracking.index')