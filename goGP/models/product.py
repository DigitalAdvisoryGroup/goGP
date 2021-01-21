# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.

from odoo import models, api, fields, _
from odoo.exceptions import UserError



class ProductTemplate(models.Model):
    _inherit = 'product.template'

    max_purchase = fields.Integer("Max Purchase")