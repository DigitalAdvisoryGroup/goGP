# -*- coding: utf-8 -*-

from odoo import fields, http, _
from odoo.http import request
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website_event.controllers.main import WebsiteEventController
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager
import base64
import werkzeug


class goGPWebsiteSale(WebsiteSale):

    @http.route()
    def checkout(self, **post):
        order = request.website.sale_get_order(update_pricelist=True)
        return super(goGPWebsiteSale, self).checkout(**post)


class goGPPortal(CustomerPortal):

    OPTIONAL_BILLING_FIELDS = ["zipcode", "state_id", "vat", "company_name","partner_sex_id","birthdate","acc_number","partner_shirt_size_id"]

    @http.route()
    def account(self, redirect=None, **post):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        PartnerBank = request.env['res.partner.bank'].sudo()
        parnter_bank_ids = PartnerBank.search([('partner_id', '=', partner.id)], limit=1)
        values.update({
            'error': {},
            'error_message': [],
        })

        if post and request.httprequest.method == 'POST':
            print("------post---------",post)
            if 'image_1920' in post:
                image_1920 = post.get('image_1920')
                if image_1920:
                    image_1920 = image_1920.read()
                    image_1920 = base64.b64encode(image_1920)
                    partner.sudo().write({
                        'image_1920': image_1920
                    })
                post.pop('image_1920')
            if 'clear_avatar' in post:
                partner.sudo().write({
                    'image_1920': False
                })
                post.pop('clear_avatar')
            error, error_message = self.details_form_validate(post)
            values.update({'error': error, 'error_message': error_message})
            values.update(post)
            if not error:
                values = {key: post[key] for key in self.MANDATORY_BILLING_FIELDS}
                values.update({key: post[key] for key in self.OPTIONAL_BILLING_FIELDS if key in post})
                for field in set(['country_id', 'state_id','partner_sex_id','partner_shirt_size_id']) & set(values.keys()):
                    try:
                        values[field] = int(values[field])
                    except:
                        values[field] = False
                values.update({'zip': values.pop('zipcode', '')})
                if values.get("acc_number"):
                    if parnter_bank_ids:
                        parnter_bank_ids.write({'acc_number':values.get("acc_number")})
                    else:
                        partner_bank_vals = {
                            "partner_id": partner.id,
                            "acc_number": values.get("acc_number")
                        }
                        request.env['res.partner.bank'].sudo().create(partner_bank_vals)
                values.pop('acc_number')
                partner.sudo().write(values)
                if redirect:
                    return request.redirect(redirect)
                return request.redirect('/my/home')

        countries = request.env['res.country'].sudo().search([])
        states = request.env['res.country.state'].sudo().search([])
        sextypes = request.env['partner.sex.type'].sudo().search([])
        shirtsizes = request.env['partner.shirt.size'].sudo().search([])

        values.update({
            'partner': partner,
            'countries': countries,
            'sextypes': sextypes,
            'shirtsizes': shirtsizes,
            'states': states,
            'acc_number': parnter_bank_ids and parnter_bank_ids.acc_number or '',
            'has_check_vat': hasattr(request.env['res.partner'], 'check_vat'),
            'redirect': redirect,
            'page_name': 'my_details',
        })

        response = request.render("portal.portal_my_details", values)
        response.headers['X-Frame-Options'] = 'DENY'
        return response

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        partner = request.env.user.partner_id

        goGPmyevent = request.env['gogp.my.event'].sudo()
        goGPmyvehicle = request.env['gogp.vehicles']
        goGPmygroups = request.env['gogp.social_groups']
        if 'myevent_count' in counters:
            values['myevent_count'] = goGPmyevent.search_count([('attendee_id', '=', partner.id),('event_registration_id.event_ticket_id.price','!=',0.0)]) if goGPmyevent.check_access_rights('read', raise_exception=False) else 0
        if 'myvehicle_count' in counters:
            values['myvehicle_count'] = goGPmyvehicle.search_count([('driver_id', '=', partner.id)]) if goGPmyvehicle.check_access_rights('read', raise_exception=False) else 0
        if 'mygroups_count' in counters:
            values['mygroups_count'] = goGPmygroups.search_count([('partner_ids', 'in', partner.ids)]) if goGPmygroups.check_access_rights('read', raise_exception=False) else 0
        return values

    @http.route(['/my/gogp/events', '/my/gogp/events/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_gogp_events(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        goGPmyevent = request.env['gogp.my.event'].sudo()

        domain = [('attendee_id', '=', partner.id),('event_registration_id.event_ticket_id.price','!=',0.0)]

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

    @http.route(['/my/gogp/event/<model("gogp.my.event"):myevent>'], type='http', auth="user", website=True)
    def portal_my_gogp_event_detail(self, myevent=None, **kw):
        if kw:
            if not kw.get("vehicle_id"):
                kw['vehicle_id'] = False
            if not kw.get("racefield_id"):
                kw['racefield_id'] = False
            myevent.sudo().write(kw)
            return request.redirect('/my/gogp/events')
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        values.update({
            'error': {},
            'error_message': [],
        })
        if myevent:
            my_vehicles = request.env['gogp.vehicles'].sudo().search([('driver_id','=',partner.id)])
            racefields = request.env['gogp.racefields'].sudo().search([])
            values.update({
                'vehicles': my_vehicles,
                'racefields': racefields,
                'myevent': myevent.sudo(),
                'page_name': 'my_event_detail',
            })
        return request.render("goGP.portal_my_gogp_event_details", values)

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

    @http.route(['/my/gogp/vehicle/<model("gogp.vehicles"):myvehicle>'], type='http', auth="user", website=True)
    def portal_my_gogp_vehicle_detail(self, myvehicle=None, **kw):
        if kw:
            if kw.get("image_128"):
                image_128 = base64.b64encode(kw.get("image_128").read())
                if image_128:
                    kw.update({'image_128': image_128})
            else:
                kw.pop("image_128")
            if 'clear_avatar' in kw:
                kw.pop("clear_avatar")
                kw.update({'image_128': False})
            for field in set(['brand_id', 'model_id', 'vehicle_type_id', 'fuel_type_id']) & set(kw.keys()):
                try:
                    kw[field] = int(kw[field])
                except:
                    kw[field] = False
            for field in set(['odometer', 'cm3', 'cylinders', 'horsepower','power']) & set(kw.keys()):
                try:
                    kw[field] = float(kw[field].replace("'",""))
                except:
                    kw[field] = False
            myvehicle.sudo().write(kw)
            return request.redirect('/my/gogp/vehicles')
        values = self._prepare_portal_layout_values()
        values.update({
            'error': {},
            'error_message': [],
        })
        if myvehicle:
            vehicle_fuel_type = request.env['gogp.vehicles.fuel.type'].sudo().search([])
            vehicle_brands = request.env['gogp.vehicles.brands'].sudo().search([])
            vehicle_models = request.env['gogp.vehicles.models'].sudo().search([])
            vehicle_models_type = request.env['gogp.vehicles.models.type'].sudo().search([])
            values.update({
                'vehicles': myvehicle,
                'vehicle_fuel_type': vehicle_fuel_type,
                'vehicle_brands': vehicle_brands,
                'vehicle_models': vehicle_models,
                'vehicle_models_type': vehicle_models_type,
                'page_name': 'my_vehicle_detail',
            })
        return request.render("goGP.portal_my_gogp_vehicle_details", values)

    @http.route(['/my/gogp/vehicle/delete/<model("gogp.vehicles"):myvehicle>'], type='http', auth="user", website=True)
    def portal_my_gogp_vehicle_delete(self, myvehicle=None, **kw):
        if myvehicle:
            myvehicle.unlink()
        return request.redirect("/my/gogp/vehicles")

    @http.route(['/my/gogp/vehicle/add'], type='http', auth="user", website=True)
    def portal_my_gogp_vehicle_add(self, **kw):
        if kw:
            image_128 = kw.get("image_128") and base64.b64encode(kw.get("image_128").read()) or ''
            kw.update({'driver_id': request.env.user.partner_id.id,'image_128':image_128})
            request.env['gogp.vehicles'].sudo().create(kw)
            return request.redirect('/my/gogp/vehicles')
        values = self._prepare_portal_layout_values()
        values.update({
            'error': {},
            'error_message': [],
        })
        vehicle_fuel_type = request.env['gogp.vehicles.fuel.type'].sudo().search([])
        vehicle_brands = request.env['gogp.vehicles.brands'].sudo().search([])
        vehicle_models = request.env['gogp.vehicles.models'].sudo().search([])
        vehicle_models_type = request.env['gogp.vehicles.models.type'].sudo().search([])
        values.update({
            'vehicle_fuel_type': vehicle_fuel_type,
            'vehicle_brands': vehicle_brands,
            'vehicle_models': vehicle_models,
            'vehicle_models_type': vehicle_models_type,
            'page_name': 'my_vehicle_detail',
        })
        return request.render("goGP.portal_my_gogp_vehicle_details_add", values)

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

    @http.route(['/my/gogp/group/<model("gogp.social_groups"):mygroup>'], type='http', auth="user", website=True)
    def portal_my_gogp_groups_detail(self, mygroup=None, **kw):
        mygroup = mygroup.sudo()
        if kw:
            return request.redirect('/my/gogp/groups')
        values = self._prepare_portal_layout_values()
        values.update({
            'error': {},
            'error_message': [],
        })
        if mygroup:
            types = request.env['gogp.social_groups.type'].sudo().search([])
            values.update({
                'mygroup': mygroup,
                'types': types,
                'mygroup_contacts': mygroup.partner_ids,
                'page_name': 'my_group_detail',
            })
        return request.render("goGP.portal_my_gogp_group_details", values)


class CustomWebsiteEventController(WebsiteEventController):

    @http.route()
    def event_register(self, event, **post):
        if event.is_login_req and not request.env.user.active:
            redirect_url = '/web/login?redirect=%s' % ('/event/%s/register' % (slug(event)))
            return request.render("goGP.event_auth_required", {'event': event.sudo(), 'redirect_url': redirect_url})
        else:
            return super(CustomWebsiteEventController, self).event_register(event, **post)

    def _create_attendees_from_registration_post(self, event, registration_data):
        resp = super(CustomWebsiteEventController, self)._create_attendees_from_registration_post(event,registration_data)
        for registration_values in registration_data:
            reg_email = registration_values['email'].lower()
            registration_values['email'] = reg_email
            if not reg_email == request.env.user.email.lower():
                portal_user_id = request.env['res.users'].sudo().search([('login', '=', reg_email)])
                if not portal_user_id:
                    another_partner_id = request.env['res.partner'].sudo().search([('email', '=', reg_email)])
                    user_vals = {
                        'company_id': request.env.company.id,
                        'name': registration_values['name'],
                        'login': reg_email,
                        'email': reg_email,
                        'lang': "de_CH",
                        'groups_id': [(6, 0, [request.env.ref('base.group_portal').id])]
                    }
                    if another_partner_id:
                        user_vals.update({'partner_id': another_partner_id.ids[0]})
                    request.env['res.users'].sudo().create(user_vals)
        for res in resp:
            gogp_myevent_vals = {
                'name': res.event_id.name,
                "attendee_id": res.partner_id.id,
                "event_id": res.event_id.id,
                "event_registration_id": res.id,
            }
            request.env['gogp.my.event'].sudo().create(gogp_myevent_vals)
        if any(resp.mapped("sidecar")):
            resp.create_socialgroup_sidecar()
        return resp

    def _process_attendees_form(self, event, form_details):
        """ Process data posted from the attendee details form.

        :param form_details: posted data from frontend registration form, like
            {'1-name': 'r', '1-email': 'r@r.com', '1-phone': '', '1-event_ticket_id': '1'}
        """
        allowed_fields = {'name', 'phone', 'email', 'mobile', 'event_id', 'partner_id', 'event_ticket_id','sidecar'}
        registration_fields = {key: v for key, v in request.env['event.registration']._fields.items() if key in allowed_fields}
        registrations = {}
        global_values = {}
        for key, value in form_details.items():
            counter, attr_name = key.split('-', 1)
            field_name = attr_name.split('-')[0]
            if field_name not in registration_fields:
                continue
            elif isinstance(registration_fields[field_name], (fields.Many2one, fields.Integer)):
                value = int(value) or False  # 0 is considered as a void many2one aka False
            else:
                value = value

            if counter == '0':
                global_values[attr_name] = value
            else:
                registrations.setdefault(counter, dict())[attr_name] = value
        for key, value in global_values.items():
            for registration in registrations.values():
                registration[key] = value
        print("-----list(registrations.values())---our-----",list(registrations.values()))
        return list(registrations.values())


    @http.route()
    def registration_new(self, event, **post):
        if not event.can_access_from_current_website():
            raise werkzeug.exceptions.NotFound()
        tickets = self._process_tickets_form(event, post)
        ticket_ids = request.env['event.event.ticket'].sudo()
        for ticket in tickets:
            if ticket.get("ticket").is_exclusive:
                ticket_ids |= ticket.get("ticket")
        if len(ticket_ids) > 1:
            return request.env['ir.ui.view']._render_template("goGP.event_registation_validate",{'error': (_("You can not select more than one exclusive ticket"))})
        availability_check = True
        if event.seats_limited:
            ordered_seats = 0
            for ticket in tickets:
                ordered_seats += ticket['quantity']
            if event.seats_available < ordered_seats:
                availability_check = False
        if not tickets:
            return False
        return request.env['ir.ui.view']._render_template("website_event.registration_attendee_details", {'user': request.env.user,'tickets': tickets, 'event': event, 'availability_check': availability_check})



