# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    receivable_sequence_id = fields.Many2one(
        'ir.sequence', 'Receivable Sequence',
        related="company_id.receivable_sequence_id",
        readonly=False,
        domain=[('code', '=', 'partner.auto.receivable')])
    receivable_template_id = fields.Many2one(
        'account.account',
        'Receivable Account Template',
        related="company_id.receivable_template_id",
        readonly=False,
        domain=[('user_type_id.type', '=', 'receivable')])
    receivable_group_id = fields.Many2one(
        'account.group',
        'Receivable Account Group',
        related="company_id.receivable_group_id",
        readonly=False)
    payable_sequence_id = fields.Many2one(
        'ir.sequence',
        'Payable Sequence',
        related="company_id.payable_sequence_id",
        readonly=False,
        domain=[('code', '=', 'partner.auto.payable')])
    payable_template_id = fields.Many2one(
        'account.account',
        'Payable Account Template',
        related="company_id.payable_template_id",
        readonly=False,
        domain=[('user_type_id.type', '=', 'payable')])
    payable_group_id = fields.Many2one(
        'account.group',
        'Payable Account Group', 
        related="company_id.payable_group_id",
        readonly=False)
    add_number_to_partner_ref = fields.Boolean(
        'Add Account Number to Partner Ref',
        related="company_id.add_number_to_partner_ref",
        readonly=False)
    use_separate_accounts = fields.Boolean(
        'Use Separate Accounts',
        related="company_id.use_separate_accounts",
        readonly=False)

