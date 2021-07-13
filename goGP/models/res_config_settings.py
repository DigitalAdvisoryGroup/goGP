# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    invoice_confirmation_template_id = fields.Many2one('mail.template', string='Invoice Confirmation Email',
                                                       domain="[('model', '=', 'account.move')]",
                                                       config_parameter='goGP.default_invoice_confirmation_template')
