# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, exceptions
from dateutil.relativedelta import relativedelta


class Property(models.Model):
    _name = "estate.property"
    _description = "Property model"
    _order = "id desc"
    _sql_constraints = [
        (
            "check_expected_price",
            "CHECK(expected_price > 0)",
            "A property expected price must be strictly positive",
        ),
        (
            "check_selling_price",
            "CHECK(selling_price > 0)",
            "A property selling price must be positive",
        ),
    ]

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    active = fields.Boolean(default=True)
    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")
    date_available = fields.Date(
        copy=False, default=fields.Date.today() + relativedelta(months=+3)
    )

    garden_orientation = fields.Selection(
        string="Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    state = fields.Selection(
        string="State",
        selection=[
            ("new", "New"),
            ("recieved", "Offer Recieved"),
            ("accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        default="new",
        required=True,
        copy=False,
    )

    property_type_id = fields.Many2one("estate.property.type", string="Property type")
    property_tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id")
    buyer_id = fields.Many2one("res.partner", "Buyer", copy=False, readonly=True)
    salesperson_id = fields.Many2one(
        "res.users", "Salesperson", default=lambda self: self.env.user
    )

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price < record.expected_price * 0.90 and record.selling_price:
                raise exceptions.ValidationError('Selling price cannot be lower than 90% of the expected price')

    @api.depends("garden_area", "living_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if len(record.mapped("offer_ids.price")):
                record.best_price = max(record.mapped("offer_ids.price"))
            else:
                record.best_price = 0

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = None

    @api.onchange("offer_ids")
    def _onchange_offer_ids(self):
        for record in self:
            if len(record.offer_ids) and record.state == "new":
                record.state = "recieved"

    def action_sold(self):
        for record in self:
            if record.state == "canceled":
                raise exceptions.UserError("Canceled properties cannot be sold")
            record.state = "sold"
        return True

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                raise exceptions.UserError("Sold properties cannot be canceled")
            record.state = "canceled"
        return True


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _order = "price desc"
    _sql_constraints = [
        (
            "check_price",
            "CHECK(price > 0)",
            "An offer price must be strictly positive",
        )
    ]

    price = fields.Float()
    validity = fields.Integer(default=7, inverse="_inverse_date_deadline")
    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline"
    )

    status = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")], copy=False
    )

    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.to_date(
                record.create_date if record.create_date else fields.Date.today()
            ) + relativedelta(days=+record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = relativedelta(
                record.date_deadline,
                record.create_date if record.create_date else fields.Date.today(),
            ).days

    def action_confirm(self):
        for record in self:
            if record.status == "refused":
                raise exceptions.UserError("This offer has already been refused")

            if record.property_id.state == "accepted":
                raise exceptions.UserError(
                    "An offer has already been accepted for this property"
                )

            if record.property_id.state == "sold":
                raise exceptions.UserError("This property has already been sold")

            if record.property_id.state == "canceled":
                raise exceptions.UserError("This property has been canceled")

            record.status = "accepted"
            record.property_id.state = "accepted"
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price

    def action_decline(self):
        for record in self:
            if record.status == "accepted":
                raise exceptions.UserError("This offer has already been accepted")

            record.status = "refused"
