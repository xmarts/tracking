# -*- coding: utf-8 -*-
import logging
from odoo import http
from odoo.http import request
import json

_logger = logging.getLogger(__name__)


class trackController(http.Controller):
    #parameter = {"CAT_CL":'2017-10-09 16:47:55',"CAT_PR":'-'}

    @http.route('/track', type='http', auth='user', methods=['GET'])
    def pos_web(self, debug=False,**k):
        print("valor par: %s"+ request.params['CAT_CL'])
        json_list = {
            'clientes': [],
            'clientes_dirs': [],
            'productos': [],
            'estados': [],
        }
        try:
            if request.params['CAT_CL'] or request.params['CAT_CLD'] or request.params['CAT_P'] or request.params['CAT_ES']  :
                valsproduct = {}
                vals = {}
                valscld = {}
                valsstate = {}
                valspaises = {}

                ####################CLIENTES#####################################
                partner_model = request.env['res.partner']
                fecha_inicio = str(request.params['CAT_CL']) + '.0'
                partner_ids = partner_model.search([('write_date','>=',fecha_inicio)])
                cont=str(len(partner_ids))
                data=str(request.params['CAT_CL']+' '+cont)
                if partner_ids:
                    insertcliente=""
                    print(partner_ids)
                    for p in partner_ids:
                        print("valor de fecha clientes"+ p.write_date)
                        if str(p.active) == False:
                            activocl = 0
                        else:
                            activocl = 1
                        insertcliente = insertcliente + "INSERT OR REPLACE INTO CLIENTE(id,id_servidor,nombre,nombre_comercial,sitio_web,puesto_trabajo,tel,movil,fax,email,id_precio_lista,active)" + " VALUES((select id from cliente where id_servidor=" + str(p.id) + "), " + str(p.id) + ",'" + str(p.name) + "','" + str(p.display_name) + "','" + str(p.website) + "','" + str(p.function) + "','" + str(p.phone) + "','" + str(p.mobile) + "',,'" + str(p.email) + "',"+str(p.property_product_pricelist.id) + str(activocl) + ");"
                    vals = {
                        data:insertcliente
                    }
                #################### DIRECCION CLIENTES############################
                fecha_cld = str(request.params['CAT_CLD']) + '.0'
                partnercld_ids = partner_model.search([('write_date', '>=', fecha_cld)])
                contcld = str(len(partnercld_ids))
                datacld = str(request.params['CAT_CLD'] + ' ' + contcld)
                if partnercld_ids:
                    insertclientecld = ""
                    print(partnercld_ids)
                    for pcl in partnercld_ids:
                        print("valor de fecha clientes direcciones" + p.write_date)
                        if str(pcl.active) == False:
                            activodir = 0
                        else:
                            activodir = 1
                        if pcl.parent_id is False:
                            pclid = pcl.id
                        else:
                            pclid=pcl.parent_id.id
                        insertclientecld = insertclientecld + "INSERT OR REPLACE INTO cliente_direccion(id, id_servidor, id_cliente_local, id_cliente_servidor, tipo, calle, num_ext, num_int, ciudad, id_estado, cp, id_pais, contacto, email, tel, movil, notas, active) VALUES((select  id from cliente_direccion where id_servidor ="+ str(pcl.id)+")," +str(pcl.id)+", (select id from cliente where id_servidor ="+str(pclid)+")," +str(pcl.id)+"',"+str(pcl.type)+"','"+str(pcl.street)+"','',"+"'','"+str(pcl.city)+"',"+str(pcl.state_id)+",'"+str(pcl.zip)+"',"+str(pcl.country_id)+",'','"+str(pcl.email)+"','"+str(pcl.phone)+"','"+str(pcl.mobile)+"','',"+str(activodir)+");"

                    valscld = {
                        datacld: insertclientecld
                    }
                #####################PRODUCTOS###########################
                product_model = request.env['product.template']
                fechap_inicio = str(request.params['CAT_P']) + '.0'
                product_ids = product_model.search([('write_date', '>=', fechap_inicio)])
                contp = str(len(product_ids))
                dataproduct = str(request.params['CAT_P'] + ' ' + contp)
                if product_ids:
                    insertproduct = ""
                    print(product_ids)
                    for pr in product_ids:
                        print("valor de fecha product" + pr.write_date)
                        if str(pr.active) == False:
                            activoproduct = 0
                        else:
                            activoproduct = 1
                        insertproduct = insertproduct + "INSERT OR REPLACE INTO producto(id_servidor,codigo,nombre,descripcion,precio_unitario,piezas_caja,active) VALUES("+str(pr.id)+",'"+str(pr.default_code)+"','"+str(pr.name)+"','"+str(pr.description)+"',"+str(pr.list_price)+","+str(pr.uom_id.name)+", "+str(activoproduct)+");"
                    valsproduct = {
                        dataproduct: insertproduct
                    }
                #####################Estados###########################
                estado_model = request.env['res.country.state']
                fechastate_inicio = str(request.params['CAT_ES']) + '.0'
                state_ids = estado_model.search([('write_date', '>=', fechastate_inicio)])
                contstate = str(len(state_ids))
                datastate = str(request.params['CAT_ES'] + ' ' + contstate)
                if state_ids:
                        insertstate = ""
                        print(state_ids)
                        for state in state_ids:
                            print("valor de fecha state" + pr.write_date)

                            insertstate = insertstate + "INSERT OR REPLACE INTO estado (id_servidor,id_pais,nombre,active) VALUES(" + str(state.id)+", "+str(state.country_id.id)+",'"+str(state.name)+"',"+str(True)+");"

                        valsstate = {
                            datastate: insertstate
                        }
                #####################Paises###########################
                #paises_model = request.env['res.country']
                #fechapaises_inicio = str(request.params['CAT_PA']) + '.0'
                #paises_ids = estado_model.search([('write_date', '>=', fechapaises_inicio)])
                #contpaises = str(len(state_ids))
                #datapaises= str(request.params['CAT_PA'] + ' ' + contpaises)
                #if paises_ids:
                #    insertpaises = ""
                #    for pais in paises_ids:
                #        print("valor de fecha pais" + pr.write_date)
                #        insertpaises = insertpaises + "INSERT OR REPLACE INTO pais (id_servidor,nombre,active) VALUES(" + str(pais.id) +",'" + str(pais.name) + "'," + str(True) + ");"

                #    valspaises = {
                #        datapaises: insertpaises
                #    }
                json_list['clientes'].append(vals)
                json_list['clientes_dirs'].append(valscld)
                json_list['productos'].append(valsproduct)
                json_list['estados'].append(valsstate)
                #json_list['paises'].append(valspaises)
            return json.dumps(json_list)
        except Exception as e:
            print(e)
        return json.dumps({'status': 0, 'data': 'Existe un problema en la API :o'})


