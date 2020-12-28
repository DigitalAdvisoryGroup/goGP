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
    'depends': ['event_enterprise','base'],
    'data': [
            "security/ir.model.access.csv",
            "views/vehicles_view.xml",
            "views/vehicles_brand_view.xml",
            "views/vehicles_models_view.xml",
            "views/racefields_view.xml",
            "views/social_group_view.xml",
            "views/my_event_view.xml",
            "views/nomination_view.xml",
            "views/my_profile_view.xml",
            "views/menu.xml",
    ],
    'demo': [
    ],
    'qweb': [

    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
