# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class AccountAccount(models.Model):
    _inherit = 'account.account'

    datev_exported = fields.Boolean('Exported')
    datev_diverse_account = fields.Boolean('Diverse Account')

    def write(self, vals):
        res = super(AccountAccount, self).write(vals)
        if 'datev_exported' not in vals:
            vals['datev_exported'] = False
        return res
