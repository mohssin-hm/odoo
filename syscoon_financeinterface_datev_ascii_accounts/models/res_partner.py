# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    datev_exported = fields.Boolean(string='Exported to DATEV', compute='_is_datev_exported')

    def _is_datev_exported(self):
        """ computation for partner, if the account was already exported"""
        for rec in self:
            receivable = (rec.property_account_receivable_id and len(
                rec.property_account_receivable_id.code) > 4 and rec.property_account_receivable_id.datev_exported)
            payable = ( rec.property_account_payable_id and len(
                rec.property_account_payable_id.code) > 4 and rec.property_account_payable_id.datev_exported)
            rec.datev_exported = receivable or payable

    def write(self, vals):
        res = super(ResPartner, self).write(vals)
        if self.property_account_receivable_id and len(self.property_account_receivable_id.code) > 4:
            self.property_account_receivable_id.sudo().write({'datev_exported': False})
        if self.property_account_payable_id and len(self.property_account_payable_id.code) > 4:
            self.property_account_payable_id.sudo().write({'datev_exported': False})
        return res