# -*- coding: utf-8 -*-
# This file is part of Odoo. The COPYRIGHT file at the top level of
# this module contains the full copyright notices and license terms.

{
    'name': 'Partner Debitoren- / Kreditorenkonto Automatik',
    'version': '13.0.1.0.7',
    'author': 'syscoon GmbH',
    'license': 'OPL-1',
    'category': 'Accounting',
    'website': 'https://syscoon.com',
    'depends': [
        'syscoon_partner_account_company',
    ],
    'description': """If a partner is created a new debit and credit account will be created automatically.""",
    'data': [
        'views/res_config_settings_views.xml',
    ],
    'init_xml': [],
    'demo_xml': [],
    'update_xml': [],
    'active': False,
    'installable': True
}
