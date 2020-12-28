# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.

from odoo import models, api, fields, _
from odoo.exceptions import UserError



class SocialGroups(models.Model):
    _name = 'social_groups'
    _description = 'goGP social groups'

    name = fields.Char("Social group name")
    description = fields.Text("Description")


class SocialGroupsCodes(models.Model):
    _name = 'social_groups.codes'
    _description = 'goGP codes for social groups'

    name = fields.Char("Social group code name")