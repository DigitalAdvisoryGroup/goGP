# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.

from odoo import api, fields, models
import logging
_logger = logging.getLogger(__name__)

class ResUsers(models.Model):

    _inherit = "res.users"

    login = fields.Char(help="Used to log into the system. Case insensitive.")

    def action_change_email_lower(self):
        rec_list = []
        for rec in self:
            try:
                rec.login = rec.login.lower()
                rec.partner_id.email = rec.partner_id.email.lower()
            except:
                rec_list.append(rec.id)
                pass
        _logger.info("----------rec_list---------%s",rec_list)

    @classmethod
    def _login(cls, db, login, password,user_agent_env):
        """ Overload _login to lowercase the `login` before passing to the
        super """
        login = login.lower()
        return super(ResUsers, cls)._login(db, login, password,user_agent_env)

    @api.model_create_multi
    def create(self, vals_list):
        """ Overload create multiple to lowercase login """
        for val in vals_list:
            val["login"] = val.get("login", "").lower()
        return super(ResUsers, self).create(vals_list)

    def write(self, vals):
        """ Overload write to lowercase login """
        if vals.get("login"):
            vals["login"] = vals["login"].lower()
        return super(ResUsers, self).write(vals)