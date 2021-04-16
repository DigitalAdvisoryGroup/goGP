# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

{
    'name': "goGP",
    'version': '1.0',
    'summary': """
        Odoo customizations for goGP
    """,
    'description': """

goGP
====
goGP

Description
-----------

    """,

    'author': "Digital Advisory Group GmbH, Candidroot Solutions Pvt. Ltd.",
    'website': "https://www.digitaladvisorygroup.io/",
    'category': 'Event',
    'depends': ['event_enterprise','sale_management','contacts','website_event','event_sale','website_event_sale'],
    'data': [
            "security/ir.model.access.csv",
            "data/data.xml",
            "views/assets.xml",
            "views/vehicles_view.xml",
            "views/vehicles_brand_view.xml",
            "views/vehicles_models_type_view.xml",
            "views/social_group_type_view.xml",
            "views/vehicles_models_view.xml",
            "views/vehicles_fuel_type_view.xml",
            "views/racefields_view.xml",
            "views/social_group_view.xml",
            "views/my_event_view.xml",
            "views/nomination_view.xml",
            "views/my_profile_view.xml",
            "views/res_partner_view.xml",
            "views/partner_sex_type_view.xml",
            "views/partner_shirt_type_view.xml",
            "views/event_view.xml",
            "views/portal_views.xml",
            "views/menu.xml",
    ],
    'demo': [
    ],
    'qweb': [
            "static/src/xml/kanban_extend_view.xml",
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    "post_init_hook": "post_init_hook_login_convert",
}
