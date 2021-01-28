# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by Candidroot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

from . import controllers
from . import models

def post_init_hook_login_convert(cr, registry):
    """After the module is installed, set all logins to lowercase
    :param openerp.sql_db.Cursor cr:
        Database cursor.
    :param openerp.modules.registry.RegistryManager registry:
        Database registry, using v7 api.
    """
    with cr.savepoint():
        print("--------post---------------")
        cr.execute("UPDATE res_users SET login=lower(login)")