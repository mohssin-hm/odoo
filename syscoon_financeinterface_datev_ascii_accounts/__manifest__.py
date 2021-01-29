# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{   'name': 'Finanzinterface - Datev ASCII Account Export',
    'version': '13.0.1.0.17',
    'depends': [
        'syscoon_financeinterface_datev_ascii',
        'syscoon_partner_account_company',
    ],
    'author': 'syscoon GmbH',
    'license': 'OPL-1',
    'website': 'https://syscoon.com',
    'summary': 'Module for exporting DATEV ASCII accounts',
    'description': """The module that export the accounts (standard, debit, credit)
                    to DATEV ASCII.""",
    'category': 'Accounting',
    'data': [
        'wizards/syscoon_financeinterface_export.xml',
        'views/res_config_settings.xml',
        'views/syscoon_financeinterface.xml',
    ],
    'active': False,
    'installable': True
}
