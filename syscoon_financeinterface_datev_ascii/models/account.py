# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class AccountAccount(models.Model):
    _inherit = 'account.account'

    datev_vatid_required = fields.Boolean('DATEV VAT-ID', help='Is required when transferring a sales VAT-ID number from the partner (e.g. EU-Invoice)')
    datev_automatic_account = fields.Boolean('DATEV Automatic Account')
    datev_automatic_tax = fields.Many2many('account.tax', string='DATEV Automatic Tax', domain=[('datev_tax_key', '!=', 0)])


class AccountTax(models.Model):
    _inherit = 'account.tax'

    datev_tax_key = fields.Char('DATEV Tax Key', default=0, required=True)
    datev_tax_case = fields.Char('DATEV Tax Case')

