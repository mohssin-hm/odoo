# -*- coding: utf-8 -*-
# This file is part of Odoo. The COPYRIGHT file at the top level of
# this module contains the full copyright notices and license terms.

from odoo import models, fields, api


class Company(models.Model):
    _inherit = 'res.company'

    datev_auto_set_accounts = fields.Selection(selection_add=[('skr03', 'SKR03')])

    def set_datev_skr03(self):
        self.env['account.tax']._set_taxkeys_skr03(self.id)
        self.env['account.account']._set_account_autoaccount_skr03(self.id)
        return

    def write(self, vals):
        if not self.datev_auto_set_accounts and 'datev_auto_set_accounts' in vals and vals['datev_auto_set_accounts'] == 'skr03':
            self.set_datev_skr03()
        return super(Company, self).write(vals)
