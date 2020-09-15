# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Finanzinterface - Datev XML Export',
    'version': '13.0.1.0.15',
    'author': 'syscoon GmbH',
    'license': 'OPL-1',
    'category': 'Accounting',
    'website': 'https://syscoon.com',
    'summary': 'Create XML exports that can be imported in DATEV. Infromations under https://www.datev.de/dnlexom/client/app/index.html#/document/1036101.',
    'external_dependencies': {
        'python': ['PyPDF2']
    },
    'depends': [
        'syscoon_financeinterface',
    ],
    'data': [
        'views/res_config_settings.xml',
        'wizards/syscoon_financeinterface_export.xml',
    ],
    'installable': True,
    'application': False,
}
