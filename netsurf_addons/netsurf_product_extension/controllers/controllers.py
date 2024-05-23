# -*- coding: utf-8 -*-
# from odoo import http


# class NetsurfProductExtension(http.Controller):
#     @http.route('/netsurf_product_extension/netsurf_product_extension', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/netsurf_product_extension/netsurf_product_extension/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('netsurf_product_extension.listing', {
#             'root': '/netsurf_product_extension/netsurf_product_extension',
#             'objects': http.request.env['netsurf_product_extension.netsurf_product_extension'].search([]),
#         })

#     @http.route('/netsurf_product_extension/netsurf_product_extension/objects/<model("netsurf_product_extension.netsurf_product_extension"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('netsurf_product_extension.object', {
#             'object': obj
#         })

