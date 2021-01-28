# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.

from odoo import models, api, fields, _
from odoo.exceptions import UserError


class VehiclesV(models.Model):
    _name = 'gogp.vehicles'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'goGP Vehicles'

    active = fields.Boolean("Active", default=True)
    name = fields.Char("Nickname")
    image_128 = fields.Binary("Logo")
    brand_id = fields.Many2one("gogp.vehicles.brands", related="model_id.brand_id", string="Brand")
    # brand_id = fields.Many2one("gogp.vehicles.brands", string="Brand")
    model_id = fields.Many2one("gogp.vehicles.models", string="Model")
    license_plate = fields.Char("License Plate")
    location = fields.Char("Location")
    color = fields.Char("Color")
    model_year = fields.Char("Model Year")
    # vehicle_type_id = fields.Many2one(related="model_id.vehicle_type_id", string="Vehicle Type")
    vehicle_type_id = fields.Many2one("gogp.vehicles.models.type", string="Vehicle Type")
    driver_id = fields.Many2one("res.partner", "Driver")
    owner_id = fields.Many2one("res.partner", "Owner")
    fuel_type_id = fields.Many2one("gogp.vehicles.fuel.type", string="Fuel Type")
    odometer = fields.Float("Last Odometer")
    acquisition_date = fields.Date("Immatriculation Date")
    vin_sn = fields.Char("Chassis Number")
    seats = fields.Integer("Seats Number")
    doors = fields.Integer("Doors Number")
    description = fields.Text("Vehicle Description")
    modifications = fields.Char("Modification")

    cm3 = fields.Integer("Cubic centimetres")
    cylinders = fields.Integer("Cylinders")
    horsepower = fields.Integer("Horsepower")
    power = fields.Integer("Power")
    co2 = fields.Float("CO2 Emissions")
    fia_homologation = fields.Char("FIA Homologation:")
    fia_doc = fields.Char("FIA Document")
    fia_periode = fields.Char("FIA Period")

    odometer_unit = fields.Selection([('', '')], string="Odometer Unit")
    transmission = fields.Selection([('', '')], string="Transmission")

    def name_get(self):
        result = []
        for rec in self:
            name = rec.model_id.name + ' (' + rec.driver_id.name+')'
            result.append((rec.id, name))
        return result


class VehiclesFuelType(models.Model):
    _name = 'gogp.vehicles.fuel.type'
    _description = 'goGP Vehicle Fuel Type'

    name = fields.Char("Name", translate=True)


class VehiclesBrand(models.Model):
    _name = 'gogp.vehicles.brands'
    _description = 'goGP Vehicle Brands'
    _order = "name"

    name = fields.Char("Make")
    image_128 = fields.Binary("Logo")
    model_count = fields.Integer("Model Count")
    model_ids = fields.One2many("gogp.vehicles.models", "brand_id", string="Model")


class VehiclesModels(models.Model):
    _name = 'gogp.vehicles.models'
    _description = 'goGP Vehicle Models'
    _order = "name"

    name = fields.Char("Model name")
    active = fields.Boolean("Active", default=True)
    brand_id = fields.Many2one("gogp.vehicles.brands", string="Manufacturer")
    image_128 = fields.Binary("Logo", related="brand_id.image_128")
    manager_id = fields.Many2one("res.users", string="Fleet Manager")
    vendor_ids = fields.Many2many("res.partner", string="Vendors")
    vehicle_type_id = fields.Many2one("gogp.vehicles.models.type", string="Vehicle Type")
    nickname = fields.Char("NickName")


class VehiclesModelsType(models.Model):
    _name = 'gogp.vehicles.models.type'
    _description = 'goGP Vehicle Models Type'

    name = fields.Char("Name")
    code = fields.Char("Code")



