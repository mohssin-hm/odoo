# -*- coding: utf-8 -*-
# This file is part of Odoo. The COPYRIGHT file at the top level of
# this module contains the full copyright notices and license terms.

{
    'name': 'Partner Debitoren- / Kreditorenkonto Automatik- Purchase',
    'version': '13.0.1.0.4',
    'author': 'syscoon GmbH',
    'license': 'OPL-1',
    'category': 'Accounting',
    'website': 'https://syscoon.com',
    'depends': [
        'syscoon_partner_account_company_automatic',
        'purchase',
    ],
    'description': """New debit and credit account will be created automatically when order is confirmed.""",
    'data': [

    ],
    'init_xml': [],
    'demo_xml': [],
    'update_xml': [],
    'active': False,
    'installable': True
}
