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
    is_user_registered = fields.Boolean(string='Is User Registered', compute='_compute_is_user_registered')
    is_user_registered_no = fields.Integer(string='Is User Registered No', compute='_compute_is_user_registered')


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

    @api.depends('registration_ids')
    def _compute_is_user_registered(self):
        for ticket in self:
            ticket = ticket.sudo()
            current_user_registration_ids = ticket.registration_ids.filtered(lambda reg: reg.email == self.env.user.email)
            if current_user_registration_ids:
                ticket.is_user_registered = True
                ticket.is_user_registered_no = len(current_user_registration_ids)
            else:
                ticket.is_user_registered = False
                ticket.is_user_registered_no = 0


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    sidecar = fields.Boolean("Sidecar")

    def _get_website_registration_allowed_fields(self):
        return {'name', 'phone', 'email', 'mobile', 'event_id', 'partner_id', 'event_ticket_id', 'sidecar'}

    def create_socialgroup_sidecar(self):
        parnter_id = self.env["res.partner"].sudo()
        social_group_name = False
        for reg in self:
            email_partner = self.env['res.partner'].sudo().search([('email','=',reg.email)],limit=1)
            if email_partner:
                if not reg.sidecar:
                    social_group_name = email_partner.name+"-Group"
                parnter_id |= email_partner
        if parnter_id:
            sidecar_type_id = self.env['gogp.social_groups.type'].sudo().search([('code','=','sidcar')])
            if sidecar_type_id:
                socialgroup_vals = {
                    "type_id": sidecar_type_id.id,
                    "partner_ids": parnter_id.ids,
                    "name": social_group_name
                }
                self.env['gogp.social_groups'].sudo().create(socialgroup_vals)



    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('email'):
                vals['email'] = vals['email'].lower()
        return super(EventRegistration, self).create(vals_list)

