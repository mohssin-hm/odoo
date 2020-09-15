# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class ResCompany(models.Model):
    _inherit = "res.company"

    receivable_sequence_id = fields.Many2one('ir.sequence', 'Receivable Sequence',
                                             domain=[('code', '=', 'partner.auto.receivable')])
    payable_sequence_id = fields.Many2one('ir.sequence', 'Payable Sequence',
                                          domain=[('code', '=', 'partner.auto.payable')])
    receivable_template_id = fields.Many2one('account.account', 'Receivable Account Template')
    receivable_group_id = fields.Many2one('account.group', 'Receivable Account Group')
    payable_template_id = fields.Many2one('account.account', 'Payable Account Template',
                                          domain=[('type', '=', 'payable')])
    payable_group_id = fields.Many2one('account.group', 'Payable Account Group' )
    add_number_to_partner_ref = fields.Boolean('Add Account Number to Partner Ref')
    use_separate_accounts = fields.Boolean('Use Separate Accounts')
