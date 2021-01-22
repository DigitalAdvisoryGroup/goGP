# -*- coding: utf-8 -*-

from odoo import fields, http, _
from odoo.http import request
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website_event.controllers.main import WebsiteEventController
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager


class goGPPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        partner = request.env.user.partner_id

        goGPmyevent = request.env['gogp.my.event']
        goGPmyvehicle = request.env['gogp.vehicles']
        goGPmygroups = request.env['gogp.social_groups']
        if 'myevent_count' in counters:
            values['myevent_count'] = goGPmyevent.search_count([('attendee_id', '=', partner.id)]) if goGPmyevent.check_access_rights('read', raise_exception=False) else 0
        if 'myvehicle_count' in counters:
            values['myvehicle_count'] = goGPmyvehicle.search_count([('driver_id', '=', partner.id)]) if goGPmyvehicle.check_access_rights('read', raise_exception=False) else 0
        if 'mygroups_count' in counters:
            values['mygroups_count'] = goGPmygroups.search_count([('partner_ids', 'in', partner.ids)]) if goGPmygroups.check_access_rights('read', raise_exception=False) else 0
        return values

    @http.route(['/my/gogp/events', '/my/gogp/events/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_gogp_event(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        goGPmyevent = request.env['gogp.my.event']

        domain = [('attendee_id', '=', partner.id)]

        searchbar_sortings = {
            'date': {'label': _('Date'), 'order': 'create_date desc'},
        }

        # default sortby order
        if not sortby:
            sortby = 'date'

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # count for pager
        gogp_event_count = goGPmyevent.search_count(domain)
        # make pager
        pager = portal_pager(
            url="/my/gogp/events",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=gogp_event_count,
            page=page,
            step=self._items_per_page
        )
        # search the count to display, according to the pager data
        myevents = goGPmyevent.search(domain, limit=self._items_per_page, offset=pager['offset'])
        print("----myevents---------",myevents)
        request.session['my_gogpevent_history'] = myevents.ids[:100]

        values.update({
            'date': date_begin,
            'myevents': myevents.sudo(),
            'page_name': 'myevent',
            'pager': pager,
            'default_url': '/my/gogp/events',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
        })
        return request.render("goGP.portal_my_gogp_events", values)

    @http.route(['/my/gogp/vehicles', '/my/gogp/vehicles/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_gogp_vehicle(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        goGPmyvehicle = request.env['gogp.vehicles']

        domain = [('driver_id', '=', partner.id)]

        searchbar_sortings = {
            'date': {'label': _('Date'), 'order': 'create_date desc'},
        }

        # default sortby order
        if not sortby:
            sortby = 'date'

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # count for pager
        gogp_vehicle_count = goGPmyvehicle.search_count(domain)
        # make pager
        pager = portal_pager(
            url="/my/gogp/vehicles",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=gogp_vehicle_count,
            page=page,
            step=self._items_per_page
        )
        # search the count to display, according to the pager data
        myvehicles = goGPmyvehicle.search(domain, limit=self._items_per_page, offset=pager['offset'])
        print("----myvehicles---------", myvehicles)
        request.session['my_gogpvehicle_history'] = myvehicles.ids[:100]

        values.update({
            'date': date_begin,
            'myvehicles': myvehicles.sudo(),
            'page_name': 'myvehicle',
            'pager': pager,
            'default_url': '/my/gogp/vehicles',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
        })
        return request.render("goGP.portal_my_gogp_vehicles", values)

    @http.route(['/my/gogp/groups', '/my/gogp/groups/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_gogp_groups(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        goGPmygroups = request.env['gogp.social_groups']

        domain = [('partner_ids', 'in', partner.ids)]

        searchbar_sortings = {
            'date': {'label': _('Date'), 'order': 'create_date desc'},
        }

        # default sortby order
        if not sortby:
            sortby = 'date'

        if date_begin and date_end:
            domain += [('create_date', '>', date_begin), ('create_date', '<=', date_end)]

        # count for pager
        gogp_group_count = goGPmygroups.search_count(domain)
        # make pager
        pager = portal_pager(
            url="/my/gogp/groups",
            url_args={'date_begin': date_begin, 'date_end': date_end, 'sortby': sortby},
            total=gogp_group_count,
            page=page,
            step=self._items_per_page
        )
        # search the count to display, according to the pager data
        mygroups = goGPmygroups.search(domain, limit=self._items_per_page, offset=pager['offset'])
        print("----mygroups---------", mygroups)
        request.session['my_gogpgroups_history'] = mygroups.ids[:100]

        values.update({
            'date': date_begin,
            'mygroups': mygroups.sudo(),
            'page_name': 'mysg',
            'pager': pager,
            'default_url': '/my/gogp/groups',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
        })
        return request.render("goGP.portal_my_gogp_groups", values)


class CustomWebsiteEventController(WebsiteEventController):

    @http.route()
    def event_register(self, event, **post):
        if event.is_login_req and not request.env.user.active:
            redirect_url = '/web/login?redirect=%s' % ('/event/%s/register' % (slug(event)))
            return request.render("goGP.event_auth_required", {'event': event.sudo(), 'redirect_url': redirect_url})
        else:
            return super(CustomWebsiteEventController, self).event_register(event, **post)
