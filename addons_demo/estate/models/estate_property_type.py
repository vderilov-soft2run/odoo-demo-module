from odoo import fields, models

class PropertyType(models.Model):

    _name = 'estate.property.type'
    _sql_constraints = [
        (
            "check_name",
            "UNIQUE(name)",
            "A property type name must be unique",
        )
    ]

    name = fields.Char()
    property_ids = fields.One2many('')