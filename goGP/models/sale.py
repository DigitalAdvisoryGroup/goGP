# -*- coding: utf-8 -*-

from odoo import api, fields, models, SUPERUSER_ID, _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _find_mail_template(self, force_confirmation_template=False):
        template_id = super(SaleOrder, self)._find_mail_template(force_confirmation_template)
        event_registration_ids = self.env['event.registration'].search([('sale_order_id', '=', self.id)])
        if event_registration_ids and self.attendee_count:
            template_id = False
        return template_id
