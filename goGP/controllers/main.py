# -*- coding: utf-8 -*-

from odoo import fields, http, _
from odoo.http import request
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website_event.controllers.main import WebsiteEventController


class CustomWebsiteEventController(WebsiteEventController):

    @http.route()
    def event_register(self, event, **post):
        if event.is_login_req and not request.env.user.active:
            redirect_url = '/web/login?redirect=%s' % ('/event/%s/register' % (slug(event)))
            return request.render("goGP.event_auth_required", {'event': event.sudo(), 'redirect_url': redirect_url})
        else:
            return super(CustomWebsiteEventController, self).event_register(event, **post)
