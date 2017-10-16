# -*- coding: utf-8 -*-
{
    'name': "Tracking",

    'summary': """
       Tracking""",

    'description': """
   Tracking
    """,

    'author': "Nayeli Valencia Díaz",
    'website': "http://www.xmarts.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','purchase'],
    # always loaded
    'data': [
        'views/sale_order.xml',
'views/track_template.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
