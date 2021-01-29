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
    "name": "MRP BoM Structure & Cost Custom Report",
    "version": "13.0.0.1",
    "category": "Manufacturing",
    "license": "AGPL-3",
    'author': 'Haresh Kansara',
    'maintainer': 'Haresh Kansara',
    'website': 'hareshkansara.odoo.com',
    'support': 'hareshkansara00@gmail.com',
    'summary': 'MRP BoM Structure & Cost Custom Report',
    'description': 'MRP BoM Structure & Cost Custom Report',
    "depends": ['mrp_plm', 'purchase'],
    "data": [
        'views/assets.xml',
        'report/bom_report_template.xml',
    ],
    "qweb": ['static/src/xml/*.xml'],
    "application": True,
}
