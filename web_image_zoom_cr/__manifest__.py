 # -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.
{
    'name': "Web Image Zoom",
    'category': 'Web',
    'summary': """Web Image Zoom.""",
    'version': '14.0.0.1',
    'author': "Candidroot Solutions Pvt. Ltd.",
    'website': 'https://www.candidroot.com/',
    'sequence': 2,
    'description': """Web Image Zoom.""",
    'depends': ['web'],
    'data': [
        'views/assets.xml',
    ],
    'qweb': ['static/src/xml/*.xml'],
    'images' : [],
    'installable': True,
    'auto_install': False,
    'application': False,
}
