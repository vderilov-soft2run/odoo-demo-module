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

    @api.onchange('type')
    def _onchange_type_clear_values(self):
        for record in self:
            if record.type != "product":
                record.netsurf_device_type = False
            if record.type != "service":
                record.netsurf_service_type = False
                record.service_speed = 0
                
    @api.constrains('netsurf_device_type', 'netsurf_service_type', 'service_speed', 'type')
    def _check_required_fields(self):
        for record in self:
            if record.type == 'product' and not record.netsurf_device_type:
                raise ValidationError("Field Device Type is required. Please select the appropriate option.")
            
            if record.type == 'service':
                if not record.netsurf_service_type:
                    raise ValidationError("Field Service Type is required. Please select the appropriate option.")
            
                if record.netsurf_service_type != 'other_services' and record.service_speed == 0:
                    raise ValidationError("Field Service Speed is required. Please enter a value greater than 0.")
