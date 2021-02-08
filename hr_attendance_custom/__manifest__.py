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
    "name": "Attendance Enhancement",
    "version": "13.0.0.1",
    "category": "HR",
    "license": "AGPL-3",
    'author': 'Haresh Kansara',
    'maintainer': 'Haresh Kansara',
    'website': 'hareshkansara.odoo.com',
    'support': 'hareshkansara00@gmail.com',
    'summary': 'Attendance Enhancement Addon',
    'description': 'Attendance Enhancement Addon',
    "depends": ['hr_attendance', 'hr_attendance_report_theoretical_time'],
    "data": [
        'security/security.xml',
        'views/hr_attendance_view.xml',
    ],
    "application": True,
}
