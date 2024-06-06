# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class NetsurfProductTemplate(models.Model):
    _inherit = 'product.template'
    
    netsurf_device_type = fields.Selection(
        selection=[
            ('ont', 'ONT'),
            ('stb', 'STB'),
            ('cables','Cables'),
            ('other_materials', 'Other materials')
        ],
        string = "Device type",
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
    

    @api.onchange('netsurf_service_type')
    def _onchange_service_type(self):
        for record in self:
            if record.netsurf_service_type != 'other_services':
                record._fields['service_speed'].required = True
            else:
                record._fields['service_speed'].required = False
                
    @api.constrains('netsurf_device_type')
    def _check_device_type(self):
        for record in self:
            if record.type == 'product' and not record.netsurf_device_type:
                    raise ValidationError("Field Device Type is required. Please select the appropriate option.")

    @api.constrains('netsurf_service_type')
    def _check_required_fields(self):
        for record in self:
            if record.type == 'service' and not record.netsurf_service_type:
                raise ValidationError("Field Service Type is required. Please select the appropriate option.")