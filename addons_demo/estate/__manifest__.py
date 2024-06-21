# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


{
    'name': 'Estate',
    'version': '1.0',
    'category': 'Sales/Estate',
    'summary': 'Track real estate properties',
    'website': 'https://www.odoo.com/app/crm',
    'depends': [
        'base_setup'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
        'views/res_users_views.xml'
    ],
    'application': True,
    'license': 'LGPL-3',
}
