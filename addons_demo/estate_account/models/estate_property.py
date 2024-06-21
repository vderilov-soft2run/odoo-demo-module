from odoo import models, exceptions

class Property(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        raise exceptions.UserError("override success")
        return super(Property, self).action_sold()
