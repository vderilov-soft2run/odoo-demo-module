# -*- coding: utf-8 -*-

from odoo import models, fields, api


class NetsurfProductTemplate(models.Model):
    _inherit = 'product.template'
    
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
    )
    
    netsurf_service_type = fields.Selection(
        selection=[
            ('internet_main', 'Internet main service'),
            ('internet_addon', 'Internet add-on'),
            ('tv_main', 'TV main service'),
            ('tv_addon', 'TV add-on'),
            ('man_service', 'MAN service'),
            ('service_pack', 'Service Pack'),
            ('other_services', 'Other Services'),
        ],
        string='Service type',
        required=False,
        store=True,
        copy=True,
    )
    
    create_ticket = fields.Boolean(
        string='Create a ticket',
        default=False,
        help='If set to true, Odoo will create a ticket on Sales Order confirmation.',
        store=True,
        copy=True,
    )

    service_speed = fields.Float(
        string='Service speed',
        required=False,
        store=True,
        copy=True,
        digits=(16, 0),
    )
    
    @api.onchange('type')
    def _onchange_product_type(self):
        for record in self:
            if record.type == 'product':
                record.device_type = record.device_type or 'ont'
                record._fields['device_type'].required = True
            else:
                record._fields['device_type'].required = False

            if record.type == 'service':
                record.netsurf_service_type = record.netsurf_service_type or 'internet_main'
                record._fields['netsurf_service_type'].required = True
            else:
                record._fields['netsurf_service_type'].required = False

    @api.onchange('netsurf_service_type')
    def _onchange_service_type(self):
        for record in self:
            if record.netsurf_service_type != 'other_services':
                record._fields['service_speed'].required = True
            else:
                record._fields['service_speed'].required = False