from odoo import fields, models, api
from odoo.exceptions import UserError

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
    offer_ids = fields.One2many(related='property_ids.offer_ids')
    offer_count = fields.Integer(compute="_compute_offer_count")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            offers = 0
            
            for prop in record.property_ids:
               offers += len(prop.offer_ids)

            record.offer_count = offers
