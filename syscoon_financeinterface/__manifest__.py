# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{   'name': 'syscoon Finanzinterface',
    'version': '13.0.1.0.6',
    'depends': ['account'],
    'author': 'syscoon GmbH',
    'license': 'OPL-1',
    'website': 'https://syscoon.com',
    'summary': 'Main Modul for export of accounting moves',
    'description': """The main modul syscoon_financeinterface provides the basic
        methods for finance exports to accounting software.""",
    'category': 'Accounting',
    'data': [
        'data/syscoon_financeinterface_sequence.xml',
        'security/syscoon_financeinterface_security.xml',
        'security/ir.model.access.csv',
        'views/account_move.xml',
        'views/syscoon_financeinterface.xml',
        'views/res_config_settings.xml',
        'wizards/syscoon_financeinterface_export.xml'
    ],
    'active': False,
    'installable': True
}
