# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Finanzinterface - Datev ASCII Export',
    'version': '13.0.1.0.28',
    'author': 'syscoon GmbH',
    'license': 'OPL-1',
    'website': 'https://syscoon.com',
    'summary': 'DATEV ASCII Export ',
    'description': """The module account_financeinterface_datev provides methods 
        to convert account moves to the Datevformat (Datev Dok.-Nr.: 1036228).""",
    'category': 'Accounting',
    'depends': [
        'syscoon_financeinterface'
    ],
    'data': [
        'views/account_move_views.xml',
        'views/account_views.xml',
        'views/res_config_settings.xml',
        'views/syscoon_financeinterface.xml',
        'wizards/syscoon_financeinterface_export.xml',
    ],
    'active': False,
    'installable': True,
}
