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
    is_exclusive = fields.Boolean(related="product_id.is_exclusive", string="Is Exclusive", store=True, readonly=False)
    is_registered = fields.Boolean(string='Is Registered', compute='_compute_is_registered')


    @api.depends('event_id.registration_ids')
    def _compute_is_registered(self):
        for ticket in self:
            current_user = self.env.user
            if ticket.is_exclusive and ticket.event_id.sudo().registration_ids:
                current_user_registration_ids = ticket.event_id.sudo().registration_ids.filtered(lambda reg: reg.email == current_user.email)
                if current_user_registration_ids:
                    ticket.is_registered = True
                else:
                    ticket.is_registered = False
            else:
                ticket.is_registered = False

