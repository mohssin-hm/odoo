# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class ResCompany(models.Model):
    _inherit = "res.company"

    create_auto_account_on = fields.Selection([('invoices', 'Invoices'), ('orders','Orders')], default='invoices',
                                              help=_(
                                                  'Select where the Accounts should be created. If on creating an invoice no account exists, it will created it then.'))

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    create_auto_account_on = fields.Selection([('invoices', _('Invoices')), ('orders', _('Orders'))],related="company_id.create_auto_account_on",readonly=False,
                                              help=_(
                                                  'Select where the Accounts should be created. If on creating an invoice no account exists, it will created it then.'))