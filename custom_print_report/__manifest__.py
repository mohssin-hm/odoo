# -*- coding: utf-8 -*-
##############################################################################
#
#    Haresh Kansara
#    Copyright (C) 2020-TODAY Haresh Kansara(hareshkansara00@gmail.com).
#    Author: Haresh Kansara(hareshkansara00@gmail.com).
#    you can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    "name": "Custom Print Report",
    "version": "13.0.0.1",
    "category": "Sales",
    "license": "AGPL-3",
    'author': 'Haresh Kansara',
    'maintainer': 'Haresh Kansara',
    'website': 'hareshkansara.odoo.com',
    'support': 'hareshkansara00@gmail.com',
    'summary': 'Custom Print Report For Sales/Quotation and Invoices',
    'description': 'Custom Print Report For Sales/Quotation and Invoices',
    "depends": ['sale_quotation_builder', 'sale_management', 'helpdesk'],
    "data": [
        'views/assets.xml',
        'views/sale_quote_template_view.xml',
        # Templates
        'templates/sale_template.xml',
    ],
}
