from odoo import fields, models

class PropertyTag(models.Model):
    _name = 'estate.property.tag'
    _order = 'name'
    _sql_constraints = [
        (
            "check_name",
            "UNIQUE(name)",
            "A property tag name must be unique",
        )
    ]

    name = fields.Char(required=True)
    color = fields.Integer()