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

from odoo import models


class ReportBomStructure(models.AbstractModel):
    _inherit = 'report.mrp.report_bom_structure'

    def _get_bom(self, bom_id=False, product_id=False, line_qty=False, line_id=False, level=False):
        res = super(ReportBomStructure, self)._get_bom(
            bom_id, product_id, line_qty, line_id, level)
        res['product_img'] = 'product_img.1'
        res['supplier'] = 'supplier.1'

        res['product_img'] = ''
        res['supplier'] = ''
        res['supplier_id'] = ''

        if res['product']:
            res['product_img'] = res['product'].image_1920

            suppliers = res['product'].seller_ids
            if suppliers and suppliers[0].name:
                res['supplier'] = suppliers[0].name.name
                res['supplier_id'] = suppliers[0].name.id
        return res

    def _add_img_and_supplier(self, components):
        for line in components:
            line['product_img'] = ''
            line['supplier'] = ''
            line['supplier_id'] = ''
            if line.get('prod_id'):
                product = self.env['product.product'].sudo().browse(
                    line.get('prod_id', 0))
                if product:
                    line['product_img'] = product.image_1920
                    suppliers = product.seller_ids
                    if suppliers and suppliers[0].name:
                        line['supplier'] = suppliers[0].name.name
                        line['supplier_id'] = suppliers[0].name.id
        return True

    def _get_bom_lines(self, bom, bom_quantity, product, line_id, level):
        components, total = super(ReportBomStructure, self)._get_bom_lines(
            bom, bom_quantity, product, line_id, level)
        self._add_img_and_supplier(components)
        return components, total

    def _get_pdf_line(self, bom_id, product_id=False, qty=1, child_bom_ids=[], unfolded=False):
        data = super(ReportBomStructure, self)._get_pdf_line(
            bom_id, product_id, qty, child_bom_ids, unfolded)
        self._add_img_and_supplier(data['lines'])
        return data
