# -*- coding: utf-8 -*-

import base64

from odoo import api, models


class MailTemplate(models.Model):
    _inherit = 'mail.template'

    def generate_email(self, res_ids, fields):
        result = super(MailTemplate, self).generate_email(res_ids, fields)
        if self.model != 'account.move':
            return result
        if isinstance(res_ids, int):
            res_ids = [res_ids]
        if self.model == 'account.move':
            for record in self.env[self.model].browse(res_ids):
                if result.get(record.id) and result.get(record.id).get('attachments'):
                    cnt = 0
                    for attachment in result.get(record.id).get('attachments'):
                        if attachment[0].startswith('ISR'):
                            result.get(record.id).get('attachments').pop(cnt)
                        if attachment[0].startswith('QR-bill'):
                            result.get(record.id).get('attachments').pop(cnt)
                        cnt += 1
                elif result.get('res_id') == record.id:
                    cnt = 0
                    for attachment in result.get('attachments'):
                        if attachment[0].startswith('ISR'):
                            result.get('attachments').pop(cnt)
                        if attachment[0].startswith('QR-bill'):
                            result.get('attachments').pop(cnt)
                        cnt += 1
        return result
