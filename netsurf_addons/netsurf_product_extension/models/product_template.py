# -*- coding: utf-8 -*-

from odoo import models, fields


class NetsurfProductTemplate(models.Model):
    _name = 'netsurf_product_extension'
    _description = 'netsurf_product_extension'
    _inherit = 'product.product'
    
    device_type = fields.Selection(
        selection=[
            ('ont', 'ONT'),
            ('stb', 'STB'),
            ('cables','Cables'),
            ('other_materials', 'Other materials')
        ],
        string = "Device type",
        required = False,
        store = True,
        copy = True,
        translate = True
    )
    
    
    # @api.onchange('type')
    # def _onchange_product_type(self):
    #     for record in self:
    #         if record.type