# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
from odoo.exceptions import UserError

import time


class syscoonFinanceinterfaceExport(models.TransientModel):
    _name = 'syscoon.financeinterface.export'
    _description = 'Export Wizard for the syscoon financeinterface'

    export_id = fields.Many2one('syscoon.financeinterface', 'Export', readonly=True)
    type = fields.Selection(selection=[('date', 'Date'), ('date_range', 'Date Range')], 
        string='Export Type')
    date_from = fields.Date('Date From', default=lambda *a: time.strftime('%Y-%m-01'))
    date_to = fields.Date('Date To', default=lambda *a: time.strftime('%Y-%m-%d'))
    date = fields.Date('Date', default=lambda *a: time.strftime('%Y-%m-%d'))
    mode = fields.Selection(selection=[('none', 'None')], string='Export Mode', required=True, default=lambda self: self._get_default_mode())

    def _get_default_mode(self):
        """Function to get the default selected journal ids from the company settings"""
        company_id = self.env.user.company_id
        if company_id.export_finance_interface:
            return company_id.export_finance_interface
        else:
            return

    @api.onchange('mode')
    def _onchange_mode(self):
        return

    def action_start(self):
        """ Start the export through the wizard
        """
        if self.mode == False:
            raise UserError(_('No Export-Method selected. Please select one or install further Modules to provide an Export-Method!'))
        return True
