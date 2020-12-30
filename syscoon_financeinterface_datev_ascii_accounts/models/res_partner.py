# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    datev_exported = fields.Boolean('Exported to DATEV', default=False, company_dependent=True)

    def write(self, values):
        if not values.get('datev_exported'):
            values['datev_exported'] = False
        return super(ResPartner, self).write(values)
