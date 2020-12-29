# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.

from odoo import models, api, fields, _
from odoo.exceptions import UserError



class Nomination(models.Model):
    _name = 'gogp.nomination'
    _description = 'goGP nomination'

    name = fields.Char("Nomination name")
    