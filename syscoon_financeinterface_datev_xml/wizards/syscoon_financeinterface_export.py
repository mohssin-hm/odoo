# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class syscoonFinanceinterfaceExport(models.TransientModel):
    _inherit = 'syscoon.financeinterface.export'

    mode = fields.Selection(selection_add=[('datev_xml', 'DATEV XML')])
    xml_mode = fields.Selection([('standard', 'Standard'), ('extended', 'Extended')],
        string='XML-Export Methode',
        help='Export Methode: Standard: without Accounts, Extended: with Accounts',
    )
    xml_invoices = fields.Selection([('customers', 'Customer Invoices'), ('vendors', 'Vendor Invoices'), ('both', 'Both')], string='Invoices')

    @api.onchange('mode')
    def _onchange_mode(self):
        """ Inherits the basic onchange mode """
        res = super(syscoonFinanceinterfaceExport, self)._onchange_mode()
        company_id = self.env.user.company_id
        if self.mode and self.mode == 'datev_xml':
            self.xml_mode = company_id.export_xml_mode
            self.type = 'date_range'
        return res

    def action_start(self):
        """Inherit of the basic start function"""
        start = super(syscoonFinanceinterfaceExport, self).action_start()
        if self.mode == 'datev_xml':
            if self.type != 'date_range':
                raise UserError(_('For the DATEV XML export you must select the type "Date Range" to do an export!'))
            args = [self.xml_mode, self.xml_invoices]
            export_id = self.env['syscoon.financeinterface'].export(self.mode, self.date_from, self.date_to, args)
            return {
                'name': 'Financial Export Invoices',
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': False,
                'res_model': 'syscoon.financeinterface',
                'type': 'ir.actions.act_window',
                'target': 'current',
                'res_id': export_id,
            }
        else:
            return start
