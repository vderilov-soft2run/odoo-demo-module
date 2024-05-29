from odoo import fields, models

class PropertyType(models.Model):

    _name = 'estate.property.type'
    _order = 'sequence, name'
    _sql_constraints = [
        (
            "check_name",
            "UNIQUE(name)",
            "A property type name must be unique",
        )
    ]

    name = fields.Char()
    sequence = fields.Integer('Sequence', default=1)
    property_ids = fields.One2many('estate.property', 'property_type_id')