# -*- coding: utf-8 -*-
{
    'name': "Netsurf Product Extension",

    'summary': "This module extends existing Odoo functionality to serve Netsurf's business requirements",

    'description': """
Long description of module's purpose
    """,

    'author': "Soft2Run",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock', 'sale_management', 'purchase', 'helpdesk', 'industry_fsm'],

    # always loaded
    # security will be implemented once new non-inherited models are defined for netsurf.
    'data': [
        # 'security/ir.model.access.csv',
        # 'data/data.xml', 
        'views/netsurf_product_extension_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

