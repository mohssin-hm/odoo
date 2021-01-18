# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright 2019 EquickERP
#
##############################################################################

{
    'name' : 'Find & Merge Duplicate Data',
    'category': 'Extra Tools',
    'version': '13.0.1.0',
    'author': 'Equick ERP',
    'description': """
        This Module allows to merge duplicate data.
        * Find Duplicate data from any model. User have option for find duplicate data based on the selected field.
        * User can merge the duplicate data of any model like Product, Partners, Product Category as well as any Custom model.
        * It will update the duplicate record reference with original record at all places in your odoo system.
        * It gives the option for what action you want to perform on the duplicate record like Delete, Archived or Nothing.
        * Specific user can merge the duplicate data.
    """,
    'summary': """search duplicate contact | search duplicate partner | search duplicate customer| search duplicate vendor | search duplicate crm | search duplicate lead | find copy data | search duplicate data remove duplicate data | merge customer remove|data cleaning""",
    'depends' : ['base'],
    'price': 126,
    'currency': 'EUR',
    'license': 'OPL-1',
    'website': "",
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'wizard/wizard_merge_data_view.xml',
        'wizard/wizard_search_duplicate_data_view.xml',
        'wizard/wizard_duplicate_data_merge_view.xml'
    ],
    'demo': [],
    'images': ['static/description/main_screenshot.png'],
    'installable': True,
    'auto_install': False,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: