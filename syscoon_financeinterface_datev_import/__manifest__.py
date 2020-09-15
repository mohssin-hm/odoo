# -*- coding: utf-8 -*-
# This file is part of Odoo. The COPYRIGHT file at the top level of
# this module contains the full copyright notices and license terms.

{
    'name': 'Finanzinterface - Datev ASCII Import',
    'version': '13.0.0.0.1',
    'license': 'OPL-1',
    'author': 'syscoon GmbH',
    'website': 'https://syscoon.com',
    'description': """The module ecoservice_financeinterface_datev_import allows you to import accounting entries.

Details of the module:
* Import of accounting entries
""",
    'category': 'Accounting',
    'summary': 'Import of DATEV Moves.',
    'depends': [
        'account',
        'syscoon_financeinterface_datev_ascii',
        'syscoon_partner_account_company',
    ],
    'data': [
        'views/import_datev.xml',
        'views/import_datev_config.xml',
        'views/import_datev_menu.xml',
        'views/account_tax.xml',
        'data/import_config.xml',
        'data/import_datev_sequence.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
}
