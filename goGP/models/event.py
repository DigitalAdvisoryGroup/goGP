# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.

from odoo import models, api, fields, _
from odoo.exceptions import UserError



class Event(models.Model):
    _inherit = 'event.event'

    is_login_req = fields.Boolean("Login Required")


class EventTicket(models.Model):
    _inherit = 'event.event.ticket'
    _order = 'sequence'

    sequence = fields.Integer('Sequence', default=1)

