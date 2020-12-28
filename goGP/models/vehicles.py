# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.

from odoo import models, api, fields, _
from odoo.exceptions import UserError


class VehiclesV(models.Model):
    _name = 'vehicles'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'goGP Vehicles'

    image_128 = fields.Binary("Logo")
    brand_id = fields.Many2one("vehicles.brands", related="model_id.brand_id", string="Brand")
    model_id = fields.Many2one("vehicles.models", string="Model")
    license_plate = fields.Char("License Plate")
    active = fields.Boolean("Active", default=True)
    vehicle_type = fields.Selection(related="model_id.vehicle_type", string="Vehicle Type")
    driver_id = fields.Many2one("res.partner", "Driver")
    owner_id = fields.Many2one("res.partner", "Owner")
    location = fields.Char("Location")
    odometer = fields.Float("Last Odometer")
    odometer_unit = fields.Selection([('','')],string="Odometer Unit")
    acquisition_date = fields.Date("Immatriculation Date")
    vin_sn = fields.Char("Chassis Number")
    seats = fields.Integer("Seats Number")
    doors = fields.Integer("Doors Number")
    color = fields.Char("Color")
    model_year = fields.Char("Model Year")
    description = fields.Text("Vehicle Description")
    modifications = fields.Char("Modification")
    transmission = fields.Selection([('','')],string="Transmission")
    cm3 = fields.Integer("Cubic centimetres")
    cylinders = fields.Integer("Cylinders")
    horsepower = fields.Integer("Horsepower")
    power = fields.Integer("Power")
    fuel_type = fields.Selection([('','')],string="Fuel Type")
    co2 = fields.Float("CO2 Emissions")
    fia_homologation = fields.Char("FIA Homologation:")
    fia_doc = fields.Char("FIA Document")
    fia_periode = fields.Char("FIA Period")

    def name_get(self):
        result = []
        for rec in self:
            name = rec.model_id.name + ' (' + rec.driver_id.name+')'
            result.append((rec.id, name))
        return result



class VehiclesBrand(models.Model):
    _name = 'vehicles.brands'
    _description = 'goGP Vehicle Brands'

    name = fields.Char("Make")
    image_128 = fields.Binary("Logo")
    model_count = fields.Integer("Model Count")
    model_ids = fields.One2many("vehicles.models", "brand_id", string="Model")


class VehiclesModels(models.Model):
    _name = 'vehicles.models'
    _description = 'goGP Vehicle Models'

    name = fields.Char("Model name")
    active = fields.Boolean("Active", default=True)
    brand_id = fields.Many2one("vehicles.brands", string="Manufacturer")
    image_128 = fields.Binary("Logo", related="brand_id.image_128")
    manager_id = fields.Many2one("res.users", string="Fleet Manager")
    vendor_ids = fields.Many2many("res.partner", string="Vendors")
    vehicle_type = fields.Selection([('car','Car')], string="Vehicle Type")
    nickname = fields.Char("NickName")



