from odoo import models, Command

class Property(models.Model):
    _inherit = 'estate.property'

    def action_sold(self):
        for record in self:
            record.env['account.move'].create({
                    "name": record.name,
                    "move_type": "out_invoice",
                    "partner_id": record.buyer_id.id,
                    "line_ids": [
                        Command.create({
                            "name": "selling price",
                            "price_unit": record.selling_price + (record.selling_price * 0.06),
                            "quantity": 1
                        }),
                        Command.create({
                            "name": "administrative fees",
                            "price_unit": 100,
                            "quantity": 1
                        })
                    ]
                }
            )

        return super().action_sold()
