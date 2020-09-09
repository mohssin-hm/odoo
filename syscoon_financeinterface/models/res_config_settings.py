# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class syscoonFinanceInterfaceConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    company_export_finance_interface = fields.Selection(related='company_id.export_finance_interface', readonly=False)